import pygame

#Interface cho các button
class Button:
    def __init__(self,images,size,center,display,text=None,text_c='black',font=None,fonts=35):
        #Khởi tạo ảnh cho pygame
        self.images = [pygame.image.load(image).convert_alpha() for image in images]
        self.images = [pygame.transform.smoothscale(image,size) for image in self.images]
        #mask để xử lí va chạm
        self.button_mask = pygame.mask.from_surface(self.images[0])
        #Vị trí
        self.center = center
        self.button_rect = self.images[0].get_rect(center=self.center)
        self.display = display
        #Giá trị bool kiểm tra nút kích hoạt
        self.is_active = False
        #Set font cho text của nút
        if font is None:
            self.font = pygame.font.SysFont("Arial", fonts)
        else:
            self.font = pygame.font.SysFont(font, fonts)
        #Text và color
        self.text = text
        self.text_color = text_c

    #vẽ nút
    def draw(self,pos):
        #kiểm tra va chạm để làm nút hover
        hover = self.on_hover(pos)
        self.display.blit(self.images[hover], self.button_rect)
        if not self.text is None:
            text = self.font.render(self.text, True,self.text_color)
            text_rect = text.get_rect(center=self.center)
            self.display.blit(text, text_rect)

    #Reset nút về giá trị khởi tạo
    def reset(self):
        self.is_active = False

    #Hàm trừu tượng xử lí sự kiện
    def event_handle(self,event,pos):
        pass

    #Kiểm tra chuột có trỏ vào nút không
    def on_hover(self,pos):
        if self.button_rect.collidepoint(pos):
            try:
                if self.button_mask.get_at((pos[0] - self.button_rect.x, pos[1] - self.button_rect.y)):
                    return True
            except:
                return False
        return False