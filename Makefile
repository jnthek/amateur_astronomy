all: T_compute.o Antenna_beam.o
	gcc -g -o T_compute.out T_compute.o GMOSS_functions.o Antenna_beam.o -lgsl -lgslcblas -lsofa_c -lm 
	rm -f *.o
	
Antenna_beam.o:
	gcc -c -o Antenna_beam.o Antenna_beam.c -lm
	
T_compute.o: GMOSS_functions.o
	gcc -c -o T_compute.o T_compute.c -lgsl -lgslcblas -lm
	
GMOSS_functions.o:
	gcc -c -o GMOSS_functions.o GMOSS_functions.c -lgsl -lgslcblas -lm
	
clean:
	rm -f *.out
	rm -f *.o
