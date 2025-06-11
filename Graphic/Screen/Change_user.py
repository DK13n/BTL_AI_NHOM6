import Graphic.Interface.Screen_interface as si
import pygame
import Graphic.Component.Button as Button

#Header cho path dẫn đến assets nút
head_path = r'Graphic\Assets\button'

#Display Sửa User
class ChangeUser(si.Screen):
    def __init__(self,display,size):
        super().__init__(display,size)

        #Tạo ra các nút bấm và background
        self.back_button = Button.ClickButton((head_path+r'\default\Out.png',head_path+r'\hover\Out.png'),
                                              (40,40),(815,225),self.display)
        self.enter_button = Button.ClickButton((head_path+r'\default\Join.png',head_path+r'\hover\Join.png'),
                                               (100,50),(540,470),self.display)
        self.user_button = Button.InputButton((head_path+r'\default\Title_button.png',head_path+r'\default\titlebar_small.png'),
                                                (350,100),(540,370),self.display,"User's Id",'pink')

        self.background = Button.BackGroundButton([head_path+r'\default\Title_bar.png'],
                                                  (600,400),(540,400),self.display)

        #Đối tượng kiểm tra error nếu có lỗi
        self.err = False
        self.err_button = Button.TextBox(self.display,"Invalid Id",(540,300),text_c='red',fonts=35)
        self.running = True

    #Vẽ các thành phần
    def draw(self,pos):
        self.background.draw(pos)
        self.back_button.draw(pos)
        self.enter_button.draw(pos)
        self.user_button.draw(pos)
        if self.err:
            self.err_button.draw()

    #Hàm chạy
    #Flag_manager: quản lý state
    #system: App xử lý logic
    def run(self,flag_manager,system,cache=None):
        #Mỗi lần được gọi cần đặt lại running là True
        self.running = True
        while self.running:
            #Bắt vị trí của chuột
            pos = pygame.mouse.get_pos()

            self.display.fill("white")
            #Bắt các sự kiện để truyền vào các nút
            for event in pygame.event.get():
                self.event_handle(event, flag_manager)
                self.enter_button.event_handle(event,pos)
                self.user_button.event_handle(event,pos)
                self.back_button.event_handle(event,pos)

            #Kiểm tra nút enter nếu được active
            if self.enter_button.is_active:
                #reset lại nút để tránh lỗi
                self.enter_button.reset()
                #kiểm tra người dùng nhập id user chưa
                if self.user_button.done:
                    try:
                        #thay đổi user cho backend
                        system.set_user(int(self.user_button.get_value()))
                    except Exception as e:
                        #Nếu lỗi err được tạo
                        print(str(e))
                        self.err = True
                    else:
                        #không lỗi sẽ chuyển state sang màn hình chính
                        flag_manager.change('main')
                        self.err = False
                        self.running = False
                    #reset lại nút user để dùng cho lúc sau
                    self.user_button.reset()
            #Kiểm tra nếu thoát
            if self.back_button.is_active:
                #Dừng màn hình
                self.running = False
                self.back_button.reset()
                #Quay lại màn hình chính
                flag_manager.change("main")
            #Vẽ và cập nhật màn hình
            self.draw(pos)
            pygame.display.flip()