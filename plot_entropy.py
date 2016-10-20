import numpy as np
import matplotlib.pyplot as plt


import util
import sklearn
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


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

	return [a, b, c, d]

def plot_avg():
	"""
	plot avg H
	"""
	m = get_all()

	x = np.arange(m[0].shape[0]) # 156*100
	print len(x)	 
	avr = []

	for i in range(4):
		avr.append(np.sum(m[i], axis=1)/m[i].shape[1])

	plt.figure('average')
	color = ['b','g','r','m']
	labels = ['hip', 'hport', 'dip', 'dport']
	for i in range(4):
		plt.plot(x, avr[i],color[i], label=labels[i])
	
	plt.legend()
	plt.show()
	return 

if __name__ == '__main__':
	plot_avg()