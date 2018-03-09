#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "GMOSS_constants.h"
#include "GMOSS_functions.h"

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
	double gal_lat_coordinate[3072],gal_lon_coordinate[3072], g_lat, g_lon;	
	double latitude,longitude, LST, zone_correction;	
	double azimuth, altitude, theta_degree, phi_degree, theta_radian;
	double alpha, dec;
	double freq, pixel_intensity, antenna_power, beam_solid_angle;
	float sky_val;
	
	FILE *fp = NULL;
	FILE *f_out = NULL;
	
	status = read_pixel_coordinates(gal_lat_coordinate,gal_lon_coordinate);
	
	year = 2017;
	month = 9;
	day = 13;
	
	hour = 12;
	minute = 00;
	second = 00;
		
	latitude = 30;
	/*longitude = 77.63245;
	zone_correction = 5.0+(30.0/60.0);*/
	
	f_out = fopen("Antenna_power_24hr_LST.txt","w");	
	fclose(f_out);
	
	//localtime2lst(year, month, day, hour, minute, second, longitude, zone_correction, &LST);
	
	for (LST=0.0; LST<24.0; LST+=1.0)
	{			
		antenna_power = 0.0;
		beam_solid_angle = 0.0;
				
		fp = fopen("map_150_r4_5deg_nested_galactic_Kelvin.txt","r");
		//rewind(fp);
   		for (i=0; i<3072; i++)
		{
			fscanf(fp,"%f",&sky_val);
			//printf("%f\n",sky_val);
			
			gal2equa(gal_lat_coordinate[i], gal_lon_coordinate[i], &alpha, &dec);			
			equa2horizon(LST, latitude, alpha, dec, &azimuth, &altitude);
				
			theta_degree = (90.0 - altitude);
			theta_radian = theta_degree*PI/180.0;	
			phi_degree = azimuth;	
			antenna_power += sky_val*Antenna_beam(theta_degree,phi_degree)*sin(theta_radian); //some error here !!!!!!!!!
			printf("%f\n", antenna_power);		
			beam_solid_angle += Antenna_beam(theta_degree,phi_degree)*sin(theta_radian);		
				
		}
		fclose(fp);
		
		antenna_power /= beam_solid_angle;			
		//printf("%f\n", antenna_power);			
		
		f_out = fopen("Antenna_power_24hr_LST.txt","a");		
		fprintf(f_out,"%.15e ", antenna_power);
			
		fprintf(f_out,"\n");
		fclose(f_out);
		
	}
	return 0;
}
