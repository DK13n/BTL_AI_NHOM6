import Graphic.Interface.Screen_interface as si
import pygame
import Graphic.Component.Button as Button

#Header cho đường dẫn nút bấm
head_path = r'Graphic\Assets\button'


#Trang gợi ý phim
class Reccomend(si.Screen):
    def __init__(self,display,size):
        super().__init__(display,size)
        #Các nút chức năng
        self.back_button = Button.ClickButton([head_path+r'\default\Prev.png',head_path+r'\hover\Prev.png'],
                                              (100,80),(130,700),self.display)
        self.next_button = Button.ClickButton([head_path+r'\default\Next.png',head_path+r'\hover\Next.png'],
                                              (100,80),(950,700),self.display)

        self.movies_bg = Button.BackGroundButton([head_path + r'\default\titlebar_small.png'],
                                                  (900, 100), (540,150), self.display, "Movies", 'white',fonts=25)
        self.back_ground = [Button.BackGroundButton([head_path + r'\default\Title_bar.png'],
                                               (900, 400), (540,400), self.display),
                            Button.BackGroundButton([head_path+r'\default\Movie_icon.png'],
                                                    (400,400),(250,400),self.display)]
        self.home_button = Button.ClickButton([head_path+r'\default\Home.png',head_path+r'\hover\Home.png'],
                                              (100,100),(540,700),self.display)
        self.id_button = Button.TextBox(self.display,"Movies'id:",(380,370),text_c='white',left=True)
        self.genres_button = Button.TextBox(self.display,"Genres:",(380,420),text_c='white',left=True)
        self.score = Button.TextBox(self.display,"Score predict:",(380,470),text_c='white',left=True)
        self.running = True

    #Hàm vẽ các thành phần trong display
    def draw(self,pos):
        self.back_button.draw(pos)
        self.next_button.draw(pos)
        for bg in self.back_ground:
            bg.draw(pos)
        self.movies_bg.draw(pos)
        self.home_button.draw(pos)
        self.id_button.draw()
        self.genres_button.draw()
        self.score.draw()

    # Hàm chạy
    # Flag_manager: quản lý state
    # system: App xử lý logic
    def run(self,flag_manager,system,cache=None):
        # Mỗi lần được gọi cần đặt lại running là True
        self.running = True
        #Lấy ra danh sách gợi ý phim
        recommendlist,rate_predict = system.get_recommend()
        size = len(recommendlist)
        #Hiển thị phim đầu tiên
        index = 0
        self.id_button.text = f"Movie's ID: {recommendlist[index][0]}"
        self.genres_button.text = f"Genres: {",".join(recommendlist[index][2].split('|'))}"
        self.movies_bg.text = f"Movie: {recommendlist[index][1]}"
        self.score.text = f"rate predict: {rate_predict[index]:.3f}"
        while self.running:
            #Lấy vị trí chuột
            pos = pygame.mouse.get_pos()
            self.display.fill("white")
            #Xử lý bắt sự kiện cho các nút chức năng
            for event in pygame.event.get():
                self.event_handle(event,flag_manager)
                self.back_button.event_handle(event,pos)
                self.next_button.event_handle(event,pos)
                self.home_button.event_handle(event,pos)

            #Kiểm tra nếu người dùng chọn xem phim gợi ý trước đó
            if self.back_button.is_active:
                #Lấy index là chia lấy dư để tránh invalid index
                index = (size + (index-1))%size
                self.id_button.text = f"Movie's ID: {recommendlist[index][0]}"
                self.genres_button.text = f"Genres: {",".join(recommendlist[index][2].split('|'))}"
                self.movies_bg.text = f"Movie: {recommendlist[index][1]}"
                self.score.text = f"rate predict: {rate_predict[index]:.3f}"
                #reset lại nút để tránh lỗi
                self.back_button.reset()

            #Kiểm tra người dùng chọn phim gợi ý sau (Tương tự xem trước)
            elif self.next_button.is_active:
                index = (size+(index+1))%size
                self.id_button.text = f"Movie's ID: {recommendlist[index][0]}"
                self.genres_button.text = f"Genres: {",".join(recommendlist[index][2].split('|'))}"
                self.movies_bg.text = f"Movie: {recommendlist[index][1]}"
                self.score.text = f"rate predict: {rate_predict[index]:.3f}"
                self.next_button.reset()

            #Kiểm tra người dùng chọn về home
            elif self.home_button.is_active:
                #dừng màn hình roi chuyển state về main
                self.running = False
                self.home_button.reset()
                flag_manager.change("main")
            #Vẽ và cập nhật màn hình
            self.draw(pos)
            pygame.display.flip()
        #Reset toàn bộ màn hình
        self.reset()