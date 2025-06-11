import sys
import pygame

#Class quản lý trạng thái
class StateManager:
    def __init__(self,state,function,state_start,stop_state):
        #Tạo dict đến các trạng thái và functions
        self.state = dict({})

        try:
            for i in range(len(state)):
                self.state[state[i]] = function[i]
        except Exception as e:
            print(f"{e} : Không thể khởi tạo danh sách state")

        #Tạo trạng thái ban đầu và trạng thái kết thúc
        if state_start in self.state and stop_state in self.state:
            #Flag là trạng thái hiện tại
            self.flag = state_start
            self.stop_state = stop_state
        else:
            sys.exit("không tìm thấy state tương ứng")
        self.running = True
        self.last_state = None

    #Hàm thay đổi trạng thái
    def change(self,state):
        if state not in self.state:
            sys.exit(f"Không tồn tại state này: {state}")
        if state == self.stop_state:
            self.running = False
        elif not state is None :
            self.last_state = self.flag
            self.flag = state

    #Hàm chạy các functions của state đang chạy
    def callstate(self,system,cache=None):
        self.state[self.flag].run(self,system,cache)

    #Hàm chạy chương trình
    def run(self,service,cache=None):
        while self.running:
            self.callstate(service,cache)