/* PAWYC is Practical Astronomy with your Calculator*/

void date2juliandate(int year, int month, int day, double *JD_out);
/* This function converts a date to Julian Date, corresponding to 0h of UT. 
Uses algorithm from PAWYC page No: 7.
Assumes that the day is after 1582 October 15 in Gregorian Calendar */

void ut2gst(int year, int month, int day, int hours, int minutes, int seconds, double *GST_out);
/* This function converts UT to GST. Uses algorithm from PAWYC page No: 17. */

void localtime2lst(int local_year, int local_month, int local_day, int local_hours, int local_minutes, int local_seconds, double longitude, double zone_correction, double *LST_out);
/* This function accepts a local year,month,day and local time along with the zone correction to be applied. Gives out the LST corresponding to that longitude. */

void horizon2equa(double LST, double latitude_degree, double azimuth_degree, double altitude_degree, double *alpha_degree_out, double *dec_degree_out);
/* This function accepts coordinates in horizon system (i.e. azimuth and altitude in degrees) and gives out the coordinates in equatorial coordinates(i.e. RA and declination in degrees). Requires the LST and the latitude of the observatory.
Uses the algorithm in Pg. No: 38 of PAWYC. */

void equa2horizon(double LST, double latitude_degree, double alpha_degree, double dec_degree, double *azimuth_degree_out, double *altitude_degree_out);
/* This function accepts coordinates in equatorial coordinates(i.e. RA and declination in degrees) and gives out the coordinates in horizon system (i.e. azimuth and altitude in degrees). Requires the LST and the latitude of the observatory. 
Uses the algorithm in Pg. No: 36 of PAWYC. */

void gal2equa(double b, double l, double *alpha, double *dec);
/* This function accepts Galactic coordinates (i.e l and b) and converts them to equatorial coordinates (i.e. RA (alpha) and dec). Angles are in degrees.
Uses algorithm from PAWYC page No: 44*/

void equa2gal(double alpha, double dec, double *b, double *l);
/* This function accepts equatorial coordinates (i.e. RA (alpha) and dec) and converts them to Galactic coordinates (i.e l and b). Angles are in degrees.
Uses algorithm from PAWYC page No: 43*/





