import Graphic.Interface.Screen_interface as si
import pygame
import Graphic.Component.Button as Button

#Header cho đường dẫn nút bấm
head_path = r'Graphic\Assets\button'

#Màn hình rating
class Rating(si.Screen):
    def __init__(self,display,size):
        super().__init__(display,size)
        # Các nút chức năng khác
        self.back_button = Button.ClickButton((head_path+r'\default\Back.png',head_path+r'\hover\Back.png'),
                                              (100,50),(75,35),self.display)
        self.enter_button = Button.ClickButton((head_path+r'\default\Title_button.png',head_path+r'\hover\Title_button.png'),
                                             (200,100),(540,730),self.display,"Enter",text_c='white')
        self.search_button = Button.InputButton([head_path+r'\default\Title_button.png',head_path+r'\default\titlebar_small.png'],
                                                (900,50),(500,90),self.display,"Search Movies",'white',fonts=25)

        self.MovieText = Button.TextBox(self.display,"MOVIES",(500,160),center=True,text_c='black',fonts=30)
        self.RateText = Button.TextBox(self.display, "Rate", (930, 160), center=True, text_c='black', fonts=30)

        self.movie_button = [Button.BackGroundButton(
            (head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'),
            (800, 50), (500, 200), self.display, "Enter Score", 'black',fonts=25),

            Button.BackGroundButton(
                (head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'),
                (800, 50), (500, 250), self.display, "Enter Score", 'black',fonts=25),

            Button.BackGroundButton(
                (head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'),
                (800, 50), (500, 300), self.display, "Enter Score", 'black',fonts=25),

            Button.BackGroundButton(
                (head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'),
                (800, 50), (500, 350), self.display, "Enter Score", 'black',fonts=25),

            Button.BackGroundButton(
                (head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'),
                (800, 50), (500, 400), self.display, "Enter Score", 'black',fonts=25),

            Button.BackGroundButton(
                (head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'),
                (800, 50), (500, 450), self.display, "Enter Score", 'black',fonts=25),

            Button.BackGroundButton(
                (head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'),
                (800, 50), (500, 500), self.display, "Enter Score", 'black',fonts=25),

            Button.BackGroundButton(
                (head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'),
                (800, 50), (500, 550), self.display, "Enter Score", 'black',fonts=25),

            Button.BackGroundButton(
                (head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'),
                (800, 50), (500, 600), self.display, "Enter Score", 'black',fonts=25)
        ]

        self.rate_button = [Button.InputButton(
            (head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'),
            (50, 50), (930, 200), self.display, "...", 'white',fonts=25),

            Button.InputButton(
                [head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'],
                (50, 50), (930, 250), self.display, "...", 'white',fonts=25),

            Button.InputButton(
                [head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'],
                (50, 50), (930, 300), self.display, "...", 'white',fonts=25),

            Button.InputButton(
                [head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'],
                (50, 50), (930, 350), self.display, "...", 'white',fonts=25),

            Button.InputButton(
                [head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'],
                (50, 50), (930, 400), self.display, "...", 'white',fonts=25),

            Button.InputButton(
                [head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'],
                (50, 50), (930, 450), self.display, "...", 'white',fonts=25),

            Button.InputButton(
                [head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'],
                (50, 50), (930, 500), self.display, "...", 'white',fonts=25),

            Button.InputButton(
                [head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'],
                (50, 50), (930, 550), self.display, "...", 'white',fonts=25),

            Button.InputButton(
                [head_path + r'\default\Title_button.png', head_path + r'\default\titlebar_small.png'],
                (50, 50), (930, 600), self.display, "...", 'white',fonts=25)
        ]

        #Kiểm tra không tìm thấy phim
        self.Notfoundtext = Button.TextBox(self.display,"Movie not found!!!",(self.w//2,self.h//2),center=True,text_c='red',fonts=50)


    #Hàm reset đưa về giá trị khởi tạo
    def reset(self):
        self.back_button.reset()
        self.search_button.reset()
        self.enter_button.reset()
        for i in range(len(self.rate_button)):
            self.rate_button[i].reset()
            self.movie_button[i].reset()

    #Vẽ các thành phần
    def draw(self,pos):
        self.enter_button.draw(pos)
        self.back_button.draw(pos)
        self.search_button.draw(pos)
        count = 0
        for i in range(len(self.rate_button)):
            if self.movie_button[i].text:
                self.rate_button[i].draw(pos)
                self.movie_button[i].draw(pos)
                count+=1
        if not count:
            self.Notfoundtext.draw()
        else:
            self.MovieText.draw()
            self.RateText.draw()


    # Hàm chạy
    # Flag_manager: quản lý state
    # system: App xử lý logic
    def run(self,flag_manager,system,cache = None):
        is_search_change = False
        # Mỗi lần được gọi cần đặt lại running là True
        self.running = True
        #Xây dựng cache lưu trữ các phiên đánh giá
        ratelist = dict({})
        #vị trí trong list danh sách
        index = 0
        #Lấy ra moive list từ system
        movielist = system.get_movielist('')
        size = len(movielist)
        while self.running:
            #Kiểm tra xem các thành phần các lại có đủ để chiếu lên không? tránh invalid index
            if index + len(self.rate_button) - 1 >= size:
                #Nếu lớn hơn thì nghĩa là chỉ lấy đủ
                showlist = movielist[index:size]
            else:
                #Ngược lại chia segment
                showlist = movielist[index:index + len(self.rate_button)]
            showsize = len(showlist)
            #lấy vị trí chuột
            pos = pygame.mouse.get_pos()
            self.display.fill("white")
            #bắt sự kiện cho các nút
            for event in pygame.event.get():
                self.event_handle(event, flag_manager)
                self.back_button.event_handle(event, pos)
                self.enter_button.event_handle(event,pos)
                self.search_button.event_handle(event,pos)
                if self.search_button.is_changed:
                    is_search_change = True
                #kiểm tra lăn chuột để chuyển tiếp segment
                if event.type == pygame.MOUSEWHEEL:
                    if event.y<0:
                        if index<size-len(self.rate_button):
                            index+=1
                    elif event.y>0:
                        if index>0:
                            index-=1
                else:
                    #Nếu không mới cho bắt event cho các nút rating
                    for i in range(showsize):
                            self.rate_button[i].event_handle(event,pos)

            #Kiểm tra sự kiện nhập của người dùng để đưa vào điểm rating cho các phim đã đánh giá
            for i in range(showsize):
                if self.rate_button[i].is_active and self.rate_button[i].done:
                    ratelist[showlist[i][0]] = self.rate_button[i].get_value()

            #Kiểm tra nếu người dùng search movies
            if is_search_change:
                data = self.search_button.get_value()
                movielist = system.get_movielist(data)
                size = len(movielist)
                index = 0
                is_search_change = False

            #Kiểm tra người dùng thoát
            if self.back_button.is_active:
                #dừng màn hình và reset xong chuyển qua main
                self.running = False
                self.back_button.reset()
                flag_manager.change("main")

            #Kiểm tra nếu nút enter được bật
            elif self.enter_button.is_active:
                #reset toàn bộ đồi tượng
                self.reset()
                #Lấy dữ liệu rate thu được để train trọng số cho user sau đó dừng để chuyển về main
                system.train(ratelist)
                system.load_rate(ratelist)
                flag_manager.change("main")
                self.running = False

            #Vẽ các đối tượng rate và phim sao cho match điểm với nhau
            for i in range(len(self.movie_button)):
                if i < showsize:
                    #lấy ra các phim
                    self.movie_button[i].text = f'{showlist[i][1]}  {showlist[i][2]}'
                    #Kiểm tra phim được đánh giá chưa
                    if showlist[i][0] in ratelist:
                        #Nếu rồi cho ô rating là điểm tương ứng
                        self.rate_button[i].text = ratelist[showlist[i][0]]
                    elif not self.rate_button[i].is_active:
                        #Nếu chưa thì coi như rate không có gì
                        self.rate_button[i].reset()
                else:
                    self.movie_button[i].text = ''
                    self.rate_button[i].reset()
            #Vẽ các thành phần và cập nhật
            self.draw(pos)
            pygame.display.flip()
        #Reset toàn bộ thành phần
        self.reset()