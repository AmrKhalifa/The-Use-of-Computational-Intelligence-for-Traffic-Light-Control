import numpy as np
import tensorflow as tf


class PolicyNetwork:

    n_features = 120
    n_classes = 2
    layer1_neurons = 30
    layer2_neurons = 10
    learning_rate = .01

    x = tf.placeholder(tf.float64, shape = [None, n_features])
    _y = tf.placeholder(tf.float64, shape = [None, n_classes])
    
    sess = tf.Session()

    weights = {

        'l1w': tf.Variable(tf.truncated_normal([n_features, layer1_neurons],dtype=tf.float64)),
        'l2w': tf.Variable(tf.truncated_normal([layer1_neurons, layer2_neurons],dtype=tf.float64)),
        'output_w': tf.Variable(tf.truncated_normal([layer2_neurons, n_classes],dtype=tf.float64))
    }

    biases = {
        'l1b': tf.Variable(tf.truncated_normal([layer1_neurons],dtype=tf.float64)),
        'l2b': tf.Variable(tf.truncated_normal([layer2_neurons],dtype=tf.float64)),
        'output_b': tf.Variable(tf.truncated_normal([n_classes],dtype=tf.float64))
    }

    def __init__(self):
        pass

    @classmethod
    def initialize_variables(cls):

        global_initializer = tf.global_variables_initializer()
        cls.sess.run(global_initializer)
        local_initializer = tf.local_variables_initializer()
        cls.sess.run(local_initializer)

        pass


    @classmethod
    def feed_forward(cls,x):
        l1 = tf.add(tf.matmul(x, cls.weights['l1w']), cls.biases['l1b'])
        l1 = tf.nn.sigmoid(l1)

        l2 = tf.add(tf.matmul(l1, cls.weights['l2w']), cls.biases['l2b'])
        l2 = tf.nn.sigmoid(l2)

        network_output = tf.add(tf.matmul(l2, cls.weights['output_w']), cls.biases['output_b'])

        outputs_softmax = tf.nn.softmax(network_output)
        #tf.reset_default_graph()
        return network_output,outputs_softmax

    @classmethod
    def train(cls,s,a,r):
        output, output_softmax = cls.feed_forward(s)
        neg_log_prob = tf.nn.softmax_cross_entropy_with_logits(logits=output, labels=cls._y)
        loss = tf.reduce_mean(neg_log_prob * r)
        train_op = tf.train.AdamOptimizer(cls.learning_rate).minimize(loss)
       
        cls.sess.run(train_op, feed_dict={cls.x: s, cls._y: a})
        theLoss = cls.sess.run(loss, feed_dict={cls.x: s, cls._y: a})
        sess.get_default_graph().finalize()
        return theLoss


    @classmethod
    def get_output(cls,input):
        y = cls.feed_forward(cls.x)
        output1,output2 = cls.sess.run(y,feed_dict = {cls.x:input})
        return output1,output2


    @classmethod
    def close_session(cls):
        cls.sess.close()