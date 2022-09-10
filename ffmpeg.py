import subprocess, struct, threading, signal, queue, time

def system_is_little_endian():
	return struct.pack('H', 1)[0] == 1

def system_is_big_endian():
	return struct.pack('H', 1)[1] == 1

common_ffmpeg_options = ('-hide_banner', '-nostats', '-loglevel', 'error')


class file_based_audio_decoder(threading.Thread):
	#This one calls ffmpeg as an external process but we aim of course to make more direct use of decoders in the future
	def __init__(self, filename):
		super().__init__()
		self.filename = filename

		#Hardcoded parameters for now - later use ffprobe
		self.sample_size = 4	#32 bit float
		self.channels = 2		#stereo
		self.sample_rate = 48000
		self.ffmpeg_format = 'f32le' if system_is_little_endian() else 'f32be'
		self.sample_format = 'ff'

		self.started = threading.Event()
		self.finished = threading.Event()

	def start(self):
		super().start()
		self.started.wait()

	def stop(self):
		#self.pipe.close()	#This works but kinda makes ffmpeg angry

		self.proc.send_signal(signal.SIGTERM)
		try:
			self.proc.wait(0.25)
		except subprocess.TimeoutExpired:
			print('ffmpeg is stubborn')
			self.proc.send_signal(signal.SIGKILL)

		#SIGTERM and SIGINT does not work.
		#SIGKILL works but I want to find a more graceful solution
		#self.proc.send_signal(signal.SIGHUP)	#Hang up on ffmpeg	 - terminates but messes up terminal
		#self.finished.set()

	def run(self):
		#ffmpeg -formats
		#example: -i input.flv -f s16le -acodec pcm_s16le output.raw

		#self.proc = subprocess.Popen(('ffmpeg', '-i', self.filename, '-f', self.ffmpeg_format, '-acodec', f'pcm_{self.ffmpeg_format}', '-'), stdout=subprocess.PIPE)
		self.proc = subprocess.Popen(('ffmpeg', *common_ffmpeg_options, '-i', self.filename, '-f', self.ffmpeg_format, '-acodec', f'pcm_{self.ffmpeg_format}', '-'), stdout=subprocess.PIPE)
		self.pipe = self.proc.stdout
		self.started.set()
		self.proc.wait()
		self.finished.set()

	def get_samples(self, count):
		buf = self.pipe.read(count * self.sample_size * self.channels)
		if not buf:
			self.finished.set()

		return struct.iter_unpack(self.sample_format, buf)

