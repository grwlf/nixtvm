import tensorflow as tf

from nnvm import sym as _sym
from copy import copy
from tensorflow import Tensor as TF_Tensor
from tensorflow.gfile import FastGFile
from tensorflow.summary import FileWriter
from tensorflow import Graph as TF_Graph, GraphDef as TF_GraphDef
from tensorflow.python.ops import variables
from nnvm.frontend import from_tensorflow
from typing import Any,Dict,List
from tvm.tensor import Tensor as TVM_Tensor

from freezepb.runners import *
from freezepb.modeldefs import *

def tf_const(name,shape):
  assert tuple(MODEL_PARAMS[name].shape)==tuple(shape)
  return tf.constant(MODEL_PARAMS[name].asnumpy())

BLOCK2_INPUT="Rcnn_ctcV3/conv_block3/unit1/add_14/add"
# sym_480391360 is connected to both inputs
BLOCK2_INPUTS=[
    "Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/batchnorm/mul_1:0"
  , "Rcnn_ctcV3/conv_block3_1/unit2/add_15/add:1"
  ]

BLOCK2_OUTPUT="Rcnn_ctcV3/conv2d_116/BiasAdd"


class Stopped(Exception):
  def __init__(self, out):
    super().__init__("nnvm stager early stop")
    self.out = out


