all: read_fits

test_fits: test_fits.c
	@echo "Compiling FITS test code"
	gcc -Wall test_fits.c -o test_fits -I/usr/include/cfitsio/ -lcfitsio -lm

read_fits: read_fits.c
	@echo "Compiling FITS read test code"
	gcc -Wall read_fits.c -o read_fits -I/usr/include/cfitsio/ -lcfitsio -lm

clean : 
	rm -f test_fits
	rm -f read_fits

