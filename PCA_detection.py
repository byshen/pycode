#!/usr/bin/python  
# -*- coding: utf-8 -*-  

import util
import sklearn
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

#计算均值,要求输入数据为numpy的矩阵格式，行表示样本数，列表示特征    
def meanX(dataX):
    return np.mean(dataX,axis=0)#axis=0表示按照列来求均值，如果输入list,则axis=1


#计算方差,传入的是一个numpy的矩阵格式，行表示样本数，列表示特征    
def variance(X):
    m, n = np.shape(X)
    mu = meanX(X)
    muAll = np.tile(mu, (m, 1))    
    X1 = X - muAll
    variance = 1./m * np.diag(X1.T * X1)
    return variance

#标准化,传入的是一个numpy的矩阵格式，行表示样本数，列表示特征    
def normalize(X):
    m, n = np.shape(X)
    mu = meanX(X)
    muAll = np.tile(mu, (m, 1))    
    X1 = X - muAll
    X2 = np.tile(np.diag(X.T * X), (m, 1))
    XNorm = X1/X2
    return XNorm
"""
参数：
	- XMat：传入的是一个numpy的矩阵格式，行表示样本数，列表示特征    
	- k：表示取前k个特征值对应的特征向量
返回值：
	- finalData：参数一指的是返回的低维矩阵，对应于输入参数二
	- reconData：参数二对应的是移动坐标轴后的矩阵
"""
def mypca(XMat, k):
    average = meanX(XMat) 
    m, n = np.shape(XMat)
    data_adjust = []
    avgs = np.tile(average, (m, 1))
    data_adjust = XMat - avgs
    covX = np.cov(data_adjust.T)   #计算协方差矩阵
    featValue, featVec=  np.linalg.eig(covX)  #求解协方差矩阵的特征值和特征向量
    index = np.argsort(-featValue) #按照featValue进行从大到小排序
    print index
    finalData = []
    if k > n:
        print "k must lower than feature number"
        return
    else:
        #注意特征向量时列向量，而numpy的二维矩阵(数组)a[m][n]中，a[1]表示第1行值
        selectVec = np.matrix(featVec.T[index[:k]]) #所以这里需要进行转置
        print len(selectVec)
        finalData = data_adjust * selectVec.T 
        reconData = (finalData * selectVec) + average  
    return finalData, reconData


def get_matrix(num):
	file_path = open('tmp/200101011400_%dentropy.txt' % num, 'r')
	matrix =[]
	for id, line in enumerate(file_path):
		m_list = line.strip().split('|')
		#print m_list

		mlist = [float(x) for x in m_list]
		if len(mlist) > 156:
			mlist = mlist[0:156]
		matrix.append(mlist)
		# print m_list
		# print "------------"

	
	return matrix

def get_all():
	hsip = []
	hsport = []
	hdip = []
	hdport = []

	for ii in range(100):
	#	print '-----', ii, '------'
		mat = get_matrix(ii)
		hsip.append(mat[0])
		hsport.append(mat[1])
		hdip.append(mat[2])
		hdport.append(mat[3])
		# for i in range(4):
		# 	print len(mat[0])

	a = np.array(hsip).transpose()
	b = np.array(hsport).transpose()
	c = np.array(hdip).transpose()
	d = np.array(hdport).transpose()

	return a, b, c, d

def plot():

	return

def main():
	x_sip, x_sport, x_dip, x_dport = get_all()
	print x_sip.shape
	
	pca = PCA(n_components=5) # 10, 0.85+ variance
	pca.fit(x_sip)

	print pca.explained_variance_ratio_
	print sum(pca.explained_variance_ratio_)
	x_new = pca.transform(x_sip)
	
	print x_new.shape

	plt.plot(x_new)
	plt.show()
	
	x_nn = pca.inverse_transform(x_new)
	
	print x_nn.shape

	x_avg = np.sum(x_nn, axis=1)/x_nn.shape[1]
	plt.plot(x_avg)
	plt.plot(np.sum(x_sip,axis=1)/x_sip.shape[1])
	plt.show()


	"""
	pca = PCA(n_components='mle') # 10, 0.75+ variance
	pca.fit(x_dip)

	print pca.explained_variance_ratio_
	print sum(pca.explained_variance_ratio_)

	pca = PCA(n_components='mle') # 10, 0.84+ variance
	pca.fit(x_sport)

	print pca.explained_variance_ratio_
	print sum(pca.explained_variance_ratio_)


	pca = PCA(n_components='mle') # 10, 0.83+ variance
	pca.fit(x_dport)

	print pca.explained_variance_ratio_
	print sum(pca.explained_variance_ratio_)
	
	a, b = mypca(x_sip, 10)
	print a.shape
	print b.shape
	"""
	return

if __name__ == '__main__':
	main()
