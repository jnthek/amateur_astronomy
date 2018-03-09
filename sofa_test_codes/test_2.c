#include <stdio.h>
#include <sofa.h>
#define PI 3.14159265
#define deg2rad(angleDegrees) (angleDegrees * PI / 180.0)
#define rad2deg(angleRadians) (angleRadians * 180.0 / PI)

int main(void)
{
	double dl, db, dr, dd; //Everything in radian
	int iy, im, id, ihr, imn;
	double sec;
	double utc1,utc2;
	double longitude,latitude;	
	double elong,phi;
	double aob,zob,hob,dob,rob,eo;
	
	iy = 2018;
	im = 3;
	id = 9;
	ihr = 15; //Time in UTC
	imn = 51;
	sec = 00;
	
	longitude = 77.5946; // For Bangalore
	latitude = 12.9716;	
	elong = deg2rad(longitude);
	phi = deg2rad(latitude);
	
	dl = deg2rad(-150); //Galactic Longitude
	db = deg2rad(-25); //Galactic Latitude
	
	iauDtf2d("UTC", iy, im, id, ihr, imn, sec, &utc1, &utc2);
	iauG2icrs (dl, db, &dr, &dd); //Galactic to ICRS  or RA,Dec
		
	printf("RA = %lf \nDec = %lf\n",rad2deg(dr),rad2deg(dd));
	
	iauAtco13(dr, dd, 0.0, 0.0, 0.0, 0.0,
              		utc1, utc2, 0.277,
              		elong, phi, 0.0, 0.0, 0.0,
              		1013, 27.0, 50.0, 1e6,
              		&aob, &zob, &hob, &dob, &rob, &eo);
        printf("Azimuth = %lf\nElevation = %lf\n",rad2deg(aob),90.0-rad2deg(zob));
	
}
