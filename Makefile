all: Convolve_code_v1.o Antenna_beam.o
	gcc -g -o Convolve_code_v1.out Convolve_code_v1.o GMOSS_functions.o Antenna_beam.o -lgsl -lgslcblas -lm
	rm -f *.o
	
Antenna_beam.o:
	gcc -c -o Antenna_beam.o Antenna_beam.c -lm
	
Convolve_code_v1.o: GMOSS_functions.o
	gcc -c -o Convolve_code_v1.o Convolve_code_v1.c -lgsl -lgslcblas -lm
	
GMOSS_functions.o:
	gcc -c -o GMOSS_functions.o GMOSS_functions.c -lgsl -lgslcblas -lm
	
clean:
	rm -f *.out
	rm -f *.o
