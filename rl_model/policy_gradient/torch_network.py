import pandas as pd
import torch
import torch.nn as nn
from torch import autograd
import numpy as np
from torch.autograd import Variable
from torch.distributions import Categorical
from torch.distributions import Bernoulli
import torch.nn.functional as F

class PolicyNetwork:

    def __init__(self):
        self.model = self.NeuralNet()
        self.model = self.model.double()
        # Loss and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.learning_rate)
        #self.optimizer = torch.optim.SGD(self.model.parameters(), lr=learning_rate)


        pass

    def get_action(self,state):
        #returns a torch tensor
        state = torch.from_numpy(state)
        #actions = self.model(state)
        probs = self.model(state)
        # Note that this is equivalent to what used to be called multinomial
        m = Categorical(probs)
        action = m.sample()

        return action

    def train(self, s, a, r):
        self.optimizer.zero_grad()

        states = torch.from_numpy(s)
        actions = a
        rewards = torch.from_numpy(r)

        for i in range (len(states)):
            state = states[i]
            action = actions[i]
            reward = rewards[i]

            probs = self.model(state)
            m = Categorical(probs)
            loss = -m.log_prob(action.double()) * reward
            loss.backward()


        self.optimizer.step()
        return(loss.item())
        pass

    class NeuralNet(nn.Module):

        n_features = 120
        n_classes = 2
        layer1_neurons = 50
        layer2_neurons = 30
        learning_rate = .001

        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(self.n_features, self.layer1_neurons)
            self.fc2 = nn.Linear(self.layer1_neurons, self.layer2_neurons)
            self.fc3 = nn.Linear(self.layer2_neurons, self.n_classes)


            torch.set_default_tensor_type('torch.DoubleTensor')

        def forward(self, x):
            out = self.fc1(x)
            out = F.relu(out)
            out = self.fc2(out)
            out = F.relu(out)
            out = self.fc3(out)

            return F.softmax(out)


