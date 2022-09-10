#include "memory_allocation.h"
#include <math.h>

#ifndef M_TAU
	#define M_TAU (M_PI * 2.0f)
#endif

//#include <stddef.h>
//#include <stdlib.h>




void init_fourier_transform(fourier_transform_state* state) {

	typeof(state->settings) settings = state->settings;

	for (int i=0; i<state->settings->bin->used; i++) {

		typeof(state->acc[i])* acc = &state->acc[i];
		typeof(state->settings->bin->data[i])* bin = &settings->bin->data[i];

		acc->accumulator = bin->start;
		acc->falloff = bin->falloff / settings->sample_rate;
		acc->advance =  M_TAU * bin->frequency / settings->sample_rate;
	}

}


// Need to add a window function for the summation
// Use a tail + head buffer for a rolling sum


void run_fourier_transform(fourier_transform_state* state, sample_buffer* input, frequency_buffer* output[]) {

	for (int i=0; i<input->used; i++) {
		for (int b=0; b<state->settings->bin->used; b++) {

			typeof(state->acc[b])* acc = &state->acc[b];
			typeof(input->data[i]) sample = input->data[i];

			acc->accumulator.x += sin(acc->phase) * sample;
			acc->accumulator.y += cos(acc->phase) * sample;

			acc->phase = fmod(acc->phase + acc->advance, M_TAU);



/*			output[b]->data[i].x = sin(acc->phase) * sample;
			output[b]->data[i].y = cos(acc->phase) * sample;
*/

			double x2 = acc->accumulator.x * acc->accumulator.x;
			double y2 = acc->accumulator.y * acc->accumulator.y;
			double d = x2 + y2;

			double s = d / 1.0;

			acc->accumulator.x *= (1.0 - s);
			acc->accumulator.y *= (1.0 - s);



			output[b]->data[i] = acc->accumulator;

		}
	}
}