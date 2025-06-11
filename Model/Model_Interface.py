import numpy as np


#Interface cho các mô hình AI
class ModelInterface:
    def __init__(self,sigmoid = False,sig_value=1,weight_cre = 0):
        #Dùng Hàm sigmoid hay không (option)
        self.sigmoi = sigmoid
        #Giá trị muốn nhân với hàm sigmoid để đưa về giới hạn chuẩn
        self.sig_value = sig_value
        #Giá trị w khởi tạo
        self.weight_value = weight_cre

    #Hàm hủy sigmoid để đưa label và y_hat về đúng quy chiếu
    def desigmoid(self,value):
        #Thay thế giá trị 0 và giá trị bằng sig_value tránh lỗi khi tính 1/x và log
        inx = np.where(value == 0)
        value[inx] = 0.0000001
        inx = np.where(value==self.sig_value)
        value[inx] -=0.0000001
        value /= self.sig_value
        value = 1/value - 1
        value = 1/value
        #Giới hạn value để tránh overflow khi dùng log
        value = np.clip(value,0.000001,1000000)
        return np.log(value)

    #Hàm sigmoid
    def sigmoid(self,value):
        value = np.clip(value,-60,60)
        return self.sig_value * (1/(1+np.exp(-value)))

    def create_weight(self,size):
        pass

    def train(self, features, label,lamba_reg = 0.005):
        pass

    def test(self,weight,features,label):
        pass

    def calculate(self,weight,features):
        pass