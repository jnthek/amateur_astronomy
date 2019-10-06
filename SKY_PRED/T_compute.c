#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sofa.h>
#include "GMOSS_functions.h"

#define PI 3.14159265
#define deg2rad(angleDegrees) (angleDegrees * PI / 180.0)
#define rad2deg(angleRadians) (angleRadians * 180.0 / PI)

double Antenna_beam(double theta_degree, double phi_degree);

int read_pixel_coordinates(double * lat_coordinate_here, double * lon_coordinate_here)
{
	double latitude,longitude,sky_val_temp;
	int i;
	char buf[100];	
	FILE *fp=NULL;
	
	fp=fopen("PIXEL_LISTING_NESTED_R4_GALACTIC.txt","r");
	if (fp==NULL)
	{
		return 0;		
	}
	
	fscanf(fp,"%s",buf);
	fscanf(fp,"%s",buf);	
	for (i=0;i<3072;i++)
	{
		fscanf(fp,"%lf",&longitude);
		fscanf(fp,"%lf",&latitude);
		lat_coordinate_here[i]=latitude;
		lon_coordinate_here[i]=longitude;
	}
	fclose(fp);
	fp=NULL;
}

int main(void)
{
	system("clear");
	
	//struct temperature_map_struct temperature_map;	
	int year, month, day, hour, minute, second;
	int status, i, freq_index, some_index;	
	double gal_lat_coordinate[3072], gal_lon_coordinate[3072], g_lat, g_lon;	
	double LST, zone_correction;	
	double azimuth, altitude, theta_degree, phi_degree, theta_radian;
	double utc1, utc2;
	double alpha, dec, gal_longitude, gal_latitude;
	double freq, pixel_intensity, antenna_power, beam_solid_angle;
	float sky_val;
	
	double site_longitude, site_latitude, elong, phi;
	double azi_obs, zenith_dist_obs, hob, dob, rob, eo;
	
	FILE *fp = NULL;
	FILE *f_out = NULL;
	
	status = read_pixel_coordinates(gal_lat_coordinate,gal_lon_coordinate);
	
	year = 2018;
	month = 3;
	day = 21;
	
	hour = 00;
	minute = 00;
	second = 00;
		
	site_longitude = 77.5946; // For Bangalore
	site_latitude = 12.9716;
	elong = deg2rad(site_longitude);
	phi = deg2rad(site_latitude);
		
	zone_correction = 5.0+(30.0/60.0);
	
	f_out = fopen("Antenna_power_24hr.txt","w");	
	fclose(f_out);	
	
	for (hour=0; hour<24; hour+=1)
	{			
		antenna_power = 0.0;
		beam_solid_angle = 0.0;
				
		fp = fopen("map_150_r4_5deg_nested_galactic_Kelvin.txt","r");
		iauDtf2d("UTC", year, month, day, hour, minute, second, &utc1, &utc2); //UTC Date and time fields into 2-part quasi-JD form	
		
		for (i=0; i<3072; i++)
		{
			fscanf(fp,"%f",&sky_val);
			
			gal_longitude = deg2rad(gal_lon_coordinate[i]); //Galactic Longitude
			gal_latitude = deg2rad(gal_lat_coordinate[i]); //Galactic Latitude	
	
			iauG2icrs (gal_longitude, gal_latitude, &alpha, &dec); //Galactic to ICRS (or RA,Dec if you will)		
			iauAtco13(alpha, dec, 0.0, 0.0, 0.0, 0.0,
              				utc1, utc2, 0.277,
              				elong, phi, 0.0, 0.0, 0.0,
              				1013, 27.0, 50.0, 1e6,
              				&azi_obs, &zenith_dist_obs, &hob, &dob, &rob, &eo); //RA,Dec to azimuth and zenith distance
              		
              		//Upto here, code is tested OK
              				  
			theta_radian = zenith_dist_obs;
				
			theta_degree = rad2deg(theta_radian);
			phi_degree = rad2deg(azi_obs);	
			
			antenna_power += sky_val*Antenna_beam(theta_degree,phi_degree)*sin(theta_radian); 
			beam_solid_angle += Antenna_beam(theta_degree,phi_degree)*sin(theta_radian);		
				
		}
		fclose(fp);
		antenna_power /= beam_solid_angle;	
		
		localtime2lst(year, month, day, hour, minute, second, site_longitude, zone_correction, &LST);		
		printf("%f,%f\n", antenna_power, LST);			
		
		f_out = fopen("Antenna_power_24hr.txt","a");		
		fprintf(f_out,"%.15e ", antenna_power);
			
		fprintf(f_out,"\n");
		fclose(f_out);
		
	}
	return 0;
}
