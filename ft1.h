#ifndef FT1_H

typedef double scalar;
typedef struct scalar_point {
	scalar x;
	scalar y;
} scalar_point;

typedef struct sample_buffer {
	int allocated;
	int used;
	scalar* data;
} sample_buffer;

typedef struct frequency_accumulator {
	scalar_point accumulator;
	scalar phase;
	scalar falloff;
	scalar advance;
	int count;
} frequency_accumulator;

typedef struct frequency_buffer {
	int allocated;
	int used;
	scalar_point* data;
} frequency_buffer;

typedef struct frequency_bin_settings {
	scalar frequency;
	scalar falloff;
	scalar_point start;
} frequency_bin_settings;

typedef struct frequency_bin_settings_buffer {
	int allocated;
	int used;
	frequency_bin_settings* data;
} frequency_bin_settings_buffer;


typedef struct fourier_transform_settings {
	scalar sample_rate;
	frequency_bin_settings_buffer* bin;
} fourier_transform_settings;

typedef struct fourier_transform_state {
	fourier_transform_settings* settings;
	frequency_accumulator* acc;
} fourier_transform_state;


#endif
#define FT1_H