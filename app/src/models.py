import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
from game import Game
import os

checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=0)


model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(6,)))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(2, activation='relu'))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

#observation = (ball_pos_x, ball_pos_y,
#               ball_vel_x, ball_vel_y,
#               paddle_pos_x, paddle_pos_y)

def choose_action(eps, model, state):
    if np.random.random() < eps:
        random_action = np.random.choice(Breakout_Env.action_space)
        return (Breakout_Env.action_space.index(random_action), random_action)
    else:
        # print(state)
        # print([state:state+1])
        # prediction = model.predict(state)

        prediction = np.argmax(model.predict(state))
        # print("prediction", prediction)
        if prediction == 0:
            return (0, 'LEFT')
        else:
            return (1, 'RIGHT')

def generate_episodes(env, number_episodes, model, logging_increment = 100):
    eps = 0.5
    epsilon_decay_factor = 0.999
    discount_factor = 0.95
    rewards = []

    for i in range(number_episodes):
        if i % logging_increment == 0:
            print("episode number {} of {}".format(i, number_episodes))

        s = env.reset()
        eps *= epsilon_decay_factor
        done = False
        total_reward = 0

        while not done:
            action = choose_action(eps, model, s)
            s_prime, reward, done, info = env.step(action[1])
            target = reward + discount_factor * np.max(model.predict(s_prime))
            target_vec = model.predict(s)
            # print(target_vec[0])
            # print(action[0])
            target_vec[0][action[0]] = target
            model.fit(s, target_vec, verbose=0, callbacks = [cp_callback])
            s = s_prime
            total_reward += reward

        rewards.append(total_reward)

    return sum(rewards)/len(rewards)


class Breakout_Env:
    reward_range = (-np.inf, np.inf)
    action_space = ['LEFT', 'RIGHT']
    observation_space = None

    def step(self, action):
        keys = { 'left': action == 'LEFT', 'right': action == 'RIGHT' }
        self.game.time_step(keys)
        current_game_state = self.game.get_game_state()

        if ( current_game_state == 'WON' or current_game_state == 'LOST' ):
            done = True
        else:
            done = False

        reward = 0.0

        if current_game_state == 'WON':
            reward = 1000.0

        if current_game_state == 'LOST':
            reward = -10.0

        if self.game.did_intersect_paddle():
            reward = 10.0

        if self.game.did_intersect_block():
            reward = 0.0

        self.state = np.array([self.game.get_game_state_vector()])

        #return tuple of state, reward, done, auxiliary info for debugging
        return self.state, reward, done, {}


    def reset(self):
        self.game = Game(2,10,60)
        game_state_vector = self.game.get_game_state_vector()
        self.state = np.array([game_state_vector])
        return self.state

    def render(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

if __name__ == '__main__':
    breakout = Breakout_Env()
    print("average reward: ", generate_episodes(breakout, 50, model, logging_increment = 10))
