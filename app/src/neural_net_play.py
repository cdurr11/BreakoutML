import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
from game import Game
import os

model = create_model()
model.load_weights('./training_1/checkpoint')
