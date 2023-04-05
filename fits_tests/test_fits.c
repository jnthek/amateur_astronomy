#include "fitsio.h"  /* required by every program that uses CFITSIO  */
main()
{   /* Create a FITS primary array containing a 2-D image */
    fitsfile *fptr;       /* pointer to the FITS file; defined in fitsio.h */
    int status, ii, jj;
    long  fpixel, nelements, array[200][300], exposure;
    char filename[] = "atestfil.fit";             /* name for new FITS file */
    int bitpix   =  16;         /* 16-bit short signed integer pixel values */
    long naxis    =   2;        /* 2-dimensional image                      */
    long naxes[2] = { 300, 200 };   /* image is 300 pixels wide by 200 rows */
    status = 0;         /* initialize status before calling fitsio routines */

    if (fits_create_file(&fptr, filename, &status)) /* create new FITS file */
        return( status );

    /* Write the required keywords for the primary array image */
    if ( fits_create_img(fptr,  bitpix, naxis, naxes, &status) )
         return( status );

    /* Initialize the values in the image with a linear ramp function */
    for (jj = 0; jj < naxes[1]; jj++)
        for (ii = 0; ii < naxes[0]; ii++)
            array[jj][ii] = ii + jj;

    fpixel = 1;                               /* first pixel to write      */
    nelements = naxes[0] * naxes[1];          /* number of pixels to write */

    /* Write the array of long integers (after converting them to short) */
    if ( fits_write_img(fptr, TLONG, fpixel, nelements, array[0], &status) )
        return( status );

    /* Write another optional keyword; must pass the ADDRESS of the value */
    exposure = 1500.;
    if ( fits_write_key(fptr, TLONG, "EXPOSURE", &exposure,
         "Total Exposure Time", &status) )
         return( status );

    fits_close_file(fptr, &status);            /* close the file */
    return( status );
}

