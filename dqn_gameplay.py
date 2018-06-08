import numpy as np
import pandas as pd
import tensorflow as tf

##np.random.seed(1)
##tf.set_random_seed(1)

class DQN_gameplay:
    def __init__(self,
            #n_actions,
            #state,
            n_features = 10,
            learning_rate=0.01,
            reward_decay=0.9,
            e_greedy=0.1, #0.9
            replace_target_iter=300,
            memory_size=500,
            batch_size=32,
            e_greedy_increment=None,
            output_graph=False,
    ):
        self.action_space = ['hp', 'attack', 'deffence', 'speed']
        self.n_actions = len(self.action_space)#n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max

        # total learning step
        self.learn_step_counter = 0
        # initialize zero memory [s, a, r, s_]
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))
        # consist of [target_net, evaluate_net]
        self._build_net()
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]

        self.sess = tf.Session()
##        if output_graph:
##            # $ tensorboard --logdir=logs
##            # tf.train.SummaryWriter soon be deprecated, use following
##            tf.summary.FileWriter("logs/", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())
        self.cost_his = []
        self.state_receive = [0,0,0,0,0,0,0,0,0]
        #print(state.shape,'state_shape')
		
    def _build_net(self):
        self.network_name = 'best_commander'
        self.s = tf.placeholder(tf.float32, [1,9], name=self.network_name)
        c_names, n_l1, w_initializer, b_initializer = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 10, \
                tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)  # config of layers
        #layer_name = 'fcn1'; hiddens = 32 ; dim = 8
        #self.ip = tf.add(state,self.b4,name=self.network_name + '_'+layer_name+'_ips')
        #self.op1 = tf.nn.relu(self.ip4,name=self.network_name + '_'+layer_name+'_activations')
        w1 = tf.get_variable('w1', [9, 4], initializer=w_initializer, collections=c_names)
        b1 = tf.get_variable('b1', [1, 4], initializer=b_initializer, collections=c_names)
        self.op1 = tf.nn.relu(tf.matmul(self.s, w1) + b1)
        #self.s = tf.placeholder(tf.float32, [None, self.n_features], name=self.network_name)  # input

        print('dqn is fine!')
	
	
    def choose_action(self, observation):
        # to have batch dimension when feed into tf placeholder
        observation1 = np.array(observation)[np.newaxis, :]
        action=[]
        for i in range(2):
            if np.random.uniform() < self.epsilon:
                # forward feed the observation and get q value for every actions
    ##            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})
    ##            action = np.argmax(actions_value)
                action.append(0)
            else:
                action.append(np.random.randint(0, self.n_actions))
        state = np.array(self.state_receive)[np.newaxis, :]
        print(self.sess.run(self.op1, feed_dict={self.s: state}),'fcn_output')
        return action

