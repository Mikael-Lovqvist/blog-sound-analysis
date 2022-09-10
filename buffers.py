import low_level as L

#Higher level
class _generic_buffer:
	def __init__(self, count):
		self._data = self._alloc(count)

	def __del__(self):
		self._free(self._data)

	def __getitem__(self, s):
		if isinstance(s, slice):
			start, stop, step = s.start or 0, s.stop or self._data.contents.allocated.value, s.step or 1
			return self._data.contents.data[start:stop:step]
		else:
			return self._data.contents.data[s]

	def __setitem__(self, s, value):
		if isinstance(s, slice):
			start, stop, step = s.start or 0, s.stop or self._data.contents.allocated.value, s.step or 1
			for index, sub_value in zip(range(start, stop, step), value):
				self._data.contents.data[index] = sub_value
		else:
			self._data.contents.data[s] = value

	@property
	def allocated(self):
		return self._data.contents.allocated.value

	@property
	def used(self):
		return self._data.contents.used.value

	@used.setter
	def used(self, value):
		self._data.contents.used.value = value


class _generic_structure:
	def __init__(self, *positional, **named):
		self._data = self._alloc(*positional, **named)

		for name, type in self._data.contents._fields_:
			setattr(self, name, getattr(self._data.contents, name))

	def __del__(self):
		self._free(self._data)


class frequency_buffer(_generic_buffer):
	_alloc = L.allocate_frequency_buffer
	_free = L.free_frequency_buffer
	_type = L.frequency_buffer

class sample_buffer(_generic_buffer):
	_alloc = L.allocate_sample_buffer
	_free = L.free_sample_buffer
	_type = L.sample_buffer

class frequency_bin_settings_buffer(_generic_buffer):
	_alloc = L.allocate_frequency_bin_settings_buffer
	_free = L.free_frequency_bin_settings_buffer
	_type = L.frequency_bin_settings_buffer

class fourier_transform_state(_generic_structure):
	_alloc = L.allocate_fourier_transform_state
	_free = L.free_fourier_transform_state
	_type = L.fourier_transform_state

