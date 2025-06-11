import sys
import numpy as np
import pandas as pd
import h5py
from sklearn.model_selection import train_test_split
from Model.regression import Regress
from Model.Gradient_Descent import GradientDescent
#from Model.Test_Gradient import GradientDescentTest
import os

class RecommendationSystem:
    def __init__(self,model='g'):
        #Chọn mô hình dự đoán
        if model[0].lower()=='g':
            self.model = GradientDescent(True,5,0)
        elif model[0].lower()=='r':
            self.model = Regress(True,5)

    #Build trọng số
    def build_predict(self,users,rating,genres,genres_by_id,predict):
        print('start building')
        #Tạo danh sách rating theo từng user
        user_rating = dict({})
        user_label = dict({})

        for i in rating[:,0]:
            user_rating[i] = []
            user_label[i] = []

        for user,movie,rate in rating:
            value = [(i in genres_by_id[movie]) for i in genres]
            user_rating[user].append(value)
            user_label[user].append(rate)

        err=[]
        #Train tìm trọng số cho từng user
        for user in user_rating:
            #Chia tập train và tập test
            if len(user_rating[user]) > 1:
                ft_train,ft_test,lb_train,lb_test = train_test_split(user_rating[user],user_label[user],test_size=0.3,random_state=312)
            else:
                ft_train = user_rating[user]
                lb_train = user_label[user]
                ft_test = None
                lb_test = None
            #Train lấy trọng số
            predict[users[user]] = self.model.train(ft_train,lb_train)
            #Test sai số
            if ft_test:
                check = self.model.test(predict[users[user]],ft_test,lb_test)
                err+=check
        #RMSE của mô hình
        print(f'RMSE = {np.sqrt(np.mean(err))}')
        return predict


    def recommend(self,user_w,movies,genres,genres_by_id,user_seen):
        #Lấy ra danh sách các phim chưa xem
        userseen = user_seen
        notseen = [j for j in range(len(userseen)) if userseen[j]==0]
        user_pre = user_w
        feature = []
        for index in notseen:
            movie_id = movies[index][0]
            feature.append([i in genres_by_id[movie_id] for i in genres])
        #Tính toán điểm số cho các phim
        rate_predict = self.model.calculate(user_pre,feature)
        #Sắp xếp lại rate_predict theo chỉ số
        inx_sort = np.argsort(rate_predict)[::-1]
        #Lấy ra 10 phim nhiều điểm nhất
        inx_sort = inx_sort[:10]
        return movies[np.array(notseen)[inx_sort]],rate_predict[inx_sort]




