#ifndef MEMORY_ALLOCATION_H

#include "ft1.h"

frequency_buffer* allocate_frequency_buffer(int size);
sample_buffer* allocate_sample_buffer(int size);
frequency_bin_settings_buffer* allocate_frequency_bin_settings_buffer(int size);
fourier_transform_state* allocate_fourier_transform(fourier_transform_settings* settings);

void free_frequency_buffer(frequency_buffer* buffer);
void free_sample_buffer(sample_buffer* buffer);
void free_frequency_bin_settings_buffer(frequency_bin_settings_buffer* buffer);
void free_fourier_transform(fourier_transform_state* state);


#endif
#define MEMORY_ALLOCATION_H