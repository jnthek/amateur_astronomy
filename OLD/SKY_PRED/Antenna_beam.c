#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define PI 3.14159265

double Antenna_beam(double theta_degree, double phi_degree)
{
	double P, theta_radian;
	
	if(theta_degree<=90.0 && phi_degree>=0.0)
	{
		theta_radian = theta_degree*PI/180.0;
		P = cos(theta_radian)*cos(theta_radian);		
	}
	else
	{
		P=0.0;
	}
	return P;
}
