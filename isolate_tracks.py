from methods import audioread, furrier_transform , plot_frequency_domain, filter, plot_time_domain
from scipy.fftpack import ifft, fft
import matplotlib.pyplot as plt
import numpy as np
import wavio
import time

def isolate_frequencies(data, t_begin = 0, t_end = 0):
	samples_per_second = len(data)/30
	duration_data = data[int(t_begin*samples_per_second):int(t_end*samples_per_second):]
	frequency_data = filter(furrier_transform(duration_data,1/samples_per_second),20,60)
	amplitudes = list(map(lambda x : x[0],frequency_data))
	frequency_data = list(zip(list(reversed(amplitudes)),list(map(lambda x : x[1],frequency_data))))
	reverse_data = list(map(lambda x : (x[0],-x[1]) , frequency_data))
	final_freq_data = list(map(lambda x : x[0] , (reverse_data+frequency_data)))
	time_data = ifft(final_freq_data)
	return time_data

def main():
	filename = '/home/nick/Desktop/Theory/pop.00000.au'
	data , _ = audioread(filename)
	write_data = []
	for i in np.linspace(0,29.9,10000):
		buffer_data = isolate_frequencies(data , t_begin = i , t_end = i+0.1)
		write_data.extend(buffer_data)
	write_data = np.array(write_data)
	plot_time_domain(write_data,22000)
	wavio.write('isolated_file2',write_data,len(write_data)/30,sampwidth = 3)


if __name__ == '__main__':
	main()