# 다중 선형 회귀 클래스 선언
import torch
import torch.nn as nn
import torch.nn.functional as F

# 데이터 생성
x_train = torch.FloatTensor([[73, 80, 75],
                            [93, 88, 93],
                            [89, 91, 90],
                            [96, 98, 100],
                            [73, 66, 70]
                             ])
y_train = torch.FloatTensor([[152], [185], [180], [196], [142]])

# class 생성


class MultivariateLinearRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(3, 1)  # input 3 output 1

    def forward(self, x):
        return self.linear.forward(x)


# model 정의
model = MultivariateLinearRegressionModel()

# optimizer
optimizer = torch.optim.SGD(model.parameters(), lr=1e-5)

# train
epochs_num = 2000
for epoch in range(epochs_num + 1):

    # model
    prediction = model(x_train)

    # loss
    loss = F.mse_loss(prediction, y_train)

    # loss 개선
    optimizer.zero_grad()  # 기울기를 0으로 초기화
    loss.backward()       # loss 함수를 미분하여 기울기 계산
    optimizer.step()      # w , b 를 업데이트

    if epoch % 100 == 0:
        print("Epoch : {:4d}/{} loss : {:.6f}".format(
            epoch, epochs_num, loss.item()
        ))

new_var = torch.FloatTensor([[73, 82, 72]])
pred_y = model(new_var)
print(f"훈련 후 입력이 {new_var} 에측값 : {pred_y}")


'''
Epoch :    0/2000 loss : 35272.894531
Epoch :  100/2000 loss : 1.027056
Epoch :  200/2000 loss : 1.003166
Epoch :  300/2000 loss : 0.980439
Epoch :  400/2000 loss : 0.958805
Epoch :  500/2000 loss : 0.938189
Epoch :  600/2000 loss : 0.918569
Epoch :  700/2000 loss : 0.899861
Epoch :  800/2000 loss : 0.882048
Epoch :  900/2000 loss : 0.865069
Epoch : 1000/2000 loss : 0.848879
Epoch : 1100/2000 loss : 0.833453
Epoch : 1200/2000 loss : 0.818718
Epoch : 1300/2000 loss : 0.804671
Epoch : 1400/2000 loss : 0.791238
Epoch : 1500/2000 loss : 0.778437
Epoch : 1600/2000 loss : 0.766208
Epoch : 1700/2000 loss : 0.754514
Epoch : 1800/2000 loss : 0.743348
Epoch : 1900/2000 loss : 0.732664
Epoch : 2000/2000 loss : 0.722441
훈련 후 입력이 tensor([[73., 82., 72.]]) 에측값 : tensor([[149.6103]], grad_fn=<AddmmBackward0>)
'''
