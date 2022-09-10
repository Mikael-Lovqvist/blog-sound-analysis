
ft1.so: ft1.o memory_allocation.o test_waveforms.o
	gcc -flto --shared -fPIC $? -o $@

ft1.o: ft1.c
	gcc -c -flto -march=native -Os $< -o $@

test_waveforms.o: test_waveforms.c
	gcc -c -flto -march=native -Os $< -o $@


memory_allocation.o: memory_allocation.c
	gcc -c -flto -march=native -Os $< -o $@


clean:
	rm ft1.o memory_allocation.o test_waveforms.o ft1.so

.PHONY: clean