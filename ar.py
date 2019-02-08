from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

fn = 'safi_v1.wav'
Fs,x = wavfile.read(fn)

# percent time stretch
bottom 	= 50
top 	= 150
N		= len(x)
Ts		= 1

control = np.linspace(bottom,top,N)

s = np.sin(np.linspace(bottom,top,N)*10)
s = s*.5
s = s*100
s += 100
control = s

# control = 100*np.ones(control.shape)

timeIdx = np.linspace(0,len(x),len(x)-1)

temp = 0
stretchIdx = []
stretchIdx.append(timeIdx[0])
for i,c in zip(timeIdx,control):
	stretchIdx.append(temp + Ts*100/c)
	temp = stretchIdx[-1]

stretchIdx = np.array(stretchIdx)
timeIdx = np.linspace(0,len(x),len(x))

rs = np.zeros(len(timeIdx))

i = 0
for iS in stretchIdx:
	val = 0
	for iT in timeIdx:
		rs[i] += np.sinc(-iT+iS)
	i += 1
	if i%10 == 0:
		print(i/len(stretchIdx),end='')

print('done')






# for c in d_control:
if [True,False][1]:
	plt.subplot(2,1,1)
	plt.plot(stretchIdx)
	plt.subplot(2,1,2)
	plt.plot(control)
	plt.show()



