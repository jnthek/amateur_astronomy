#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "GMOSS_constants.h"

void date2juliandate(int year, int month, int day, double *JD_out)
{
	long A,B,C_here,D;
	double JD;
		
	if (month==1 || month==2)
	{
		year--;
		month+=12;
	}	
	
	A = (int)(year/100);
	B = 2 - A + (int)(A/4);		
	C_here = (int)(365.25*year);
	D = (int)(30.6001*(month+1));	
	JD = (double)(B+C_here+D) + day + 1720994.5;
	*JD_out = JD;
}

void ut2gst(int year, int month, int day, int hours, int minutes, int seconds, double *GST_out)
{
	double JD, S, T, T0, GST, UT_decimal_hours;
	
	date2juliandate(year,month,day,&JD);
	//printf("JD is %f\n",JD);
		
	S = JD - 2451545.0; /* corresponding to epoch J2000 */
	T = S/36525.0;
	T0 = (6.697374558)+(2400.051336*T)+(0.000025862*T*T);
	
	if (T0 < 0)
		T0 = T0 + (24*(1+((int)abs(T0))/24));
	else
		T0 = T0 - (24*(((int)abs(T0))/24));
		
	UT_decimal_hours = (hours)+(minutes/(60.0))+(seconds/(60.0*60.0));	
	UT_decimal_hours *= 1.002737909;	
	GST = T0 + UT_decimal_hours;
	
	if (GST < 0)
		GST = GST + (24*(1+((int)abs(GST))/24));
	else
		GST = GST - (24*(((int)abs(GST))/24));
		
	*GST_out = GST;	
}
	
void localtime2lst(int local_year, int local_month, int local_day, int local_hours, int local_minutes, int local_seconds, double longitude, double zone_correction, double *LST_out)
{
	double GST, LST, local_decimal_hours, UT_decimal_hours, minutes_double, seconds_double;
	int year, month, day, hours, minutes, seconds;
	
	local_decimal_hours = (local_hours)+(local_minutes/(60.0))+(local_seconds/(60.0*60.0));
	UT_decimal_hours = local_decimal_hours - zone_correction;
		
	year = local_year;
	month = local_month;
	day = local_day;
	
	if (UT_decimal_hours < 0.0)
	{
		day -= 1;
		UT_decimal_hours += 24.0;			
	}	
	
	hours = floor(UT_decimal_hours);
	minutes_double = (UT_decimal_hours-hours)*60.0;
	minutes = floor(minutes_double);
	seconds_double = (minutes_double-minutes)*60.0;
	seconds = round(seconds_double);
		
	//printf("UT is %lf\n",UT_decimal_hours);
	//printf("UT is %d,%d,%d,%d,%d,%d \n",year,month,day,hours,minutes,seconds);
	 
	ut2gst(year,month,day,hours,minutes,seconds,&GST);	
	//printf("GST is %f\n", GST);
	
	LST = GST + ((longitude/360.0)*24.0);
	if (LST > 24.0)
		LST -= 24.0;
	else if(LST < 0.0)
		LST += 24.0;
		
	*LST_out = LST;
}

void horizon2equa(double LST, double latitude_degree, double azimuth_degree, double altitude_degree, double *alpha_degree_out, double *dec_degree_out)
{
	double azi_radian, alt_radian, lat_radian;
	double hour_angle_hours, hour_angle_radian, hour_angle_degree, alpha_hours, alpha_degree, dec_degree, dec_radian;
	
	azi_radian = azimuth_degree*PI/180.0;
	alt_radian = altitude_degree*PI/180.0;
	lat_radian = latitude_degree*PI/180.0;
	
	dec_radian = asin(sin(alt_radian)*sin(lat_radian) + cos(alt_radian)*cos(lat_radian)*cos(azi_radian));
	hour_angle_radian = acos((sin(alt_radian) - sin(lat_radian)*sin(dec_radian)) / (cos(lat_radian)*cos(dec_radian)));
	
	if (sin(azi_radian)>0.0)
		 hour_angle_radian = 2*PI - hour_angle_radian;
		 
	hour_angle_degree = hour_angle_radian*180.0/PI;
	hour_angle_hours = hour_angle_degree/15.0;
	
	alpha_hours = LST - hour_angle_hours;
	
	if (alpha_hours < 0.0)
		alpha_hours += 24.0;
	
	alpha_degree = alpha_hours*15.0;
	dec_degree = dec_radian*180.0/PI;
	
	*alpha_degree_out = alpha_degree;
	*dec_degree_out = dec_degree;	
}	

