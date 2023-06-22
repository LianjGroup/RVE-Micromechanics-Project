# UNFINISHED: I am unsure about how to continue and output results
# based on video: WGAN implementation from scratch

# FIRST ONE based on article
# Tensorflow / Keras
from tensorflow import keras # for building Neural Networks
#print('Tensorflow/Keras: %s' % keras.__version__) # print version
from keras.models import Sequential # for assembling a Neural Network model
from keras.layers import Dense # adding layers to the Neural Network model
#from tensorflow.keras.utils import plot_model # for plotting model diagram
from plot_model import plot_model

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

# Data manipulation
import numpy as np # for data manipulation
print('numpy: %s' % np.__version__) # print version
import pandas as pd # for data manipulation
print('pandas: %s' % pd.__version__) # print version
import math # for generating real data (points on a circle in this case)

# Visualization
import matplotlib 
import matplotlib.pyplot as plt # or data visualizationa
print('matplotlib: %s' % matplotlib.__version__) # print version
import graphviz # for showing model diagram
print('graphviz: %s' % graphviz.__version__) # print version
import plotly
import plotly.express as px # for data visualization
print('plotly: %s' % plotly.__version__) # print version


# Other utilities
import sys
import os

# Assign main directory to a variable
main_dir = os.path.dirname(sys.path[0])
#print(main_dir)

import torch
import torch.nn as nn


'''SET UP MODELS USING PYTORCH'''
class Discriminator(nn.Module):
    def __init__(self, in_features):
        super().__init__()
        self.disc = nn.Sequential(
            nn.ReLU(in_features, 32), # in_features are 2
            nn.ReLU(32, 16),
            nn.Sigmoid(16, 1),
        )
    
    def forward(self, x):
        return self.disc(x)

class Generator(nn.Module):
    def __init__(self, z_dim, in_features):
        super().__init__()
        self.gen = nn.Sequential(
            nn.ReLU(z_dim, 32), # z dim is 3
            nn.ReLU(32, 16),
            nn.Linear(16, in_features), # in_features = 2
        )

    def forward(self, x):
        return self.gen(x)
    


''' SET UP INPUT FUNCTIONS '''
# A function to get coordinates of points on the circle's circumference
def PointsInCircum(r,n=100):
    return [(math.cos(2*math.pi/n*x)*r,math.sin(2*math.pi/n*x)*r) for x in range(0,n+1)] 
    #returns x & y coordinates of points on circumference
    # n = number of points

# Save coordinates of a set of real points making up a circle with radius=2
circle=np.array(PointsInCircum(r=2,n=1000))

# Draw a chart
plt.figure(figsize=(15,15), dpi=400) # dpi = dot pixels per inch
plt.title(label='Real circle to be learned by the GAN generator', loc='center')
plt.scatter(circle[:,0], circle[:,1], s=5, color='black')
plt.show()
print("Input plot done")

def real_samples(n):
    
    # Samples of real data
    X = circle[np.random.choice(circle.shape[0], n, replace=True), :]

    # Class labels: labels are 1 because this is real data
    y = np.ones((n, 1)) # n by 1 matrix --> n rows, 1 col of ones
    return X, y

def latent_points(latent_dim, n):
    
    # Generate points in the latent space
    latent_input = np.random.randn(latent_dim * n)
    
    # Reshape into a batch of inputs for the network
    latent_input = latent_input.reshape(n, latent_dim) # reshape to n rows and latent_dim cols
    return latent_input

def fake_samples(generator, latent_dim, n):
    
    # Generate points in latent space
    latent_output = latent_points(latent_dim, n)
    
    # Predict outputs (i.e., generate fake samples)
    X = generator.predict(latent_output)
    
    # Create class labels --> labes are marked 0 because this should be identified as fake
    y = np.zeros((n, 1))
    return X, y


''' HYPERPARAMETERS '''
device = "cuda" if torch.cuda.is_available() else "cpu"
learning_rate = 5e-5
z_dim = 3
in_features = 2
batch_size = 64
num_epochs = 5
critic_iterations = 5
weight_clip = 0.01

#x_fake, y_fake = fake_samples(g_model, latent_dim, half_batch)

x_gen_input = latent_points(z_dim, batch_size)
y_gan = np.ones((batch_size, 1))



disc = Discriminator(in_features).to(device)
gen = Generator(z_dim, in_features).to(device)
fixed_noise = torch.randn((batch_size, z_dim)).to(device)
#transforms = transforms.Compose(
#    [transforms.ToTensor(), transforms.Normalize((0.5), (0.5))]
#)
opt_disc = optim.RMSprop(disc.parameters(), lr=learning_rate)
opt_gen = optim.RMSprop(gen.parameters(), lr=learning_rate)
#criterion = nn.CrossEntropyLoss()

writer_fake = SummaryWriter(f"runs/GAN_circle/fake")
writer_real = SummaryWriter(f"runs/GAN_circle/real")
step = 0
n = 1000

gen.train()
disc.train()

for epoch in range(num_epochs):
    
    x_real, y_real = real_samples(batch_size/2)
    

    for _ in range(critic_iterations):
        noise = latent_points(z_dim, batch_size)
        x_fake = gen(noise)
        critic_real = disc(x_real).reshape(-1)
        critic_fake = disc(x_fake).reshape(-1)
        loss_critic = -(torch.mean(critic_real) - torch.mean(critic_fake)) #trying to maximize inner function, optimization agorithms are for minimizing so put -ve sign
        disc.zero_grad()
        loss_critic.backward(retain_graph=True)
        opt_disc.step()

        for p in disc.parameters():
            p.data.clamp_(-weight_clip, weight_clip)
    
    # Train Generator: min -E[ciritic(gen_fake)]
    output = disc(x_fake).reshape(-1)
    loss_gen = -torch.mean(output)
    gen.zero_grad()
    loss_gen.backward()
    opt_gen.step()

    print(
                f"Epoch [{epoch}/{num_epochs}] \
                Loss D: {loss_critic:.4f}, loss G: {loss_gen:.4f}"
            )

    with torch.no_grad():
                fake = gen(fixed_noise)
                data = x_real
                img_grid_fake = torchvision.utils.make_grid(fake, normalize=True)
                img_grid_real = torchvision.utils.make_grid(data, normalize=True)
                step += 1







