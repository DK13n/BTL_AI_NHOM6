import numpy as np
from typing_extensions import override
from Model.Model_Interface import ModelInterface


#Mô hình hồi quy
class Regress(ModelInterface):
    def __init__(self,sigmoid = False,sig_value=1):
        super().__init__(sigmoid,sig_value)


    #Nạp chồng hàm train
    @override
    def train(self, features, label,lamba_reg = 0.005):
        #Thêm bias và chuẩn hóa dữ liệu về array
        features_ = np.copy(features)
        features_ = list(features_)
        for i in range(len(features_)):
            features_[i] = list(features_[i])
            features_[i].append(1)
        features_ = np.array(features_)
        label = np.array(label)
        #Kiểm tra option sigmoid
        if self.sigmoi:
            #đưa label về hệ quy chiếu cần thiết
            label = self.desigmoid(label)
        #Tính trọng số theo công thức hồi quy
        weight = np.linalg.pinv(features_.T.dot(features_) + lamba_reg*np.eye(features_.shape[1])).dot(features_.T).dot(label)
        return weight


    #Nạp chồng hàm test
    @override
    def test(self, weight, features, label):
        count = 0
        #Thêm bias chuẩn hóa về array
        features_ = np.copy(features)
        features_ = list(features_)
        for i in range(len(features_)):
            features_[i] = list(features_[i])
            features_[i].append(1)
        features_ = np.array(features_)
        weight = np.array(weight)
        label = np.array(label)
        #tính giá trị dự đoán
        value = features_.dot(weight.T)
        if self.sigmoi:
            value = self.sigmoid(value)
        # Sai số
        count += len(value)
        err = np.sum((label - value) ** 2)
        return err, count


    @override
    def calculate(self, weight, features):
        features_ = np.copy(features)
        features_ = list(features_)
        for i in range(len(features_)):
            features_[i] = list(features_[i])
            features_[i].append(1)
        features_ = np.array(features_)
        weight = np.array(weight)
        value = features_.dot(weight.T)
        if self.sigmoi:
            value = self.sigmoid(value)
        return value