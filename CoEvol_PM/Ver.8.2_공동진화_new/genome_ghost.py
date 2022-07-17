import numpy as np

class GhostGenome():
    def __init__(self):
        self.fitness = 0
        self.input_size = 10
        self.hidden_layer_size1 = 30
        self.hidden_layer_size2 = 40
        self.hidden_layer_size3 = 15
        self.output_size = 4
        self.w1 = np.random.randn(self.input_size, self.hidden_layer_size1)
        self.w2 = np.random.randn(self.hidden_layer_size1, self.hidden_layer_size2)
        self.w3 = np.random.randn(self.hidden_layer_size2, self.hidden_layer_size3)
        self.w4 = np.random.randn(self.hidden_layer_size3, self.output_size)
        '''
        표준정규분포 난수 매트릭스 어레이 생성
        각 가중치 설정
        9 -> 15 -> 20 -> 10 -> 4
        '''

    def forward(self, input):
        # (m,n) matrix 곱셈 연산
        net = np.matmul(input, self.w1)
        net = self.relu(net)
        net = np.matmul(net, self.w2)
        net = self.relu(net)
        net = np.matmul(net, self.w3)
        net = self.relu(net)
        net = np.matmul(net, self.w4)
        net = self.relu(net)
        return net

    # 목표치가 다범주, 각 범주에 속할 사후확률 제공
    def softmax(self, x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def relu(self,x):
        return x * (x >= 0)

    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))
