#-*-coding:utf-8-*-
import numpy as np
import logging
import theano
#选择一定的方式，根据梯度更新params的方法
class ADAGRAD(object):
    def __init__(self, params, lr, lr_sgd, epsilon=1e-8):
        logging.info('Optimizer ADAGRAD lr %f' % (lr, ))
        self.lr = lr
        self.lr_sgd = lr_sgd
        self.epsilon = epsilon
        self.acc_grad = {}
        for param in params:
            self.acc_grad[param] = np.zeros_like(param.get_value())

    def iterate(self, grads):
        lr = self.lr
        epsilon = self.epsilon
        for param, grad in grads.iteritems():

            if param.name != 'Ws':
                param.set_value((param.get_value() - grad.get_value() * self.lr_sgd).astype(theano.config.floatX))
            else:
                self.acc_grad[param] = self.acc_grad[param] + grad.get_value()**2
                param_update = lr * grad.get_value() / (np.sqrt(self.acc_grad[param]) + epsilon)
                param.set_value((param.get_value() - param_update).astype(theano.config.floatX))

    def iterateSGD(self, grads):
        for param, grad in grads.iteritems():
            param.set_value((param.get_value() - grad.get_value() * self.lr_sgd).astype(theano.config.floatX))

    def iterateADAGRAD(self, grads):
        lr = self.lr
        epsilon = self.epsilon
        for param, grad in grads.iteritems():
            self.acc_grad[param] = self.acc_grad[param] + grad.get_value()**2
            param_update = lr * grad.get_value() / (np.sqrt(self.acc_grad[param]) + epsilon)
            param.set_value((param.get_value() - param_update).astype(theano.config.floatX))

OptimizerList = {'ADAGRAD': ADAGRAD}
