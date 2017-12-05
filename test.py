def estimate_key(data,octaves = 5,print_key = False):
	A , f = list(map(lambda x : x[0] , data)),list(map(lambda x : x[1] , data))
	root_notes = [16.35,17.32,18.35,19.45,20.60,21.83,24.50,25.96,27.50,29.14,30.87]
	[root_notes.extend(list(map(lambda x : round(x*i,2) , root_notes))) for i in range(2,octaves)]
	note_amplitudes = [A[find_nearest2(f , value)] for value in root_notes]
	note_density = []
	for i in range(0,12):
		note_density.append(np.sum([note_amplitudes[x] for x in range(i,len(note_amplitudes),11)]))
	key = np.argmax(note_density)
	key_amplitude = note_density[key]
	note_density.remove(note_density[key])
	key_confidence = (key_amplitude - max(note_density))/key_amplitude
	notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	if print_key:
		print('Key:' , notes[key] , ', with confidence:', key_confidence*100 , '%')
	return notes[key] , key_confidence
	
def plot_density(note_density):
	plt.plot(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'],note_density,'ro')
	plt.show()