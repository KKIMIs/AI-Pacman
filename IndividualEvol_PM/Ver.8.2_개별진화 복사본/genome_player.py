import numpy as np

class p_genome():
    def __init__(self):
        self.fitness = 0
        self.input_size = 9
        self.hidden_layer_size1 = 20
        self.hidden_layer_size2 = 35
        self.hidden_layer_size3 = 15
        self.output_size = 4
        # 표준정규분포(평균0 표준편차 1) 난수 (m,n) matrix array 생성
        self.w1 = np.random.randn(self.input_size, self.hidden_layer_size1)
        self.w2 = np.random.randn(self.hidden_layer_size1, self.hidden_layer_size2)
        self.w3 = np.random.randn(self.hidden_layer_size2, self.hidden_layer_size3)
        self.w4 = np.random.randn(self.hidden_layer_size3, self.output_size)

        '''
        표준정규분포 난수 매트릭스 어레이 생성
        각 가중치 설정
        9 -> 20 -> 30 -> 15 -> 4
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
        net = self.sigmoid(net)
        return net

    # 목표치가 다범주, 각 범주에 속할 사후확률 제공
    def softmax(self, x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def relu(self,x):
        return x * (x >= 0)

    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))