def block2_block_nnvm(sym_480391360,stopat:str=BLOCK2_OUTPUT):
  varnames={}
  stopnames=[]

  def addvar(name,shape):
    nonlocal varnames
    s = _sym.Variable(name=name,shape=shape)
    varnames.update({name:s})
    return s

  def checkpoint(s):
    nonlocal stopnames
    name = s.list_output_names()[0].replace('_output','')
    stopnames.append(name)
    if name==stopat:
      raise Stopped(s)

  try:
    sym_89108592 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/moving_variance",shape=(192,))
    sym_86660000 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/batchnorm/add/y",shape=(1,))
    sym_146107552 = _sym.broadcast_add(sym_89108592,sym_86660000,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/batchnorm/add")
    sym_382713408 = _sym.__pow_scalar__(sym_146107552,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/batchnorm/Rsqrt",scalar=-0.5)
    sym_85993200 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/gamma",shape=(192,))
    sym_146107280 = _sym.broadcast_mul(sym_382713408,sym_85993200,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/batchnorm/mul")
    sym_146107376 = _sym.broadcast_mul(sym_480391360,sym_146107280,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/batchnorm/mul_1")
    sym_393365200 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/moving_mean",shape=(192,))
    sym_100393904 = _sym.broadcast_mul(sym_393365200,sym_146107280,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/batchnorm/mul_2")
    sym_367190496 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/beta",shape=(192,))
    sym_100394320 = _sym.broadcast_sub(sym_367190496,sym_100393904,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/batchnorm/sub")
    sym_149168256 = _sym.broadcast_add(sym_146107376,sym_100394320,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_28/batchnorm/add_1")
    checkpoint(sym_149168256)
    sym_91999584 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/activation/conv2d_85/kernel",shape=(1, 1, 192, 192))
    sym_489572528 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/activation/conv2d_85/bias",shape=(192,))
    sym_452185136 = _sym.pad(sym_149168256,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_489573008 = _sym.conv2d(sym_452185136,sym_91999584,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(1, 1),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_1/unit2/activation/conv2d_85/convolution",use_bias=False)
    sym_452185136 = _sym.broadcast_add(sym_489573008,sym_489572528)
    sym_105212592 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/activation/conv2d_86/kernel",shape=(1, 1, 192, 192))
    sym_100075984 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/activation/conv2d_86/bias",shape=(192,))
    sym_105212304 = _sym.pad(sym_149168256,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_455423312 = _sym.conv2d(sym_105212304,sym_105212592,layout="NHWC",strides=(1, 1),padding=[0, 0],dilation=(1, 1),kernel_size=(1, 1),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_1/unit2/activation/conv2d_86/convolution",use_bias=False)
    sym_105212304 = _sym.broadcast_add(sym_455423312,sym_100075984)
    sym_455423856 = _sym.broadcast_add(sym_452185136,sym_105212304,name="Rcnn_ctcV3/conv_block3_1/unit2/activation/max_27/add")
    sym_82981456 = _sym.broadcast_sub(sym_452185136,sym_105212304,name="Rcnn_ctcV3/conv_block3_1/unit2/activation/max_27/sub")
    sym_88256992 = _sym.relu(sym_82981456,name="Rcnn_ctcV3/conv_block3_1/unit2/activation/max_27/Relu")
    sym_385748976 = _sym.broadcast_add(sym_455423856,sym_88256992,name="Rcnn_ctcV3/conv_block3_1/unit2/activation/max_27/add_1")
    sym_118633648 = _sym.broadcast_sub(sym_105212304,sym_452185136,name="Rcnn_ctcV3/conv_block3_1/unit2/activation/max_27/sub_1")
    sym_118633776 = _sym.relu(sym_118633648,name="Rcnn_ctcV3/conv_block3_1/unit2/activation/max_27/Relu_1")
    sym_83860624 = _sym.broadcast_add(sym_385748976,sym_118633776,name="Rcnn_ctcV3/conv_block3_1/unit2/activation/max_27/add_2")
    sym_88942384 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/activation/max_27/mul/x",shape=(1,))
    sym_83860784 = _sym.broadcast_mul(sym_88942384,sym_83860624,name="Rcnn_ctcV3/conv_block3_1/unit2/activation/max_27/mul")
    checkpoint(sym_83860784)
    sym_146185312 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/conv2d_87/kernel",shape=(3, 3, 192, 192))
    sym_123818576 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/conv2d_87/bias",shape=(192,))
    sym_51379712 = _sym.pad(sym_83860784,pad_width=((0, 0), (1, 1), (1, 1), (0, 0)))
    sym_284337840 = _sym.conv2d(sym_51379712,sym_146185312,layout="NHWC",strides=(1, 1),padding=[0, 0],dilation=(1, 1),kernel_size=(3, 3),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_1/unit2/conv2d_87/convolution",use_bias=False)
    sym_51379712 = _sym.broadcast_add(sym_284337840,sym_123818576)
    sym_118481536 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/gamma",shape=(192,))
    sym_108661440 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/beta",shape=(192,))
    sym_83230208 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/moving_mean",shape=(192,))
    sym_75303200 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/moving_variance",shape=(192,))
    sym_223540640 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/batchnorm/add/y",shape=(1,))
    sym_284338384 = _sym.broadcast_add(sym_75303200,sym_223540640,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/batchnorm/add")
    checkpoint(sym_284338384)
    sym_379070752 = _sym.__pow_scalar__(sym_284338384,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/batchnorm/Rsqrt",scalar=-0.5)
    sym_457130976 = _sym.broadcast_mul(sym_379070752,sym_118481536,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/batchnorm/mul")
    sym_470662800 = _sym.broadcast_mul(sym_51379712,sym_457130976,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/batchnorm/mul_1")
    sym_470662864 = _sym.broadcast_mul(sym_83230208,sym_457130976,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/batchnorm/mul_2")
    sym_89117184 = _sym.broadcast_sub(sym_108661440,sym_470662864,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/batchnorm/sub")
    sym_89117376 = _sym.broadcast_add(sym_470662800,sym_89117184,name="Rcnn_ctcV3/conv_block3_1/unit2/static_batch_normalization_29/batchnorm/add_1")
    sym_149765696 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/conv2d_88/kernel",shape=(1, 1, 192, 192))
    sym_483354480 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/conv2d_88/bias",shape=(192,))
    sym_367083280 = _sym.pad(sym_89117376,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_483354960 = _sym.conv2d(sym_367083280,sym_149765696,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(1, 1),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/conv2d_88/convolution",use_bias=False)
    sym_367083280 = _sym.broadcast_add(sym_483354960,sym_483354480)
    sym_145792752 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/conv2d_89/kernel",shape=(1, 1, 192, 192))
    sym_457499856 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/conv2d_89/bias",shape=(192,))
    sym_145792464 = _sym.pad(sym_89117376,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_149112096 = _sym.conv2d(sym_145792464,sym_145792752,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(1, 1),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/conv2d_89/convolution",use_bias=False)
    sym_145792464 = _sym.broadcast_add(sym_149112096,sym_457499856)
    sym_149112640 = _sym.broadcast_add(sym_367083280,sym_145792464,name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/max_28/add")
    sym_457122720 = _sym.broadcast_sub(sym_367083280,sym_145792464,name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/max_28/sub")
    sym_457709440 = _sym.relu(sym_457122720,name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/max_28/Relu")
    sym_88086480 = _sym.broadcast_add(sym_149112640,sym_457709440,name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/max_28/add_1")
    sym_223552112 = _sym.broadcast_sub(sym_145792464,sym_367083280,name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/max_28/sub_1")
    sym_223552176 = _sym.relu(sym_223552112,name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/max_28/Relu_1")
    sym_223552560 = _sym.broadcast_add(sym_88086480,sym_223552176,name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/max_28/add_2")
    sym_149177840 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/max_28/mul/x",shape=(1,))
    sym_394085360 = _sym.broadcast_mul(sym_149177840,sym_223552560,name="Rcnn_ctcV3/conv_block3_1/unit2/activation_1/max_28/mul")
    sym_104094144 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/conv2d_90/kernel",shape=(3, 3, 192, 192))
    sym_385754128 = addvar(name="Rcnn_ctcV3/conv_block3_1/unit2/conv2d_90/bias",shape=(192,))
    sym_149177968 = _sym.pad(sym_394085360,pad_width=((0, 0), (1, 1), (1, 1), (0, 0)))
    sym_359386352 = _sym.conv2d(sym_149177968,sym_104094144,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(3, 3),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_1/unit2/conv2d_90/convolution",use_bias=False)
    sym_149177968 = _sym.broadcast_add(sym_359386352,sym_385754128)
    sym_88474160 = _sym.broadcast_add(sym_149177968,sym_480391360,name="Rcnn_ctcV3/conv_block3_1/unit2/add_15/add")
    checkpoint(sym_88474160)
    sym_377560640 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/gamma",shape=(192,))
    sym_105564416 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/beta",shape=(192,))
    sym_149177744 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/moving_mean",shape=(192,))
    sym_394323280 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/moving_variance",shape=(192,))
    sym_143315712 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/batchnorm/add/y",shape=(1,))
    sym_149177568 = _sym.broadcast_add(sym_394323280,sym_143315712,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/batchnorm/add")
    sym_223534496 = _sym.__pow_scalar__(sym_149177568,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/batchnorm/Rsqrt",scalar=-0.5)
    sym_223534592 = _sym.broadcast_mul(sym_223534496,sym_377560640,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/batchnorm/mul")
    sym_359373472 = _sym.broadcast_mul(sym_88474160,sym_223534592,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/batchnorm/mul_1")
    sym_359373888 = _sym.broadcast_mul(sym_149177744,sym_223534592,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/batchnorm/mul_2")
    sym_82826624 = _sym.broadcast_sub(sym_105564416,sym_359373888,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/batchnorm/sub")
    sym_82827104 = _sym.broadcast_add(sym_359373472,sym_82826624,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_30/batchnorm/add_1")
    checkpoint(sym_82827104)
    sym_367184720 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/activation/conv2d_91/kernel",shape=(1, 1, 192, 192))
    sym_284058064 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/activation/conv2d_91/bias",shape=(192,))
    sym_367184304 = _sym.pad(sym_82827104,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_394436448 = _sym.conv2d(sym_367184304,sym_367184720,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(1, 1),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_2/unit3/activation/conv2d_91/convolution",use_bias=False)
    sym_367184304 = _sym.broadcast_add(sym_394436448,sym_284058064)
    sym_223532000 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/activation/conv2d_92/kernel",shape=(1, 1, 192, 192))
    sym_75038320 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/activation/conv2d_92/bias",shape=(192,))
    sym_394436992 = _sym.pad(sym_82827104,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_149198800 = _sym.conv2d(sym_394436992,sym_223532000,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(1, 1),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_2/unit3/activation/conv2d_92/convolution",use_bias=False)
    sym_394436992 = _sym.broadcast_add(sym_149198800,sym_75038320)
    sym_223512992 = _sym.broadcast_add(sym_367184304,sym_394436992,name="Rcnn_ctcV3/conv_block3_2/unit3/activation/max_29/add")
    sym_88156128 = _sym.broadcast_sub(sym_367184304,sym_394436992,name="Rcnn_ctcV3/conv_block3_2/unit3/activation/max_29/sub")
    sym_181417296 = _sym.relu(sym_88156128,name="Rcnn_ctcV3/conv_block3_2/unit3/activation/max_29/Relu")
    sym_385616848 = _sym.broadcast_add(sym_223512992,sym_181417296,name="Rcnn_ctcV3/conv_block3_2/unit3/activation/max_29/add_1")
    sym_385617264 = _sym.broadcast_sub(sym_394436992,sym_367184304,name="Rcnn_ctcV3/conv_block3_2/unit3/activation/max_29/sub_1")
    sym_52513744 = _sym.relu(sym_385617264,name="Rcnn_ctcV3/conv_block3_2/unit3/activation/max_29/Relu_1")
    sym_367099056 = _sym.broadcast_add(sym_385616848,sym_52513744,name="Rcnn_ctcV3/conv_block3_2/unit3/activation/max_29/add_2")
    sym_88156448 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/activation/max_29/mul/x",shape=(1,))
    sym_367099216 = _sym.broadcast_mul(sym_88156448,sym_367099056,name="Rcnn_ctcV3/conv_block3_2/unit3/activation/max_29/mul")
    sym_238287504 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/conv2d_93/kernel",shape=(3, 3, 192, 192))
    sym_93313120 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/conv2d_93/bias",shape=(192,))
    sym_394312880 = _sym.pad(sym_367099216,pad_width=((0, 0), (1, 1), (1, 1), (0, 0)))
    sym_455609696 = _sym.conv2d(sym_394312880,sym_238287504,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(3, 3),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_2/unit3/conv2d_93/convolution",use_bias=False)
    sym_394312880 = _sym.broadcast_add(sym_455609696,sym_93313120)
    sym_453626080 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/gamma",shape=(192,))
    sym_385757328 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/beta",shape=(192,))
    sym_92005968 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/moving_mean",shape=(192,))
    sym_457127312 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/moving_variance",shape=(192,))
    sym_104985248 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/batchnorm/add/y",shape=(1,))
    sym_453625568 = _sym.broadcast_add(sym_457127312,sym_104985248,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/batchnorm/add")
    sym_367089856 = _sym.__pow_scalar__(sym_453625568,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/batchnorm/Rsqrt",scalar=-0.5)
    sym_472030368 = _sym.broadcast_mul(sym_367089856,sym_453626080,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/batchnorm/mul")
    sym_472030464 = _sym.broadcast_mul(sym_394312880,sym_472030368,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/batchnorm/mul_1")
    sym_74982368 = _sym.broadcast_mul(sym_92005968,sym_472030368,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/batchnorm/mul_2")
    sym_74982496 = _sym.broadcast_sub(sym_385757328,sym_74982368,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/batchnorm/sub")
    sym_223613200 = _sym.broadcast_add(sym_472030464,sym_74982496,name="Rcnn_ctcV3/conv_block3_2/unit3/static_batch_normalization_31/batchnorm/add_1")
    checkpoint(sym_223613200)
    sym_83206384 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/conv2d_94/kernel",shape=(1, 1, 192, 192))
    sym_125060048 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/conv2d_94/bias",shape=(192,))
    sym_223613680 = _sym.pad(sym_223613200,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_452030544 = _sym.conv2d(sym_223613680,sym_83206384,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(1, 1),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/conv2d_94/convolution",use_bias=False)
    sym_223613680 = _sym.broadcast_add(sym_452030544,sym_125060048)
    sym_492264992 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/conv2d_95/kernel",shape=(1, 1, 192, 192))
    sym_94777856 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/conv2d_95/bias",shape=(192,))
    sym_132912848 = _sym.pad(sym_223613200,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_385631504 = _sym.conv2d(sym_132912848,sym_492264992,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(1, 1),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/conv2d_95/convolution",use_bias=False)
    sym_132912848 = _sym.broadcast_add(sym_385631504,sym_94777856)
    sym_453607776 = _sym.broadcast_add(sym_223613680,sym_132912848,name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/max_30/add")
    sym_74186480 = _sym.broadcast_sub(sym_223613680,sym_132912848,name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/max_30/sub")
    sym_457775984 = _sym.relu(sym_74186480,name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/max_30/Relu")
    sym_457776176 = _sym.broadcast_add(sym_453607776,sym_457775984,name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/max_30/add_1")
    sym_216045840 = _sym.broadcast_sub(sym_132912848,sym_223613680,name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/max_30/sub_1")
    sym_299777120 = _sym.relu(sym_216045840,name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/max_30/Relu_1")
    sym_74186176 = _sym.broadcast_add(sym_457776176,sym_299777120,name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/max_30/add_2")
    sym_120063008 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/max_30/mul/x",shape=(1,))
    sym_74186272 = _sym.broadcast_mul(sym_120063008,sym_74186176,name="Rcnn_ctcV3/conv_block3_2/unit3/activation_1/max_30/mul")
    sym_116113008 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/conv2d_96/kernel",shape=(3, 3, 192, 192))
    sym_382719232 = addvar(name="Rcnn_ctcV3/conv_block3_2/unit3/conv2d_96/bias",shape=(192,))
    sym_382719056 = _sym.pad(sym_74186272,pad_width=((0, 0), (1, 1), (1, 1), (0, 0)))
    sym_382112272 = _sym.conv2d(sym_382719056,sym_116113008,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(3, 3),channels=192,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block3_2/unit3/conv2d_96/convolution",use_bias=False)
    sym_382719056 = _sym.broadcast_add(sym_382112272,sym_382719232)
    sym_74186736 = _sym.broadcast_add(sym_382719056,sym_88474160,name="Rcnn_ctcV3/conv_block3_2/unit3/add_16/add")
    checkpoint(sym_74186736)
    sym_489301152 = addvar(name="Rcnn_ctcV3/expand_conv4/conv2d_97/kernel",shape=(1, 1, 192, 256))
    sym_457717648 = addvar(name="Rcnn_ctcV3/expand_conv4/conv2d_97/bias",shape=(256,))
    sym_472042128 = _sym.pad(sym_74186736,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_379783504 = _sym.conv2d(sym_472042128,sym_489301152,layout="NHWC",strides=(1, 1),padding=[0, 0],dilation=(1, 1),kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/expand_conv4/conv2d_97/convolution",use_bias=False)
    sym_472042128 = _sym.broadcast_add(sym_379783504,sym_457717648)
    sym_86813200 = addvar(name="Rcnn_ctcV3/expand_conv4/conv2d_98/kernel",shape=(3, 3, 192, 256))
    sym_149206176 = addvar(name="Rcnn_ctcV3/expand_conv4/conv2d_98/bias",shape=(256,))
    sym_366878288 = _sym.pad(sym_74186736,pad_width=((0, 0), (1, 1), (1, 1), (0, 0)))
    sym_378188352 = _sym.conv2d(sym_366878288,sym_86813200,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(3, 3),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/expand_conv4/conv2d_98/convolution",use_bias=False)
    sym_366878288 = _sym.broadcast_add(sym_378188352,sym_149206176)
    sym_79062816 = addvar(name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/gamma",shape=(256,))
    sym_100932496 = addvar(name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/beta",shape=(256,))
    sym_75061856 = addvar(name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/moving_mean",shape=(256,))
    sym_121639120 = addvar(name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/moving_variance",shape=(256,))
    sym_489278688 = addvar(name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/batchnorm/add/y",shape=(1,))
    sym_223609616 = _sym.broadcast_add(sym_121639120,sym_489278688,name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/batchnorm/add")
    sym_382109104 = _sym.__pow_scalar__(sym_223609616,name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/batchnorm/Rsqrt",scalar=-0.5)
    sym_472034112 = _sym.broadcast_mul(sym_382109104,sym_79062816,name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/batchnorm/mul")
    sym_472034560 = _sym.broadcast_mul(sym_366878288,sym_472034112,name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/batchnorm/mul_1")
    sym_457503264 = _sym.broadcast_mul(sym_75061856,sym_472034112,name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/batchnorm/mul_2")
    sym_457503648 = _sym.broadcast_sub(sym_100932496,sym_457503264,name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/batchnorm/sub")
    sym_455442096 = _sym.broadcast_add(sym_472034560,sym_457503648,name="Rcnn_ctcV3/expand_conv4/static_batch_normalization_32/batchnorm/add_1")
    checkpoint(sym_455442096)
    sym_86776256 = addvar(name="Rcnn_ctcV3/expand_conv4/activation/conv2d_99/kernel",shape=(1, 1, 256, 256))
    sym_379070224 = addvar(name="Rcnn_ctcV3/expand_conv4/activation/conv2d_99/bias",shape=(256,))
    sym_455442480 = _sym.pad(sym_455442096,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_451396240 = _sym.conv2d(sym_455442480,sym_86776256,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/expand_conv4/activation/conv2d_99/convolution",use_bias=False)
    sym_455442480 = _sym.broadcast_add(sym_451396240,sym_379070224)
    sym_92742368 = addvar(name="Rcnn_ctcV3/expand_conv4/activation/conv2d_100/kernel",shape=(1, 1, 256, 256))
    sym_88574976 = addvar(name="Rcnn_ctcV3/expand_conv4/activation/conv2d_100/bias",shape=(256,))
    sym_223539440 = _sym.pad(sym_455442096,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_483359056 = _sym.conv2d(sym_223539440,sym_92742368,layout="NHWC",strides=(1, 1),padding=[0, 0],dilation=(1, 1),kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/expand_conv4/activation/conv2d_100/convolution",use_bias=False)
    sym_223539440 = _sym.broadcast_add(sym_483359056,sym_88574976)
    sym_223540032 = _sym.broadcast_add(sym_455442480,sym_223539440,name="Rcnn_ctcV3/expand_conv4/activation/max_31/add")
    sym_457135056 = _sym.broadcast_sub(sym_455442480,sym_223539440,name="Rcnn_ctcV3/expand_conv4/activation/max_31/sub")
    sym_457729248 = _sym.relu(sym_457135056,name="Rcnn_ctcV3/expand_conv4/activation/max_31/Relu")
    sym_457729440 = _sym.broadcast_add(sym_223540032,sym_457729248,name="Rcnn_ctcV3/expand_conv4/activation/max_31/add_1")
    sym_457142480 = _sym.broadcast_sub(sym_223539440,sym_455442480,name="Rcnn_ctcV3/expand_conv4/activation/max_31/sub_1")
    sym_457142672 = _sym.relu(sym_457142480,name="Rcnn_ctcV3/expand_conv4/activation/max_31/Relu_1")
    sym_385623856 = _sym.broadcast_add(sym_457729440,sym_457142672,name="Rcnn_ctcV3/expand_conv4/activation/max_31/add_2")
    sym_453605008 = addvar(name="Rcnn_ctcV3/expand_conv4/activation/max_31/mul/x",shape=(1,))
    sym_385624016 = _sym.broadcast_mul(sym_453605008,sym_385623856,name="Rcnn_ctcV3/expand_conv4/activation/max_31/mul")
    sym_234740896 = addvar(name="Rcnn_ctcV3/expand_conv4/conv2d_101/kernel",shape=(3, 3, 256, 256))
    sym_394390128 = addvar(name="Rcnn_ctcV3/expand_conv4/conv2d_101/bias",shape=(256,))
    sym_378184992 = _sym.pad(sym_385624016,pad_width=((0, 0), (1, 1), (1, 1), (0, 0)))
    sym_51336848 = _sym.conv2d(sym_378184992,sym_234740896,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(3, 3),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/expand_conv4/conv2d_101/convolution",use_bias=False)
    sym_378184992 = _sym.broadcast_add(sym_51336848,sym_394390128)
    sym_477435760 = _sym.broadcast_add(sym_378184992,sym_472042128,name="Rcnn_ctcV3/expand_conv4/add_17/add")
    checkpoint(sym_477435760)
    sym_124429376 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/gamma",shape=(256,))
    sym_385617296 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/beta",shape=(256,))
    sym_75392816 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/moving_mean",shape=(256,))
    sym_103921888 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/moving_variance",shape=(256,))
    sym_394044400 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/batchnorm/add/y",shape=(1,))
    sym_477435888 = _sym.broadcast_add(sym_103921888,sym_394044400,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/batchnorm/add")
    sym_385433312 = _sym.__pow_scalar__(sym_477435888,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/batchnorm/Rsqrt",scalar=-0.5)
    sym_457495552 = _sym.broadcast_mul(sym_385433312,sym_124429376,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/batchnorm/mul")
    sym_457496096 = _sym.broadcast_mul(sym_477435760,sym_457495552,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/batchnorm/mul_1")
    sym_378195984 = _sym.broadcast_mul(sym_75392816,sym_457495552,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/batchnorm/mul_2")
    sym_378196400 = _sym.broadcast_sub(sym_385617296,sym_378195984,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/batchnorm/sub")
    sym_46963920 = _sym.broadcast_add(sym_457496096,sym_378196400,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_33/batchnorm/add_1")
    checkpoint(sym_46963920)
    sym_70178352 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/activation/conv2d_102/kernel",shape=(1, 1, 256, 256))
    sym_73075840 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/activation/conv2d_102/bias",shape=(256,))
    sym_223558384 = _sym.pad(sym_46963920,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_394305968 = _sym.conv2d(sym_223558384,sym_70178352,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4/unit1/activation/conv2d_102/convolution",use_bias=False)
    sym_223558384 = _sym.broadcast_add(sym_394305968,sym_73075840)
    sym_392605408 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/activation/conv2d_103/kernel",shape=(1, 1, 256, 256))
    sym_152478752 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/activation/conv2d_103/bias",shape=(256,))
    sym_452990880 = _sym.pad(sym_46963920,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_86637584 = _sym.conv2d(sym_452990880,sym_392605408,layout="NHWC",strides=(1, 1),padding=[0, 0],dilation=(1, 1),kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4/unit1/activation/conv2d_103/convolution",use_bias=False)
    sym_452990880 = _sym.broadcast_add(sym_86637584,sym_152478752)
    sym_152480096 = _sym.broadcast_add(sym_223558384,sym_452990880,name="Rcnn_ctcV3/conv_block4/unit1/activation/max_32/add")
    sym_382186448 = _sym.broadcast_sub(sym_223558384,sym_452990880,name="Rcnn_ctcV3/conv_block4/unit1/activation/max_32/sub")
    sym_367093088 = _sym.relu(sym_382186448,name="Rcnn_ctcV3/conv_block4/unit1/activation/max_32/Relu")
    sym_367093280 = _sym.broadcast_add(sym_152480096,sym_367093088,name="Rcnn_ctcV3/conv_block4/unit1/activation/max_32/add_1")
    sym_451215696 = _sym.broadcast_sub(sym_452990880,sym_223558384,name="Rcnn_ctcV3/conv_block4/unit1/activation/max_32/sub_1")
    sym_451215888 = _sym.relu(sym_451215696,name="Rcnn_ctcV3/conv_block4/unit1/activation/max_32/Relu_1")
    sym_382119392 = _sym.broadcast_add(sym_367093280,sym_451215888,name="Rcnn_ctcV3/conv_block4/unit1/activation/max_32/add_2")
    sym_452814752 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/activation/max_32/mul/x",shape=(1,))
    sym_382119552 = _sym.broadcast_mul(sym_452814752,sym_382119392,name="Rcnn_ctcV3/conv_block4/unit1/activation/max_32/mul")
    sym_83201008 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/conv2d_104/kernel",shape=(3, 3, 256, 256))
    sym_93335072 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/conv2d_104/bias",shape=(256,))
    sym_486331504 = _sym.pad(sym_382119552,pad_width=((0, 0), (1, 1), (1, 1), (0, 0)))
    sym_382363280 = _sym.conv2d(sym_486331504,sym_83201008,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(3, 3),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4/unit1/conv2d_104/convolution",use_bias=False)
    sym_486331504 = _sym.broadcast_add(sym_382363280,sym_93335072)
    sym_81047024 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/gamma",shape=(256,))
    sym_79073392 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/beta",shape=(256,))
    sym_91927664 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/moving_mean",shape=(256,))
    sym_238348176 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/moving_variance",shape=(256,))
    sym_379840640 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/batchnorm/add/y",shape=(1,))
    sym_394299376 = _sym.broadcast_add(sym_238348176,sym_379840640,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/batchnorm/add")
    sym_89392304 = _sym.__pow_scalar__(sym_394299376,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/batchnorm/Rsqrt",scalar=-0.5)
    sym_93587680 = _sym.broadcast_mul(sym_89392304,sym_81047024,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/batchnorm/mul")
    sym_93587776 = _sym.broadcast_mul(sym_486331504,sym_93587680,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/batchnorm/mul_1")
    sym_73448960 = _sym.broadcast_mul(sym_91927664,sym_93587680,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/batchnorm/mul_2")
    sym_382736736 = _sym.broadcast_sub(sym_79073392,sym_73448960,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/batchnorm/sub")
    sym_382736864 = _sym.broadcast_add(sym_93587776,sym_382736736,name="Rcnn_ctcV3/conv_block4/unit1/static_batch_normalization_34/batchnorm/add_1")
    checkpoint(sym_382736864)
    sym_76408096 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/activation_1/conv2d_105/kernel",shape=(1, 1, 256, 256))
    sym_218187488 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/activation_1/conv2d_105/bias",shape=(256,))
    sym_93588000 = _sym.pad(sym_382736864,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_76671024 = _sym.conv2d(sym_93588000,sym_76408096,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4/unit1/activation_1/conv2d_105/convolution",use_bias=False)
    sym_93588000 = _sym.broadcast_add(sym_76671024,sym_218187488)
    sym_51337392 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/activation_1/conv2d_106/kernel",shape=(1, 1, 256, 256))
    sym_104880304 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/activation_1/conv2d_106/bias",shape=(256,))
    sym_76671152 = _sym.pad(sym_382736864,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_81912736 = _sym.conv2d(sym_76671152,sym_51337392,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4/unit1/activation_1/conv2d_106/convolution",use_bias=False)
    sym_76671152 = _sym.broadcast_add(sym_81912736,sym_104880304)
    sym_473742192 = _sym.broadcast_add(sym_93588000,sym_76671152,name="Rcnn_ctcV3/conv_block4/unit1/activation_1/max_33/add")
    sym_379159792 = _sym.broadcast_sub(sym_93588000,sym_76671152,name="Rcnn_ctcV3/conv_block4/unit1/activation_1/max_33/sub")
    sym_146204640 = _sym.relu(sym_379159792,name="Rcnn_ctcV3/conv_block4/unit1/activation_1/max_33/Relu")
    sym_366874912 = _sym.broadcast_add(sym_473742192,sym_146204640,name="Rcnn_ctcV3/conv_block4/unit1/activation_1/max_33/add_1")
    sym_366875328 = _sym.broadcast_sub(sym_76671152,sym_93588000,name="Rcnn_ctcV3/conv_block4/unit1/activation_1/max_33/sub_1")
    sym_88731184 = _sym.relu(sym_366875328,name="Rcnn_ctcV3/conv_block4/unit1/activation_1/max_33/Relu_1")
    sym_152211952 = _sym.broadcast_add(sym_366874912,sym_88731184,name="Rcnn_ctcV3/conv_block4/unit1/activation_1/max_33/add_2")
    sym_146204704 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/activation_1/max_33/mul/x",shape=(1,))
    sym_152212112 = _sym.broadcast_mul(sym_146204704,sym_152211952,name="Rcnn_ctcV3/conv_block4/unit1/activation_1/max_33/mul")
    sym_79059936 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/conv2d_107/kernel",shape=(3, 3, 256, 256))
    sym_78831712 = addvar(name="Rcnn_ctcV3/conv_block4/unit1/conv2d_107/bias",shape=(256,))
    sym_452825680 = _sym.pad(sym_152212112,pad_width=((0, 0), (1, 1), (1, 1), (0, 0)))
    sym_457779424 = _sym.conv2d(sym_452825680,sym_79059936,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(3, 3),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4/unit1/conv2d_107/convolution",use_bias=False)
    sym_452825680 = _sym.broadcast_add(sym_457779424,sym_78831712)
    sym_457507664 = _sym.broadcast_add(sym_452825680,sym_477435760,name="Rcnn_ctcV3/conv_block4/unit1/add_18/add")
    checkpoint(sym_457507664)
    sym_256158240 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/gamma",shape=(256,))
    sym_83430496 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/beta",shape=(256,))
    sym_329254032 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/moving_mean",shape=(256,))
    sym_378173584 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/moving_variance",shape=(256,))
    sym_457507168 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/batchnorm/add/y",shape=(1,))
    sym_89401920 = _sym.broadcast_add(sym_378173584,sym_457507168,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/batchnorm/add")
    sym_477439760 = _sym.__pow_scalar__(sym_89401920,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/batchnorm/Rsqrt",scalar=-0.5)
    sym_477439856 = _sym.broadcast_mul(sym_477439760,sym_256158240,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/batchnorm/mul")
    sym_453615040 = _sym.broadcast_mul(sym_457507664,sym_477439856,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/batchnorm/mul_1")
    sym_367200976 = _sym.broadcast_mul(sym_329254032,sym_477439856,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/batchnorm/mul_2")
    sym_367201104 = _sym.broadcast_sub(sym_83430496,sym_367200976,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/batchnorm/sub")
    sym_101145744 = _sym.broadcast_add(sym_453615040,sym_367201104,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_35/batchnorm/add_1")
    sym_100941744 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/activation/conv2d_108/kernel",shape=(1, 1, 256, 256))
    sym_80614592 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/activation/conv2d_108/bias",shape=(256,))
    sym_101146224 = _sym.pad(sym_101145744,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_143310448 = _sym.conv2d(sym_101146224,sym_100941744,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4_1/unit2/activation/conv2d_108/convolution",use_bias=False)
    sym_101146224 = _sym.broadcast_add(sym_143310448,sym_80614592)
    sym_101105904 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/activation/conv2d_109/kernel",shape=(1, 1, 256, 256))
    sym_394411888 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/activation/conv2d_109/bias",shape=(256,))
    sym_104543072 = _sym.pad(sym_101145744,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_83196848 = _sym.conv2d(sym_104543072,sym_101105904,layout="NHWC",strides=(1, 1),padding=[0, 0],dilation=(1, 1),kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4_1/unit2/activation/conv2d_109/convolution",use_bias=False)
    sym_104543072 = _sym.broadcast_add(sym_83196848,sym_394411888)
    sym_104543664 = _sym.broadcast_add(sym_101146224,sym_104543072,name="Rcnn_ctcV3/conv_block4_1/unit2/activation/max_34/add")
    sym_117663728 = _sym.broadcast_sub(sym_101146224,sym_104543072,name="Rcnn_ctcV3/conv_block4_1/unit2/activation/max_34/sub")
    sym_105219440 = _sym.relu(sym_117663728,name="Rcnn_ctcV3/conv_block4_1/unit2/activation/max_34/Relu")
    sym_83021568 = _sym.broadcast_add(sym_104543664,sym_105219440,name="Rcnn_ctcV3/conv_block4_1/unit2/activation/max_34/add_1")
    sym_83021728 = _sym.broadcast_sub(sym_104543072,sym_101146224,name="Rcnn_ctcV3/conv_block4_1/unit2/activation/max_34/sub_1")
    sym_83407296 = _sym.relu(sym_83021728,name="Rcnn_ctcV3/conv_block4_1/unit2/activation/max_34/Relu_1")
    sym_103682960 = _sym.broadcast_add(sym_83021568,sym_83407296,name="Rcnn_ctcV3/conv_block4_1/unit2/activation/max_34/add_2")
    sym_378281392 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/activation/max_34/mul/x",shape=(1,))
    sym_378281200 = _sym.broadcast_mul(sym_378281392,sym_103682960,name="Rcnn_ctcV3/conv_block4_1/unit2/activation/max_34/mul")
    checkpoint(sym_378281200)
    sym_152788384 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/conv2d_110/kernel",shape=(3, 3, 256, 256))
    sym_77188768 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/conv2d_110/bias",shape=(256,))
    sym_89400064 = _sym.pad(sym_378281200,pad_width=((0, 0), (1, 1), (1, 1), (0, 0)))
    sym_77190208 = _sym.conv2d(sym_89400064,sym_152788384,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(3, 3),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4_1/unit2/conv2d_110/convolution",use_bias=False)
    sym_89400064 = _sym.broadcast_add(sym_77190208,sym_77188768)
    sym_88778896 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/gamma",shape=(256,))
    sym_238290352 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/beta",shape=(256,))
    sym_104191024 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/moving_mean",shape=(256,))
    sym_86902736 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/moving_variance",shape=(256,))
    sym_52504256 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/batchnorm/add/y",shape=(1,))
    sym_238712976 = _sym.broadcast_add(sym_86902736,sym_52504256,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/batchnorm/add")
    sym_452801328 = _sym.__pow_scalar__(sym_238712976,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/batchnorm/Rsqrt",scalar=-0.5)
    sym_379767200 = _sym.broadcast_mul(sym_452801328,sym_88778896,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/batchnorm/mul")
    sym_379767296 = _sym.broadcast_mul(sym_89400064,sym_379767200,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/batchnorm/mul_1")
    sym_149039632 = _sym.broadcast_mul(sym_104191024,sym_379767200,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/batchnorm/mul_2")
    sym_149040048 = _sym.broadcast_sub(sym_238290352,sym_149039632,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/batchnorm/sub")
    sym_378980928 = _sym.broadcast_add(sym_379767296,sym_149040048,name="Rcnn_ctcV3/conv_block4_1/unit2/static_batch_normalization_36/batchnorm/add_1")
    checkpoint(sym_378980928)
    sym_125175280 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/conv2d_111/kernel",shape=(1, 1, 256, 256))
    sym_366867792 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/conv2d_111/bias",shape=(256,))
    sym_366864960 = _sym.pad(sym_378980928,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_379847360 = _sym.conv2d(sym_366864960,sym_125175280,padding=[0, 0],dilation=(1, 1),layout="NHWC",strides=(1, 1),kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/conv2d_111/convolution",use_bias=False)
    sym_366864960 = _sym.broadcast_add(sym_379847360,sym_366867792)
    sym_130260432 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/conv2d_112/kernel",shape=(1, 1, 256, 256))
    sym_394401808 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/conv2d_112/bias",shape=(256,))
    sym_378993264 = _sym.pad(sym_378980928,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_105862560 = _sym.conv2d(sym_378993264,sym_130260432,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/conv2d_112/convolution",use_bias=False)
    sym_378993264 = _sym.broadcast_add(sym_105862560,sym_394401808)
    sym_83429088 = _sym.broadcast_add(sym_366864960,sym_378993264,name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/max_35/add")
    sym_118634784 = _sym.broadcast_sub(sym_366864960,sym_378993264,name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/max_35/sub")
    sym_455434320 = _sym.relu(sym_118634784,name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/max_35/Relu")
    sym_455434512 = _sym.broadcast_add(sym_83429088,sym_455434320,name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/max_35/add_1")
    sym_452016176 = _sym.broadcast_sub(sym_378993264,sym_366864960,name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/max_35/sub_1")
    sym_452016368 = _sym.relu(sym_452016176,name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/max_35/Relu_1")
    sym_149046704 = _sym.broadcast_add(sym_455434512,sym_452016368,name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/max_35/add_2")
    sym_223649568 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/max_35/mul/x",shape=(1,))
    sym_451233824 = _sym.broadcast_mul(sym_223649568,sym_149046704,name="Rcnn_ctcV3/conv_block4_1/unit2/activation_1/max_35/mul")
    sym_394319936 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/conv2d_113/kernel",shape=(3, 3, 256, 256))
    sym_121636512 = addvar(name="Rcnn_ctcV3/conv_block4_1/unit2/conv2d_113/bias",shape=(256,))
    sym_149047296 = _sym.pad(sym_451233824,pad_width=((0, 0), (1, 1), (1, 1), (0, 0)))
    sym_94636928 = _sym.conv2d(sym_149047296,sym_394319936,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(3, 3),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/conv_block4_1/unit2/conv2d_113/convolution",use_bias=False)
    sym_149047296 = _sym.broadcast_add(sym_94636928,sym_121636512)
    sym_382095632 = _sym.broadcast_add(sym_149047296,sym_457507664,name="Rcnn_ctcV3/conv_block4_1/unit2/add_19/add")
    checkpoint(sym_382095632)
    sym_457721664 = addvar(name="Rcnn_ctcV3/static_batch_normalization_37/gamma",shape=(256,))
    sym_382354176 = addvar(name="Rcnn_ctcV3/static_batch_normalization_37/beta",shape=(256,))
    sym_104234656 = addvar(name="Rcnn_ctcV3/static_batch_normalization_37/moving_mean",shape=(256,))
    sym_385760896 = addvar(name="Rcnn_ctcV3/static_batch_normalization_37/moving_variance",shape=(256,))
    sym_115259392 = addvar(name="Rcnn_ctcV3/static_batch_normalization_37/batchnorm/add/y",shape=(1,))
    sym_385428032 = _sym.broadcast_add(sym_385760896,sym_115259392,name="Rcnn_ctcV3/static_batch_normalization_37/batchnorm/add")
    sym_121467136 = _sym.__pow_scalar__(sym_385428032,name="Rcnn_ctcV3/static_batch_normalization_37/batchnorm/Rsqrt",scalar=-0.5)
    sym_121467232 = _sym.broadcast_mul(sym_121467136,sym_457721664,name="Rcnn_ctcV3/static_batch_normalization_37/batchnorm/mul")
    sym_121467680 = _sym.broadcast_mul(sym_382095632,sym_121467232,name="Rcnn_ctcV3/static_batch_normalization_37/batchnorm/mul_1")
    sym_367166064 = _sym.broadcast_mul(sym_104234656,sym_121467232,name="Rcnn_ctcV3/static_batch_normalization_37/batchnorm/mul_2")
    sym_367166448 = _sym.broadcast_sub(sym_382354176,sym_367166064,name="Rcnn_ctcV3/static_batch_normalization_37/batchnorm/sub")
    sym_472209424 = _sym.broadcast_add(sym_121467680,sym_367166448,name="Rcnn_ctcV3/static_batch_normalization_37/batchnorm/add_1")
    sym_88800208 = addvar(name="Rcnn_ctcV3/activation/conv2d_114/kernel",shape=(1, 1, 256, 256))
    sym_378170400 = addvar(name="Rcnn_ctcV3/activation/conv2d_114/bias",shape=(256,))
    sym_472209872 = _sym.pad(sym_472209424,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_382373888 = _sym.conv2d(sym_472209872,sym_88800208,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/activation/conv2d_114/convolution",use_bias=False)
    sym_472209872 = _sym.broadcast_add(sym_382373888,sym_378170400)
    sym_132599600 = addvar(name="Rcnn_ctcV3/activation/conv2d_115/kernel",shape=(1, 1, 256, 256))
    sym_394302224 = addvar(name="Rcnn_ctcV3/activation/conv2d_115/bias",shape=(256,))
    sym_477431696 = _sym.pad(sym_472209424,pad_width=((0, 0), (0, 0), (0, 0), (0, 0)))
    sym_88133200 = _sym.conv2d(sym_477431696,sym_132599600,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(1, 1),channels=256,kernel_layout="HWIO",name="Rcnn_ctcV3/activation/conv2d_115/convolution",use_bias=False)
    sym_477431696 = _sym.broadcast_add(sym_88133200,sym_394302224)
    sym_486318912 = _sym.broadcast_add(sym_472209872,sym_477431696,name="Rcnn_ctcV3/activation/max_36/add")
    sym_486319296 = _sym.broadcast_sub(sym_472209872,sym_477431696,name="Rcnn_ctcV3/activation/max_36/sub")
    sym_75084208 = _sym.relu(sym_486319296,name="Rcnn_ctcV3/activation/max_36/Relu")
    sym_75084400 = _sym.broadcast_add(sym_486318912,sym_75084208,name="Rcnn_ctcV3/activation/max_36/add_1")
    sym_75084752 = _sym.broadcast_sub(sym_477431696,sym_472209872,name="Rcnn_ctcV3/activation/max_36/sub_1")
    sym_120853792 = _sym.relu(sym_75084752,name="Rcnn_ctcV3/activation/max_36/Relu_1")
    sym_120854176 = _sym.broadcast_add(sym_75084400,sym_120853792,name="Rcnn_ctcV3/activation/max_36/add_2")
    checkpoint(sym_120854176)
    sym_140634816 = addvar(name="Rcnn_ctcV3/activation/max_36/mul/x",shape=(1,))
    sym_140634432 = _sym.broadcast_mul(sym_140634816,sym_120854176,name="Rcnn_ctcV3/activation/max_36/mul")
    sym_283877680 = addvar(name="Rcnn_ctcV3/conv2d_116/kernel",shape=(1, 6, 256, 1318))
    sym_105665056 = addvar(name="Rcnn_ctcV3/conv2d_116/bias",shape=(1318,))
    sym_89033648 = _sym.conv2d(sym_140634432,sym_283877680,dilation=(1, 1),layout="NHWC",strides=(1, 1),padding=[0, 0],kernel_size=(1, 6),channels=1318,kernel_layout="HWIO",name="Rcnn_ctcV3/conv2d_116/convolution",use_bias=False)
    sym_375435392 = _sym.broadcast_add(sym_89033648,sym_105665056,name=BLOCK2_OUTPUT)
    checkpoint(sym_375435392)
    # if stopat!=BLOCK2_OUTPUT:
    raise Exception("block2_nnvm_run: Invalid stop output for staging")
    # return sym_375435392,varnames,stopnames
  except Stopped as s:
    return s.out,varnames,stopnames



def block2_tf_run(nwarmup:int=0,nloops:int=1,init_method='zeros',verbose=True,stopat:str=BLOCK2_OUTPUT,**kwargs)->Result:
  """ Run the model on tensorflow with zero inputs """
  print("Warning: unused args:", kwargs) if kwargs != {} else None
  r=Result()
  r.desc='tf running time'

  with tf.Session(graph=tf.Graph()) as sess:
    with FastGFile(MODEL_PB, 'rb') as f:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name="")
    sess.run(variables.global_variables_initializer())
    g=tf.get_default_graph()
    # inps=[g.get_tensor_by_name(t) for t in BLOCK2_INPUTS]
    # inps=[g.get_tensor_by_name(t) for t in ["Rcnn_ctcV3/conv_block3/unit1/conv2d_84/BiasAdd:0"]]
    inps=[g.get_tensor_by_name(t) for t in [BLOCK2_INPUT+":0"]]
    for i in inps:
      print("Input nodes:",type(i), i.name, i.dtype, i)
    out=g.get_tensor_by_name(stopat+":0")
    print("Output node:",type(out), out.name, out.dtype, out)

    return run_tf(
        sess,nwarmup,nloops
      , {i:common_init(init_method, i.shape, i.dtype.as_numpy_dtype()) for i in inps}
      , out
      , verbose)


def block2_nnvm_run(nwarmup:int=0,nloops:int=1,init_method='zeros',verbose=True,debug=False,stopat:str=BLOCK2_OUTPUT,**kwargs):
  # sym_149080784 = tf.placeholder(shape=(1,108,21,32),dtype=tf.float32)
  print("Warning: unused args:", kwargs) if kwargs != {} else None
  inp=_sym.Variable(name='inp', init=np.zeros(shape=(1,54,6,192)))

  block2,blockvars,_=block2_block_nnvm(inp,stopat=stopat)
  block2_params={sym:MODEL_PARAMS[k] for (k,sym) in blockvars.items()}
  block2_params.update({inp:common_init('zeros',(1,54,6,192),np.float32)})

  r=run_nnvm(
      nwarmup,nloops,
      block2_params,
      block2,
      verbose=verbose,
      debug=debug)

  return r


def block2_analyze(r:Result):

  d=r.last_debug_datum
  print(d)

  eid = 0
  rank=[]
  for node, time in zip(d._nodes_list, d._time_list):
    num_outputs = d.get_graph_node_output_num(node)
    for j in range(num_outputs):
      op = node['op']
      if node['op'] == 'param':
        continue
      name = node['name']
      shape = str(d._output_tensor_list[eid].shape)
      time_us = round(time[0] * 1000000, 2)
      inputs = str(node['attrs']['num_inputs'])
      outputs = str(node['attrs']['num_outputs'])
      rank.append((time_us, shape, op,name))
      eid+=1

  for t,shape,op,name in sorted(rank,key=lambda x: x[0]):
    print('%8.2f'%(t,), shape, op, name)

def experiment1():
  _,_,stopnames=block2_block_nnvm(_sym.Variable(name='inp', init=np.zeros(shape=(1,54,6,192))))

  for stopat in stopnames:
    print('StopPoint',stopat)
    r1=block2_nnvm_run(1,10,stopat=stopat);
    print(r1)
    r2=block2_tf_run(1,10,stopat=stopat);
    print(r2)


