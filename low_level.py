from c_helpers import c_type, c_typedef, c_struct, c_pointer, c_function, c_lib

_lib = c_lib('./ft1.so')

c_type('double', 'c_double')
c_type('int', 'c_int')

c_typedef('scalar', double)
c_struct('scalar_point',
	x = scalar,
	y = scalar,
)

c_struct('sample_buffer',
	allocated = int,
	used = int,
	data = c_pointer(scalar),
)

c_struct('frequency_buffer',
	allocated = int,
	used = int,
	data = c_pointer(scalar_point),
)


c_struct('frequency_bin_settings',
	frequency = scalar,
	falloff = scalar,
	start = scalar_point,
)

c_struct('frequency_bin_settings_buffer',
	allocated = int,
	used = int,
	data = c_pointer(frequency_bin_settings),
)

c_struct('frequency_accumulator',
	accumulator = scalar_point,
	phase = scalar,
	falloff = scalar,
	advance = scalar,
	count = int,
)

c_struct('fourier_transform_settings',
	sample_rate = scalar,
	bin = c_pointer(frequency_bin_settings_buffer),
)

c_struct('fourier_transform_state',
	settings = c_pointer(fourier_transform_settings),
	acc = c_pointer(frequency_accumulator),
)

c_function(_lib, 'allocate_sample_buffer', c_pointer(sample_buffer),
	size = int,
)

c_function(_lib, 'allocate_frequency_buffer', c_pointer(frequency_buffer),
	size = int,
)

c_function(_lib, 'allocate_frequency_bin_settings_buffer', c_pointer(frequency_bin_settings_buffer),
	size = int,
)

c_function(_lib, 'allocate_fourier_transform_state', c_pointer(fourier_transform_state),
	settings = c_pointer(fourier_transform_settings),
)

c_function(_lib, 'free_sample_buffer', None,
	buffer = c_pointer(sample_buffer),
)

c_function(_lib, 'free_frequency_buffer', None,
	buffer = c_pointer(frequency_buffer),
)

c_function(_lib, 'free_frequency_bin_settings_buffer', None,
	buffer = c_pointer(frequency_bin_settings_buffer),
)

c_function(_lib, 'free_fourier_transform_state', None,
	buffer = c_pointer(fourier_transform_state),
)


c_function(_lib, 'init_fourier_transform', None,
	state = c_pointer(fourier_transform_state),
)


c_function(_lib, 'run_fourier_transform', None,
	state = c_pointer(fourier_transform_state),
	input = c_pointer(sample_buffer),
	output = c_pointer(c_pointer(frequency_buffer)),	#TODO - we should use a collection probably
)