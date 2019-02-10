from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

# read audio
fn = 'safi_v1.wav'
Fs,x = wavfile.read(fn)
# x = x[:5*Fs,0]
Ts = 1/Fs

# generate time modulation signal
	# Periodic
	# use a generator!
def singen(T = 1,Fs = 44100,A=1,bias=0,phase=0):
	s = A*np.sin(np.linspace(0,2*np.pi,T*Fs)+phase)+bias
	while True:
		for x in s:
			yield(x)

# generate desired sample indices
	# bounded by min/max time with a border equal
	# to the window width
width = 20
ri = [width] 							# resampled indices
s = singen(T=.5,Fs=Fs,A=5,bias=100) 	# control signal
while True:
	ri.append(ri[-1]+1*s.__next__()/100)
	if ri[-1]>len(x)-width:
		nope = ri.pop()
		break

# iterate through the generated indices,
# using a windowed sinc reconstruction
# centered at the floor of the current index.

so = [] 				# signal out
ctr = 0
for i in ri:
	t = 0
	rt = width+i%1
	for v in x[int(i)-width:int(i)+width]:
		t += v*np.sinc(rt)
		rt -= 1
	so.append(t)


	if not ctr%44100:
		print(ctr/len(ri),end='\r')
	ctr += 1

print('\n')
so = np.array(so)
norm_signal = so-so.min()
norm_signal = norm_signal/norm_signal.max()
norm_signal = norm_signal-1

# write audio file
wavfile.write('tester2.wav',data=norm_signal,rate=Fs)


