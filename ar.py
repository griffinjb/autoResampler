from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from time import strftime


class autoResampler:

# Global Class variables and control
	fn = 'demo_wavBender.wav'
	Fs = 0
	Ts = 0
	x = []
	width = 20
	out = []
	# s = []

	# def __init__(self):
	# 		# control signal
	# 	self.s = self.singen(T=.25,Fs=self.Fs,A=3,bias=100)


	def run(self):
		self.readAudio(self.fn)
		s = self.singen(T=.25,Fs=self.Fs,A=3,bias=100)
		# print(s.__next__())
		newIdx = self.genNewIdx(s)
		self.out = self.windowedSinc(newIdx,self.x,self.width)
		self.out = self.norm(out)
		self.write_audio(self.out)


	# read audio
	def readAudio(self,fn):
		self.Fs,self.x = wavfile.read(fn)
		# self.x = self.x[:5*self.Fs,0]
		self.Ts = 1/self.Fs



	# generate time modulation signal
		# Periodic
		# use a generator!
	def singen(self,T = 1,Fs = 44100,A=1,bias=0,phase=0):
		s = A*np.sin(np.linspace(0,2*np.pi,T*Fs)+phase)+bias
		while True:
			for x in s:
				yield(x)

	# generate desired sample indices
		# bounded by min/max time with a border equal
		# to the window width
	def genNewIdx(self,s):
		ri = [self.width]				# resampled indices
		while True:
			ri.append(ri[-1]+1*s.__next__()/100)
			if ri[-1]>len(self.x)-self.width:
				nope = ri.pop()
				break
		return(ri)

	# iterate through the generated indices,
	# using a windowed sinc reconstruction
	# centered at the floor of the current index.
	def windowedSinc(self,ri,x,width):
		so = [] 				# signal out
		ctr = 0
		for i in ri:
			t = 0
			rt = width+i%1
			for v in x[int(i)-width:int(i)+width]:
				t += v*np.sinc(rt)
				rt -= 1
			so.append(t)


			if not ctr%1000:
				print(ctr/len(ri),end='\r')
			ctr += 1
		print('\n')
		return(so)

	def norm(self,so,A=1.8):
		so = np.array(so)
		norm_signal = so-so.min()
		norm_signal = A*norm_signal/norm_signal.max()
		norm_signal = norm_signal-A/2
		return(norm_signal)

	def write_audio(self,x):	
		# write audio file
		wavfile.write('demo_wavBender'+strftime("%Y%m%d_%H%M%S_")+'.wav',data=x,rate=self.Fs)


if __name__ == '__main__':
	ar = autoResampler()
	ar.run()

