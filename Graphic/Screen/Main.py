import Graphic.Interface.Screen_interface as si
import pygame
import Graphic.Component.Button as Button

#Header cho đường dẫn nút bấm
head_path = r'Graphic\Assets\button'

#Màn hình chính
class Main(si.Screen):
    def __init__(self,display,size):
        super().__init__(display,size)
        #Các nút chức năng khác
        self.button_list =dict({
            "recommend" : Button.ClickButton([head_path+r'\default\Title_button.png',head_path+r'\hover\Title_button.png'],
                                             (200,100),(270,151),self.display,"Reccomend"),
            "rate" : Button.ClickButton([head_path+r'\default\Title_button.png',head_path+r'\hover\Title_button.png'],
                                             (200,100),(270,317),self.display,"Rating Movies"),
            "Change_user" : Button.ClickButton([head_path+r'\default\Title_button.png',head_path+r'\hover\Title_button.png'],
                                             (200,100),(270,483),self.display,"Change User")
        })
        self.back_button = Button.ClickButton([head_path+r'\default\Title_button.png',head_path+r'\hover\Title_button.png'],
                                             (200,100),(270,649),self.display,"Quit")
        self.user_id_bg = Button.BackGroundButton([head_path+r'\default\titlebar_small.png'],
                                             (400,100),(810,151),self.display,"User Id: ",'pink')
        self.text_bg = Button.BackGroundButton([head_path+r'\default\Title_bar.png'],
                                             (400,478),(810,460),self.display)
        self.list_weight = [
            Button.TextBox(self.display,"Action: ",(625,244),left=True,text_c="pink"),
            Button.TextBox(self.display,"Adventure: ",(625,282),left=True,text_c="pink"),
            Button.TextBox(self.display,"Animation: ",(625,320),left=True,text_c="pink"),
            Button.TextBox(self.display,"Children: ",(625,358),left=True,text_c="pink"),
            Button.TextBox(self.display,"Comedy: ",(625,396),left=True,text_c="pink"),
            Button.TextBox(self.display,"Crime: ",(625,434),left=True,text_c="pink"),
            Button.TextBox(self.display,"Documentary: ",(625,472),left=True,text_c="pink"),
            Button.TextBox(self.display,"Drama: ",(625,510),left=True,text_c="pink"),
            Button.TextBox(self.display,"Fantasy: ",(625,548),left=True,text_c="pink"),
            Button.TextBox(self.display,"Film-Noir: ",(625,586),left=True,text_c="pink"),
            Button.TextBox(self.display,"Horror: ",(860,244),left=True,text_c="pink"),
            Button.TextBox(self.display,"Musical: ",(860,282),left=True,text_c="pink"),
            Button.TextBox(self.display,"Mystery: ",(860,320),left=True,text_c="pink"),
            Button.TextBox(self.display,"Romance: ",(860,358),left=True,text_c="pink"),
            Button.TextBox(self.display,"Sci-Fi: ",(860,396),left=True,text_c="pink"),
            Button.TextBox(self.display,"Thriller: ",(860,434),left=True,text_c="pink"),
            Button.TextBox(self.display,"War: ",(860,472),left=True,text_c="pink"),
            Button.TextBox(self.display,"Western: ",(860,510),left=True,text_c="pink"),
            Button.TextBox(self.display,"IMAX: ",(860,548),left=True,text_c="pink"),
            Button.TextBox(self.display,"Bias: ",(860,586),left=True,text_c="pink"),
            Button.TextBox(self.display, "User's Weight", (810, 650), center=True, text_c="pink",fonts=30),
        ]
        self.listText = ["Action: ","Adventure: ","Animation: ","Children: ","Comedy: ",
                         "Crime: ","Documentary: ","Drama: ","Fantasy: ","Film-Noir: ",
                         "Horror: ","Musical: ","Mystery: ","Romance: ","Sci-Fi: ",
                         "Thriller: ","War: ","Western: ","IMAX: ","Bias: ",]

    #Đưa về giá trị khởi tạo
    def reset(self):
        self.back_button.reset()
        for but in self.button_list.values():
            but.reset()

    #Vẽ các thành phần trong display
    def draw(self,pos):
        self.back_button.draw(pos)
        self.user_id_bg.draw(pos)
        self.text_bg.draw(pos)
        for weight in self.list_weight:
            weight.draw()
        for button in self.button_list.values():
            button.draw(pos)

    # Hàm chạy
    # Flag_manager: quản lý state
    # system: App xử lý logic
    def run(self,flag_manager,system,cache=None):
        # Mỗi lần được gọi cần đặt lại running là True
        self.running = True
        #Lấy các thông tin trọng số từ system
        user_w = system.get_userw()
        for i in range(len(user_w)):
            self.list_weight[i].text = f'{self.listText[i]}{user_w[i]:.3f}'
        self.user_id_bg.text=f"User's ID: {system.user}"
        while self.running:
            # Bắt vị trí của chuột
            pos = pygame.mouse.get_pos()
            self.display.fill("white")
            #Bắt các sự kiện để truyền vào các nút
            for event in pygame.event.get():
                self.event_handle(event,flag_manager)
                self.back_button.event_handle(event,pos)
                for button in self.button_list:
                    current_button = self.button_list[button]
                    current_button.event_handle(event,pos)
                    #kiểm tra các nút chức năng có được click hay không
                    if current_button.is_active:
                        #Nếu có bất kỳ nút nào được bấm liền dừng và chuyển trạng thái
                        self.running = False
                        flag_manager.change(button)
            # Kiểm tra nếu thoát
            if self.back_button.is_active:
                #Dừng màn hình và chuyển trạng thái
                self.running = False
                flag_manager.change("quit")
            #Vẽ và cập nhật màn hình
            self.draw(pos)
            pygame.display.flip()
        #Reset màn hình
        self.reset()