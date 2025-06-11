import numpy as np
from typing_extensions import override
from Model.Model_Interface import ModelInterface


class GradientDescent(ModelInterface):
    def __init__(self,sigmoid=False,sig_value=1,weight_cre=0):
        super().__init__(sigmoid,sig_value,weight_cre)


    @override
    def create_weight(self,size):
        weight = np.zeros(size)+self.weight_value
        return weight

    @override
    def train(self, features, label,weight=None, learning_rate=0.01,epochs = 300):
        #Thêm bias và chuẩn hóa dữ liệu về array
        features_ = np.copy(features)
        features_ = list(features_)
        for i in range(len(features_)):
            features_[i] = list(features_[i])
            features_[i].append(1)
        features_ = np.array(features_)
        label = np.array(label)

        #Tạo trọng số bắt đầu bằng 0 nếu như không truyền trọng số
        if weight is None or len(weight)!=len(features_[0]):
            weight = self.create_weight(len(features_[0]))
        else:
            weight = np.array(weight)
        #Số lượng mẫu
        size = len(features_)

        #Lặp nhiều lần thực hiện gradient descent để hội tụ về cực tiểu
        for epoch in range(epochs):
            val = features_.dot(weight.T)
            if self.sigmoi:
                val = self.sigmoid(val)
            grad = (2/size) * features_.T.dot((val-label))
            weight -= learning_rate*grad
        return weight


    @override
    def test(self,weight,features,label):

        # Thêm bias chuẩn hóa về array
        features_ = np.copy(features)
        features_ = list(features_)
        for i in range(len(features_)):
            features_[i] = list(features_[i])
            features_[i].append(1)
        features_ = np.array(features_)
        weight = np.array(weight)
        label = np.array(label)

        # tính giá trị dự đoán
        value = (features_.dot(weight.T))
        if self.sigmoi:
            value = self.sigmoid(value)

        # Sai số
        err =list((label-value)**2)
        return err


    @override
    def calculate(self,weight,features):
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
