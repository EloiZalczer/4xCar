#!/usr/bin/python

import torch
import torch.nn as nn
import torch.nn.functional as F

class DeepPicar(nn.Module):
    def __init__(self):
        super(DeepPicar, self).__init__()

        self.conv1 = nn.Conv2d(3, 24, 5, stride=2, bias=True)
        self.conv2 = nn.Conv2d(24, 36, 5, stride=2, bias=True)
        self.conv3 = nn.Conv2d(36, 48, 5, stride=2, bias=True)
        self.conv4 = nn.Conv2d(48, 64, 3, stride=1, bias=True)
        self.conv5 = nn.Conv2d(64, 64, 3, stride=1, bias=True)

        self.fc1 = nn.Linear(1152, 1164)
        self.fc2 = nn.Linear(1164, 100)
        self.fc3 = nn.Linear(100, 50)
        self.fc4 = nn.Linear(50, 10)
        self.fc5 = nn.Linear(10, 1)

    def forward(self, x):
        y = F.relu(self.conv1(x))
        # print("After conv1 : ", y)
        y = F.relu(self.conv2(y))
        # print("After conv2 : ", y)
        y = F.relu(self.conv3(y))
        # print("After conv3 : ", y)
        y = F.relu(self.conv4(y))
        # print("After conv4 : ", y)
        y = F.relu(self.conv5(y))
        # print("After conv5 : ", y)

        y = y.view(-1, 1152)
        # print("After view : ", y.shape)

        y = F.dropout(F.relu(self.fc1(y)))
        # print("After fc1 : ", y)
        y = F.dropout(F.relu(self.fc2(y)))
        # print("After fc2 : ", y)
        y = F.dropout(F.relu(self.fc3(y)))
        # print("After fc3 : ", y)
        y = F.dropout(F.relu(self.fc4(y)))
        # print("After fc4 : ", y)
        y = self.fc5(y)
        # print("After fc5 : ", y)

        return torch.mul(torch.atan(y), 2)