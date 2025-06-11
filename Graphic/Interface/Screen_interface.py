import sys
import pygame

#Interface cho screen
class Screen:
    def __init__(self,display,size):
        #lấy size của display
        self.size = size
        self.w = size[0]
        self.h = size[1]
        self.display = display
        self.running = True

    #Hàm xử lý các sự kiện cơ bản
    def event_handle(self,event,flag_manager):
        if event.type == pygame.QUIT:
            flag_manager.change(flag_manager.stop_state)
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                flag_manager.change(flag_manager.last_state)

    #Hàm trừu tượng đưa về các giá trị khởi tạo của display
    def reset(self):
        pass

    #Hàm trừu tượng vẽ các đối tượng trong display
    def draw(self,pos):
        pass

    #Hàm trừu tượng để chạy display
    def run(self,flag_manager,system,cache=None):
        pass