#include "fitsio.h" 
#include <assert.h>
int main(void)
{  
    fitsfile *fptr;      
    int status, res;
    char filename[] = "atestfil.fit";            
    char comment[100];
    long exposure;
    status = 0;      

    res = fits_open_file(&fptr, filename, READONLY, &status);
    assert (res==0);

    res = fits_read_key (fptr, TLONG, "EXPOSURE", &exposure, comment, &status);
    assert (res==0);

    printf("%ld, %s\n", exposure, comment);
    fits_close_file(fptr, &status);            /* close the file */
    return (status);
}

