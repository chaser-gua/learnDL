import numpy as np
import torch
from torch.utils import data
from d2l import torch as d2l

# 产生伪真实的用于训练的数据集
true_w = torch.tensor([2, -3.4])
true_b = 4.2
features, labels = d2l.synthetic_data(true_w, true_b, 1000)


# 利用深度学习框架中的API打乱样本并且获得小批量了
def load_array(data_arrays, batch_size, is_train=True):  #@save
    """构造一个PyTorch数据迭代器"""
    dataset = data.TensorDataset(*data_arrays)
    return data.DataLoader(dataset, batch_size, shuffle=is_train)

batch_size = 10
data_iter = load_array((features, labels), batch_size)


# 利用深度学习框架中的层来定义模型
# nn是神经网络的缩写
from torch import nn

# 定义网络结构,Linear中是全连接层，2和1分别代表输入输出特征形状
net = nn.Sequential(nn.Linear(2, 1))

# 设置参数
net[0].weight.data.normal_(0, 0.01)
net[0].bias.data.fill_(0)

# 定义损失函数，也是直接调用API
loss = nn.MSELoss()

# 优化函数
trainer = torch.optim.SGD(net.parameters(), lr=0.03)

# 最终实现训练
num_epochs = 3
for epoch in range(num_epochs):
    for X, y in data_iter:
        l = loss(net(X) ,y)
        trainer.zero_grad()
        l.backward()
        trainer.step()
    l = loss(net(features), labels)
    print(f'epoch {epoch + 1}, loss {l:f}')

w = net[0].weight.data
print('w的估计误差：', true_w - w.reshape(true_w.shape))
b = net[0].bias.data
print('b的估计误差：', true_b - b)