void equa2horizon (double LST, double latitude_degree, double alpha_degree, double dec_degree, double *azimuth_degree_out, double *altitude_degree_out)
{
	double dec_radian, lat_radian, alpha_hours, alt_radian, azi_radian, alt_degree, azi_degree;
	double hour_angle_hours, hour_angle_radian, hour_angle_degree;	
		
	alpha_hours = alpha_degree/15.0;
	
	hour_angle_hours = LST - alpha_hours;	
	if (hour_angle_hours < 0.0)
		hour_angle_hours += 24.0;
		
	dec_radian = dec_degree*PI/180.0;
	lat_radian = latitude_degree*PI/180.0;
	
	hour_angle_degree = hour_angle_hours*15.0;
	hour_angle_radian = hour_angle_degree*PI/180.0;
	
	alt_radian = asin(sin(dec_radian)*sin(lat_radian) + cos(dec_radian)*cos(lat_radian)*cos(hour_angle_radian));
	azi_radian = acos((sin(dec_radian) - sin(lat_radian)*sin(alt_radian)) / (cos(lat_radian)*cos(alt_radian)));
	
	if (sin(hour_angle_radian)>0.0)
		 azi_radian = 2*PI - azi_radian;
	
	alt_degree = alt_radian*180.0/PI;
	azi_degree = azi_radian*180.0/PI;
	
	*azimuth_degree_out = azi_degree;
	*altitude_degree_out = alt_degree;
}

void gal2equa(double b_degree, double l_degree, double *alpha_degree_out, double *dec_degree_out) 
{
	double alpha_radian, dec_radian, b_radian, l_radian, x, y;
	
	b_radian = b_degree*PI/180.0;
	l_radian = l_degree*PI/180.0;
	
	dec_radian = asin((cos(b_radian)*cos(0.4735)*sin(l_radian-0.575))+(sin(b_radian)*sin(0.4735)));
	
	y = cos(b_radian)*cos(l_radian-0.575);
	x = sin(b_radian)*cos(0.4735) - cos(b_radian)*sin(0.4735)*sin(l_radian-0.575);
	
	
	if (x>=0.0 && y>=0.0)
		alpha_radian = atan(y/x);
	else if (x<0.0 && y>=0.0)
		alpha_radian = atan(y/x) + PI;
	else if (x<0.0 && y<0.0)
		alpha_radian = atan(y/x) + PI;
	else if (x>=0.0 && y<0.0)
		alpha_radian = atan(y/x) + (2*PI);	
	
	alpha_radian += 3.355;	
	
	if(alpha_radian>=2*PI)
		alpha_radian-=2*PI;
	
	*alpha_degree_out = alpha_radian*180.0/PI;
	*dec_degree_out = dec_radian*180.0/PI;	
}

void equa2gal(double alpha_degree, double dec_degree, double *b_degree, double *l_degree) 
{
	double alpha_radian, dec_radian, b_radian, l_radian, x, y;  
	
	alpha_radian = alpha_degree*PI/180.0;
	dec_radian = dec_degree*PI/180.0;
	
	b_radian = asin((cos(dec_radian)*cos(0.4735)*cos(alpha_radian-3.355)) + sin(dec_radian)*sin(0.4735));
	
	y = sin(dec_radian) - sin(b_radian)*sin(0.4735);
	x = cos(dec_radian)*sin(alpha_radian-3.355)*cos(0.4735);
	
	if (x>=0.0 && y>=0.0)
		l_radian = atan(y/x);
	else if (x<0.0 && y>=0.0)
		l_radian = atan(y/x) + PI;
	else if (x<0.0 && y<0.0)
		l_radian = atan(y/x) + PI;
	else if (x>=0.0 && y<0.0)
		l_radian = atan(y/x) + (2*PI);	
	
	l_radian += 0.575;
	
	if(l_radian>=2*PI)
		l_radian-=2*PI;
	
	*b_degree = b_radian*180.0/PI;
	*l_degree = l_radian*180.0/PI;
}
