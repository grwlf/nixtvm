""" Neural Network.

A 2-Hidden Layers Fully Connected Neural Network (a.k.a Multilayer Perceptron)
implementation with TensorFlow. This example is using the MNIST database
of handwritten digits (http://yann.lecun.com/exdb/mnist/).

This example is using TensorFlow layers, see 'neural_network_raw' example for
a raw implementation with variables.

Links:
    [MNIST Dataset](http://yann.lecun.com/exdb/mnist/).

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
"""

from __future__ import print_function

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=False)

import tensorflow as tf

# Parameters
learning_rate = 0.1
num_steps = 1000
batch_size = 128
display_step = 100

# Network Parameters
n_hidden_1 = 256 # 1st layer number of neurons
n_hidden_2 = 256 # 2nd layer number of neurons
num_input = 784 # MNIST data input (img shape: 28*28)
num_classes = 10 # MNIST total classes (0-9 digits)



# Define the model function (following TF Estimator Template)
def model_fn(features, labels, mode):
  # TF Estimator input is a dict, in case of multiple inputs
  x = features['images']
  # Hidden fully connected layer with 256 neurons
  layer_1 = tf.layers.dense(x, n_hidden_1)
  # Hidden fully connected layer with 256 neurons
  layer_2 = tf.layers.dense(layer_1, n_hidden_2)
  # Output fully connected layer with a neuron for each class
  logits = tf.layers.dense(layer_2, num_classes)

  # Predictions
  pred_classes = tf.argmax(logits, axis=1)
  pred_probas = tf.nn.softmax(logits)

  # If prediction mode, early return
  if mode == tf.estimator.ModeKeys.PREDICT:
    return tf.estimator.EstimatorSpec(
        mode=mode,
        predictions=pred_classes)

  # Define loss and optimizer
  loss_op = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(
    logits=logits, labels=tf.cast(labels, dtype=tf.int32)))
  optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
  train_op = optimizer.minimize(loss_op,
                                global_step=tf.train.get_global_step())

  # Evaluate the accuracy of the model
  acc_op = tf.metrics.accuracy(labels=labels, predictions=pred_classes)

  # TF Estimators requires to return a EstimatorSpec, that specify
  # the different ops for training, evaluating, ...
  return tf.estimator.EstimatorSpec(
    mode=mode,
    predictions=pred_classes,
    loss=loss_op,
    train_op=train_op,
    eval_metric_ops={'accuracy': acc_op})

class Model:
  def __init__(self):
    pass

def load(m=None):
  if m is None:
    m=Model()
  # Build the Estimator
  m.estimator = tf.estimator.Estimator(model_fn)
  return m

def train(m):
  # Define the input function for training
  input_fn = tf.estimator.inputs.numpy_input_fn(
    x={'images': mnist.train.images}, y=mnist.train.labels,
    batch_size=batch_size, num_epochs=None, shuffle=True)
  # Train the Model
  m.estimator.train(input_fn, steps=num_steps)

def eval(m):
  # Evaluate the Model
  # Define the input function for evaluating
  input_fn = tf.estimator.inputs.numpy_input_fn(
      x={'images': mnist.test.images}, y=mnist.test.labels,
      batch_size=batch_size, shuffle=False)

  # Use the Estimator 'evaluate' method
  e = m.estimator.evaluate(input_fn)
  print("Testing Accuracy:", e['accuracy'])

