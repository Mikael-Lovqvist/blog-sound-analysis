import subprocess
assert subprocess.call(('make', '-B')) == 0

from math import sqrt

from buffers import sample_buffer, frequency_buffer, frequency_bin_settings_buffer, fourier_transform_state
from low_level import fourier_transform_settings, init_fourier_transform, run_fourier_transform, c_pointer
import ffmpeg
from utils import counting_iterator






bin_settings = frequency_bin_settings_buffer(5)

bin_settings[0].frequency = 100
bin_settings[1].frequency = 200
bin_settings[2].frequency = 300
bin_settings[3].frequency = 400
bin_settings[4].frequency = 500

common_falloff = 10000.0
bin_settings[0].falloff = common_falloff
bin_settings[1].falloff = common_falloff
bin_settings[2].falloff = common_falloff
bin_settings[3].falloff = common_falloff
bin_settings[4].falloff = common_falloff


bin_settings.used = 5


buflen = 500000

settings = fourier_transform_settings(48000, bin_settings._data)


buf = sample_buffer(buflen)

output_buffers = [frequency_buffer(buflen) for f in range(bin_settings.used)]



from math import sin, tau

def gen_sine(frequency, sample_rate, amplitude=1.0, phase_offset=0.0):
	accumulator = phase_offset % tau
	accumulator_step = frequency * tau / sample_rate

	while True:
		accumulator = (accumulator + accumulator_step) % tau
		yield sin(accumulator) * amplitude


state = fourier_transform_state(settings)


#print(settings.bin.contents.data[0])
#print(state.acc[0])

#print(state.acc[2])

init_fourier_transform(state._data)




output_matrix_type = c_pointer(frequency_buffer._type) * bin_settings.used
output = output_matrix_type(*(b._data for b in output_buffers))


sample_counter = counting_iterator()

filename = '/home/devilholk/Downloads/Rolemusic - pl4y1ng.mp3'

#filename ='/home/devilholk/Authorative_Repository/Planning/Archived Voice Recordings/p2.m4a'

audio_source = ffmpeg.file_based_audio_decoder(filename)


audio_source.start()
t = 0.0

try:
	samples = audio_source.get_samples(buf.allocated)
	buf[:] = sample_counter((left + right) * .5 for (left, right) in samples)
	buf.used = sample_counter.value

	t += sample_counter.value / audio_source.sample_rate
	print(f'Time: {t:.02f}s')

	run_fourier_transform(state._data, buf._data, output)



finally:

	audio_source.stop()


import struct

with open('dump.raw', 'wb') as outfile:

	for index in range(output_buffers[0].allocated):

		output_sample = b''

		for buf in output_buffers:
			sample = buf._data.contents.data[index]

			value = sqrt(sample.x.value**2 + sample.y.value**2)
			#value = sample.y.value

			output_sample += struct.pack('d', value)
		outfile.write(output_sample)


# for i in range(settings.bin.contents.used.value):
# 	print(state.acc[i])

# for sample in output[2].contents.data[:100000]:
#  	print(sqrt(sample.x.value**2 + sample.y.value**2))

# #print(buf)