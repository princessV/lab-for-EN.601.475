import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.autograd import Variable
from torchvision import datasets, transforms


##TO-DO: Import data here:
transform = transforms.Compose([transforms.ToTensor(),
                               transforms.Normalize(mean=[0.5,0.5,0.5],std=[0.5,0.5,0.5])])

data_train = datasets.MNIST(root = "./data/",
                            transform=transform,
                            train = True,
                            download = True)

data_test = datasets.MNIST(root="./data/",
                           transform = transform,
                           train = False)

data_loader_train = torch.utils.data.DataLoader(dataset=data_train,
                                                batch_size = 64,
                                                shuffle = True,
                                                 num_workers=2)

data_loader_test = torch.utils.data.DataLoader(dataset=data_test,
                                               batch_size = 64,
                                               shuffle = True,
                                                num_workers=2)

##


##TO-DO: Define your model:
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(1, 6, 3, padding=1)
        self.conv2 = nn.Conv2d(6, 16, 3, padding=1)

        self.fc1 = nn.Linear(7 * 7 * 16, 400)
        self.fc2 = nn.Linear(400, 120)
        self.fc3 = nn.Linear(120, 10)
        ##Define layers making use of torch.nn functions:
    
    def forward(self, x):
        ##Define how forward pass / inference is done:
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, 7 * 7 * 16)
        x = F.relu(self.fc1(x))
        x = F.dropout(F.relu(self.fc2(x)), p=0.5)
        x = self.fc3(x)
        return x
        #return out #return output


my_net = Net()
print(my_net)


##TO-DO: Train your model:
cost = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(my_net.parameters())

iterations = 5
for i in range(iterations):
    print("Epoch {}/{}".format(i, iterations))
    print("-" * 10)

    running_loss = 0.0
    running_correct = 0
    for data in data_loader_train:
        X_train, y_train = data
        X_train, y_train = Variable(X_train), Variable(y_train)
        outputs = my_net.forward(X_train)
        _, predictions = torch.max(outputs.data, 1)
        optimizer.zero_grad()

        loss = cost(outputs, y_train)
        loss.backward()
        optimizer.step()
        # ?
        running_loss += loss.data[0]
        running_correct += torch.sum(predictions == y_train.data)


    testing_correct = 0
    for data in data_loader_test:
        X_test, y_test = data
        X_test, y_test = Variable(X_test), Variable(y_test)
        outputs = my_net.forward(X_test)
        _, predictions = torch.max(outputs.data, 1)
        testing_correct += torch.sum(predictions == y_test.data)

    print("Loss is:{:.4f}, Train Accuracy is:{:.4f}%, Test Accuracy is:{:.4f}".format(running_loss / len(data_train),
                                                                                      100 * running_correct / len(
                                                                                          data_train),
                                                                                      100 * testing_correct / len(
                                                                                          data_test)))
    print('=' * 10)

torch.save(my_net.state_dict(), 'model.pkl')
