import matplotlib.pyplot as plt
from scipy.io import wavfile
import os
from pydub import AudioSegment

def get_wav_info(wav_file):
	rate,data = wavfile.read(wav_file)
	return rate,data

def graph_spectrogram(wav_file):
	rate,data = get_wav_info(wav_file)
	nfft = 200
	fs =8000
	noverlap = 171
	nchannels = data.ndim
	if nchannels == 1:
		pxx, freqs, bins, im = plt.specgram(data, nfft, fs, noverlap = noverlap)
	elif nchannels == 2:
		pxx, freqs, bins, im = plt.specgram(data[:,0], nfft, fs, noverlap = noverlap)
	return pxx

#Because of superposing some audio segments may become excessively loud causing the network to learn that, this will standardise it
def match_target_amplitude(sound, target_dBFS):
	change_in_dBFS = target_dBFS - sound.dBFS
	return sound.apply_gain(change_in_dBFS)

def load_raw_audio():
	ons = []
	offs = []
	negatives = []
	backgrounds = []
	for filename in os.listdir("./data/on"):
		if filename.endswith("wav"):
			audio = AudioSegment.from_wav("./data/on/"+filename)
			ons.append(audio)
	for filename in os.listdir("./data/off"):
		if filename.endswith("wav"):
			audio = AudioSegment.from_wav("./data/off/"+filename)
			offs.append(audio)
	for filename in os.listdir("./data/_background_noise_"):
		if filename.endswith("wav"):
			audio = AudioSegment.from_wav("./data/_background_noise_/"+filename)
			backgrounds.append(audio)

	for filename in os.listdir("./data/negatives"):
		if filename.endswith("wav"):
			audio = AudioSegment.from_wav("./data/negatives/"+filename)
			negatives.append(audio)
	return ons, offs, negatives, backgrounds