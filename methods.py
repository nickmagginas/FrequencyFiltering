import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
import time

plt.style.use('dark_background')

def audioread(filename): 
	data , fs = sf.read(filename)
	data = data[:660000]
	return data , fs

def find_nearest2(x,value):
	indices = list(range(0,len(x)))
	x = [(indices[i],x[i]) for i in range(0,len(x))]
	while len(x)>1:
		amplitude = list(map(lambda x : x[1] , x))
		x = x[:int(len(x)/2)] if (abs(np.min(amplitude)-value) < abs(np.max(amplitude)-value)) else x[int(len(x)/2):]
	return x[0][0]

def find_nearest(x,value):
	return np.argmin([abs(x-value) for x in x])

def get_loudness(data):
	return np.average(data)

def plot_time_domain(data,fs):
	x = np.linspace(0,1/fs*len(data),len(data))
	plt.plot(x,data)
	plt.show()

def furrier_transform(data,T):
	frequency_data = fft(data)
	f = np.linspace(0.0, 1.0/(2.0*T), len(frequency_data)/2)
	frequency_data = 2.0/len(frequency_data) * np.abs(frequency_data[:len(frequency_data)//2])
	frequency_data = [(lambda x,y : (x,y))(frequency_data[i],f[i]) for i in range(0,len(frequency_data))]
	return frequency_data

def plot_frequency_domain(data):
	yf , xf = list(map(lambda x : x[0] , data)),list(map(lambda x : x[1] , data))
	plt.plot(xf,yf)
	plt.show() 

def filter(data , high_pass = None , low_pass = 9999999): 
	new_data = []
	for i in data: 
		if i[1] > high_pass and i[1] < low_pass:
			new_data.append(i)
		else: new_data.append((0,i[1]))
	return new_data

def remove_noise(data , amplitude_cut = None, octaves = (1,11)):
	octaves = [(16.35*np.power(2,i) , 30.87*np.power(2,i)) for i in range(octaves[0]-1,octaves[1])]	
	noiseless_data = []
	octave_data = []
	for i in octaves: 
		octave_data  = filter(data, i[0] , i[1])
		if i == octaves[0]:
			max_amplitude = np.max(list(map(lambda x : x[0], octave_data)))
		noiseless_data.extend([i for i in octave_data if i[0] > amplitude_cut*max_amplitude])
		max_amplitude = np.max(list(map(lambda x : x[0], octave_data)))
	return noiseless_data

def harmonize(data):
	notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	root_notes = [16.35,17.32,18.35,19.45,20.60,21.83,24.50,25.96,27.50,29.14,30.87]
	all_notes = []
	[all_notes.extend(list(map(lambda x : round(x*np.power(2,i),2) , root_notes))) for i in range(0,11)]
	amplitudes = np.zeros(12)
	for i in data:
		index = find_nearest(all_notes,i[1])
		if index < 12: 
			amplitudes[index] += i[0]
		else: amplitudes[index%12] += i[0]
	return amplitudes

def smooth(data):
	root_notes = [16.35,17.32,18.35,19.45,20.60,21.83,24.50,25.96,27.50,29.14,30.87]
	all_notes = []
	[all_notes.extend(list(map(lambda x : round(x*np.power(2,i),2) , root_notes))) for i in range(1,11)]
	
def plot_density(note_density):
	plt.plot(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'],note_density,'ro')
	plt.show()

def main(plot = False):
	print('Beginning Execution...')
	start_time = time.time()
	filename = '/home/nick/Desktop/Theory/blues.00000.au'
	data , fs = audioread(filename)
	frequency_data = furrier_transform(data,1/fs)
	data = filter(frequency_data , high_pass = 16.35 , low_pass = 30.87*(2**5))
	noiseless_data = remove_noise(data,amplitude_cut = 0.8 ,octaves = (1,5))
	amplitude_notes = harmonize(noiseless_data)
	plot_density(amplitude_notes)
	

	print('Execution Time:', str(time.time()-start_time) + 's')

if __name__ == "__main__": 
	main()