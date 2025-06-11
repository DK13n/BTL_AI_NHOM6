import sys
import pygame
import numpy
from typing_extensions import override
from Graphic.Interface.Button_Interface import Button

#Tạo class button bắt sự kiện bấm chuột
class ClickButton(Button):
    def __init__(self,images,size,center,display,text=None,text_c='black',font="Arial",fonts=35):
        super().__init__(images,size,center,display,text,text_c,font,fonts)

    #override event_handle để xử lý event
    def event_handle(self,event,pos):
        if self.on_hover(pos):
            #kích hoạt khi bấm chuột, event.button = 1 nếu bấm chuột trái
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.is_active = True


#Tạo button bắt sự kien nhập dữ liệu
class InputButton(Button):
    def __init__(self, images, size, center, display, text='', text_c='black', font=None,fonts=35):
        super().__init__(images, size, center, display, text, text_c, font,fonts)
        #default_text để lưu trữ text hiển thị mặc định
        self.default_text = text
        #flag_text để check xem người dùng đã gõ vào chưa
        self.flag_text = False
        #Giá trị bool kiểm tra dữ liệu có thay đổi hay không
        self.is_changed = False
        #Giá trị lưu trạng thái cũ của dữ liệu text
        self.last_text = text
        #done để check xem có dữ liệu trong input chưa
        self.done = False

    @override
    def draw(self,pos):
        #Hàm draw này override để vẽ thêm các đối tượng khác
        hover = (self.on_hover(pos) or self.is_active)
        self.display.blit(self.images[hover], self.button_rect)
        if not self.text is None:
            text = self.font.render(self.text, True,self.text_color)
            text_rect = text.get_rect(center=self.center)
            self.display.blit(text, text_rect)

    #Hàm trả lại về giá trị khởi tạo
    def reset(self):
        super().reset()
        self.text = self.default_text
        self.flag_text = False
        self.done = False

    #override hàm bắt sự kiện
    @override
    def event_handle(self,event,pos):
        # kiểm tra logic

        #Nếu text đã có nhưng chưa done
        if self.text and not self.done and self.flag_text:
            self.done = True
        #Nếu text chưa có mà vẫn còn active
        elif not self.text and self.is_active:
            self.done = False
        #Nếu text chưa có mà cũng chưa active thì trả về giá trị ban đầu
        elif not self.text and not self.is_active:
            self.text = self.default_text
            self.flag_text = False

        #Bắt sự kiện bấm chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Bấm chuột trái
            if event.button == 1:
                if self.on_hover(pos):
                    self.is_active = True
                    #Nếu nút chưa được nhấn, bắt đầu cho nhấn mà đã active
                    if not self.flag_text:
                        self.text = ''
                        self.flag_text = True
                #Nếu bấm vào vùng khác nút thì nút tự hủy active
                else:
                    self.is_active = False
            #Cuộn chuột cũng sẽ hủy active
            elif event.button==4 or event.button==5:
                self.is_active = False

        #Bắt sự kiện bấm nút input
        elif event.type == pygame.KEYDOWN:
            if self.flag_text:
                if self.is_active:
                    if event.key == pygame.K_RETURN:
                        self.is_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text = self.text + event.unicode

        self.is_changed = not (self.text == self.last_text)
        if self.is_changed:
            self.last_text = self.text


    #Lấy text hiện tại
    def get_value(self):
        #Chỉ lấy text khi khác default_text
        if self.text != self.default_text:
            return self.text
        else:
            return ''

#Tạo Class chỉ để vẽ lên màn hình
class BackGroundButton(Button):
    def __init__(self, images, size, center, display, text=None, text_c='black', font=None,fonts=35):
        super().__init__(images, size, center, display, text, text_c, font,fonts)

    @override
    def draw(self,pos):
        self.display.blit(self.images[0], self.button_rect)
        if not self.text is None:
            text = self.font.render(self.text, True,self.text_color)
            text_rect = text.get_rect(center=self.center)
            self.display.blit(text, text_rect)

    def change_text(self,text):
        self.text = text


#Class để tạo chữ không cần khung
class TextBox:
    def __init__(self,display,text,location,center=False,left=False,right=False,text_c = "black",font=None,fonts=25):
        self.display = display
        self.text = text
        self.text_color = text_c
        self.location=location

        #Chọn căn lề cho text
        if not (center and left and right):
            center = True
        elif (center and left) or (left and right) or (center and right):
            print("Can chỉnh không hợp lệ! Đưa về mặc định")
            center = True
            left,right = False, False
        self.center = center
        self.left = left
        self.right = right

        #Kiểu mặc định nếu không có font
        if font is None:
            self.font = pygame.font.SysFont("Arial", fonts)
        else:
            self.font = pygame.font.SysFont(font, fonts)
        self.height = self.font.get_height()

    #Vẽ chữ lên màn hình
    def draw(self):
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.location)
        if self.left:
            text_rect = text.get_rect(topleft=self.location)
        elif self.right:
            text_rect = text.get_rect(topright=self.location)
        self.display.blit(text, text_rect)