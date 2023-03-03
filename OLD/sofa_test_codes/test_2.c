#include <stdio.h>
#include <sofa.h>
#define PI 3.14159265
#define deg2rad(angleDegrees) (angleDegrees * PI / 180.0)
#define rad2deg(angleRadians) (angleRadians * 180.0 / PI)

int main(void)
{
	double gal_longitude, gal_latitude, RA, dec; //Everything in radian
	int iy, im, id, ihr, imn;
	double sec;
	double utc1, utc2;
	double site_longitude, site_latitude, elong, phi;
	double azi_obs, zenith_dist_obs, hob, dob, rob, eo;
	
	iy = 2018;
	im = 3;
	id = 9;
	ihr = 15; //Time in UTC
	imn = 51;
	sec = 27;
	
	iauDtf2d("UTC", iy, im, id, ihr, imn, sec, &utc1, &utc2); //UTC Date and time fields into 2-part quasi-JD form
	
	site_longitude = 77.5946; // For Bangalore
	site_latitude = 12.9716;	
	elong = deg2rad(site_longitude);
	phi = deg2rad(site_latitude);
	
	gal_longitude = deg2rad(-150.7588); //Galactic Longitude
	gal_latitude = deg2rad(-25.24533); //Galactic Latitude	
	
	iauG2icrs (gal_longitude, gal_latitude, &RA, &dec); //Galactic to ICRS (or RA,Dec if you will)		
	printf("RA = %lf \nDec = %lf\n",rad2deg(RA),rad2deg(dec));
	
	iauAtco13(RA, dec, 0.0, 0.0, 0.0, 0.0,
              		utc1, utc2, 0.277,
              		elong, phi, 0.0, 0.0, 0.0,
              		1013, 27.0, 50.0, 1e6,
              		&azi_obs, &zenith_dist_obs, &hob, &dob, &rob, &eo); // This works, cross checked with Stellarium computations
              		
        printf("Azimuth = %lf\nElevation = %lf\n",rad2deg(azi_obs),90.0-rad2deg(zenith_dist_obs));
	
}
