import App.Service as Service

#Class quản lý service và state manager
class App:
    def __init__(self,state_sys, path, genres):
        self.state_manager = state_sys
        self.service = Service.App(path, genres)
        self.cache = dict({})

    #Chạy app
    def run(self):
        self.state_manager.run(self.service)
        #Push dữ liệu lại sau khi dừng
        self.service.push_data()

