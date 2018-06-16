import pandas as pd
import torch
import torch.nn as nn
from torch import autograd


class PolicyNetwork:

    def __init__(self):
        self.model = self.Model()
        # Loss and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.learning_rate)
        #self.optimizer = torch.optim.SGD(self.model.parameters(), lr=learning_rate)

        pass

    def get_action(self,state):
        #convert tensor to numpy array
        actions = self.model.feed_forward(state)
        print(actions)
        #actions = softmax(actions)

        return actions

    def train(self,sates,rewards):

        pass

    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()




    class Model(nn.Module):

        n_features = 120
        n_classes = 2
        layer1_neurons = 50
        layer2_neurons = 30
        learning_rate = .001

        def __init__(self, ):
            super().__init__()
            self.fc1 = nn.Linear(self.n_features, self.layer1_neurons)
            self.fc2 = nn.Linear(self.layer1_neurons, self.layer2_neurons)
            self.fc3 = nn.Linear(self.layer2_neurons, self.n_classes)

            # activiation functions
            self.sigmoid = torch.nn.Sigmoid()
            self.relu = nn.ReLU()

        def feed_forward(self, x):
            out = self.fc1(x)
            out = self.relu(out)
            out = self.fc2(out)
            out = self.relu(out)
            out = self.fc3(out)
            # without softmax
            return out


