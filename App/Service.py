import pandas as pd
import numpy as np
import h5py
import sys

from pyexpat import features

from App.RecommendSys import RecommendationSystem as Rcm

class App:
    def __init__(self,path,genres):
        print('Tải dữ liệu từ Data...')
        self.recommend = Rcm()
        # Thể loại phim
        self.genres = genres

        # Đường dẫn đến Data
        self.path = path

        # Mỗi thể loại là 1 feature, thêm bias
        self.size_w = len(genres) + 1

        # Lọc ra rating (features + labels)
        try:
            with h5py.File(self.path['rating'], 'r') as f:
                self.rating = f['float_matrix'][:]
        except Exception as e:
            sys.exit(f'Không tìm thấy file {self.path['rating']}')

        # Lọc movies
        self.movies = np.array(pd.read_csv(self.path['movies'], encoding='latin1'))
        self.movies_inx = dict({int(self.movies[i][0]): i for i in range(len(self.movies))})

        # Tạo dict Users với userId và thứ tự trong bảng predict
        self.users = np.array(pd.read_csv(self.path['users'], encoding='latin1'))[:, 1:].flatten().astype('int')
        self.user = np.random.choice(self.users)
        self.users = dict({int(self.users[i]): i for i in range(len(self.users))})

        # Lọc genres theo id phim
        self.genres_by_id = dict(
            {int(self.movies[i][0]): str(self.movies[i][2]).split('|') for i in range(len(self.movies))})

        # Tạo trọng số theo thể loại cho từng user
        self.predict = np.array([])
        try:
            with h5py.File(self.path['users_weight'], 'r') as f:
                self.predict = f['float_matrix'][:]
        except:
            print('Không tìm thấy file user_weight.h5! Thiết lập mới')
            self.predict = np.zeros((len(self.users), self.size_w))
            self.predict=self.recommend.build_predict(self.users,self.rating,self.genres,self.genres_by_id,self.predict)

        #Cache cho lượt user: weight, isseen
        self.user_w = None
        self.user_isseen = None
        self.caches_ = dict({
            'new_user': dict({
            }),
            'new_rating':[]
        })
        self.set_user(self.user)
        print('Tải dữ liệu hoàn tất!')


    #Chuyển user khác
    def set_user(self,user):
        #Kiểm tra user có tồn tại chưa
        if user not in self.users:
            #Khởi tạo mới user và đưa vào cache
            self.users[user] = len(self.users)
            self.user_w = np.zeros(self.size_w)
            self.caches_['new_user'][str(self.users[user])] = dict({
                'weight':self.user_w,
            })
            print("New user")
        else:
            #Nếu đã tồn tại có thể nó sẽ nằm trong cache hoặc nằm trong users
            user_inx = self.users[user]
            #Kiểm tra tồn tại trong caches không. Nếu không sẽ là người dùng của lượt cũ
            if str(user_inx) not in self.caches_['new_user']:
                self.user_w = self.predict[user_inx]
            #Ngược lại sẽ là người dùng nằm trong caches
            else:
                self.user_w = self.caches_['new_user'][str(user_inx)]['weight']

        #Tạo vector phim đã xem, tìm phim xem rồi bằng cách kiểm tra lịch sử đánh giá
        self.user_isseen = np.zeros(len(self.movies))
        for uid, mid, i in self.rating:
            if uid == user:
                self.user_isseen[self.movies_inx[mid]] = True

        #lưu cache người dùng hiện tại
        self.user = user

    #Thêm vào những rating mới với datas là dict
    def load_rate(self,datas:dict):
        for data in datas:
            try:
                data = [self.user,int(data),float(datas[data])]
                self.caches_['new_rating'].append(data)
            except:
                pass

    #lấy trọng số của người dùng hiện tại
    def get_userw(self):
        user_inx = self.users[self.user]
        #Kiểm tra xem người dùng đã co trọng số được lưu vào predict chưa
        if user_inx >= len(self.predict):
            #Chưa có thì sẽ nằm trong caches
            user_w = self.caches_['new_user'][str(user_inx)]['weight']
        else:
            #Ngược lại sẽ lấy ra predict đã lưu
            user_w = self.predict[user_inx]
        return user_w


    #Train thêm dữ liệu cho trọng số của người dùng
    def train(self,data:dict):
        #Lấy ra thông tin về weight, index
        user_inx = self.users[self.user]
        user_w = self.get_userw()

        #Lấy data chia thành feature và label
        data = data.items()
        feature = []
        label = []
        for item in data:
            try:
                label.append(float(item[1]))
                feature.append([i in self.genres_by_id[int(item[0])] for i in self.genres])
            except:
                pass

        #Kiểm tra feature có rỗng không
        if feature:
            #nếu không tiến hành train
            self.user_w = self.recommend.model.train(feature,label,weight=user_w)
            if user_inx<len(self.predict):
                self.predict[user_inx] = self.user_w
            else:
                self.caches_["new_user"][str(user_inx)]["weight"] = self.user_w

    #Lấy ra gợi ý dựa vào trọng số và phim chưa xem của user
    def get_recommend(self):
        return self.recommend.recommend(self.user_w,self.movies,self.genres,self.genres_by_id,self.user_isseen)


    #Lấy ra các movies có id chua data
    def get_movielist(self,data):
        #Nếu data khác rỗng sẽ bắt đầu tìm kiếm phim
        if data:
            #lấy ra các id phim
            col = (self.movies[:,0].astype(str) + self.movies[:,1].astype(str))
            #Kiểm tra data có nằm trong các tên hoặc id của phim không
            moviesindex = np.where(np.char.find(np.char.lower(col),str(data).lower())>=0)
            movieslist = self.movies[moviesindex]
        else:
            #Nếu rỗng sẽ lấy toàn bộ movies
            movieslist = self.movies
        return movieslist


    #Cập nhật lại các thay đổi vào CSDL
    def push_data(self):

        #Lấy ra các trọng số mới của các người dùng mới
        newpredict = np.array([j["weight"] for j in self.caches_['new_user'].values() ])
        #Kiểm tra nếu có trọng số mới
        if len(newpredict):
            #Cập nhật thêm trọng số mới
            self.predict = np.concat([self.predict,newpredict])
        #Nếu không có trọng số mới nhưng có người dùng mơi
        elif len(self.caches_['new_user']):
            self.predict = np.concat([self.predict,np.zeros((len(self.caches_['new_user']),self.size_w))])

        #Cập nhật các rating mới nếu có
        if self.caches_["new_rating"]:
            self.rating = np.concat([self.rating,self.caches_["new_rating"]])

        #Ghi đè dữ liệu đã cập nhật
        try:
            pd.DataFrame(self.users.keys()).to_csv(self.path['users'])

            with h5py.File(self.path['users_weight'], 'w') as f:
                f.create_dataset('float_matrix', data=self.predict)

            with h5py.File(self.path['rating'], 'w') as f:
                f.create_dataset('float_matrix', data=self.rating)

        except Exception as e:
            print(str(e))