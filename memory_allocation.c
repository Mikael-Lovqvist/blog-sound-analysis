#include "memory_allocation.h"
#include <stddef.h>
#include <stdlib.h>


frequency_buffer* allocate_frequency_buffer(int size) {

	frequency_buffer* result = calloc(1, sizeof(frequency_buffer));

	if (!result) {
		return NULL;
	}

	*result = (typeof(*result)) {
		.allocated = size,
		.used = 0,
		.data = calloc(size, sizeof(result->data[0])),
	};

	if (!result->data) {
		free(result);
		return NULL;
	}

	return result;
}

void free_frequency_buffer(frequency_buffer* buffer) {
	if (buffer->data) {
		free(buffer->data);
	}
	free(buffer);
}



sample_buffer* allocate_sample_buffer(int size) {

	sample_buffer* result = calloc(1, sizeof(sample_buffer));

	if (!result) {
		return NULL;
	}

	*result = (typeof(*result)) {
		.allocated = size,
		.used = 0,
		.data = calloc(size, sizeof(result->data[0])),
	};

	if (!result->data) {
		free(result);
		return NULL;
	}

	return result;
}

void free_sample_buffer(sample_buffer* buffer) {
	if (buffer->data) {
		free(buffer->data);
	}
	free(buffer);
}






frequency_bin_settings_buffer* allocate_frequency_bin_settings_buffer(int size) {

	frequency_bin_settings_buffer* result = calloc(1, sizeof(frequency_bin_settings_buffer));

	if (!result) {
		return NULL;
	}

	*result = (typeof(*result)) {
		.allocated = size,
		.used = 0,
		.data = calloc(size, sizeof(result->data[0])),
	};

	if (!result->data) {
		free(result);
		return NULL;
	}

	return result;
}

void free_frequency_bin_settings_buffer(frequency_bin_settings_buffer* buffer) {
	if (buffer->data) {
		free(buffer->data);
	}
	free(buffer);
}


fourier_transform_state* allocate_fourier_transform_state(fourier_transform_settings* settings) {

	fourier_transform_state* result = calloc(1, sizeof(fourier_transform_state));

	if (!result) {
		return NULL;
	}

	*result = (typeof(*result)) {
		.settings = settings,
		.acc = calloc(settings->bin->used, sizeof(result->acc[0])),
	};

	if (!result->acc) {
		free(result);
		return NULL;
	}


	return result;
}



void free_fourier_transform_state(fourier_transform_state* state) {
	if (state->acc) {
		free(state->acc);
	}
	free(state);
}
