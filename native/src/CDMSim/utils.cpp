#include "utils.h"
//#include <iostream>
//float rSigma = utils::calcSigmaNorm(rNorm);
//float dSigma = utils::calcSigmaNorm(dNorm);


void utils::vectorAdd(float a[2], float b[2], float c[2])
{
	
	c[0] = a[0] + b[0];
	c[1] = a[1] + b[1];
//	return c;
}

//template <typename T>
//array<T,2> utils::vectorDivide(array<T,2> a, float b)
void utils::vectorDivide(float a[2], float b, float c[2])
{
	c[0] = a[0] / b;
	c[1] = a[1] / b;
}

//template <typename T>
//float utils::vectorDot(array<T,2> a, array<T,2> b)
float utils::vectorDot(float a[2], float b[2])
{
	float c;
	c = a[0] * b[0] + a[1] * b[1];
	return c;
}

//template <typename T>
//array<T,2> utils::vectorMult(array<T,2> a, float b)
void utils::vectorMult(float a[2], float b, float c[2])
{
	c[0] = a[0] * b;
	c[1] = a[1] * b;
}

float utils::myAtan(float x, float y)
{
	if (x == 0 && y == 0)
	{
	  return 0;
	}
	else
	{
	  return fmodf(atan2(y,x), 2 * PI);
	}
}

float utils::calcSigmaNorm(float z[2])
{ 
	float magSq 	 = pow(z[0], 2) + pow(z[1], 2);
	float magSqPrime = magSq * eps + 1;
	return (1 / eps) * (sqrt(magSqPrime) - 1);
}

float utils::calcPhiAlpha(float z)
{
	return calcRho(z / rSigma) * calcPhi(z - dSigma);
}

float utils::calcRho(float z)
{
	if (z < h)
	{
	  return 1;
	}
	else if (z <= 1)
	{
	  return 0.5 * (1 + cos((PI * (z - h) / (1 - h) )));
	}	
	else
	{
	  return 0;
	}
}

float utils::calcPhi(float z)
{
	float sig = calcSigma1(z + c);
	return 0.5 * ((a + b) * sig + (a - b));
}

float utils::calcSigma1(float z)
{
	return (z / sqrt(1 + pow(z, 2)));
}

float utils::subtractHeadings(float a, float b)
{
	// this needs to work using radians...
	if (true)
	{
		float diff = a - b;
		if (diff > PI)
		{
		  diff -= 2 * PI;
		}
		else if (diff < -PI)
		{
		  diff += 2 * PI;
		}
		
		return diff;



	}
	else
	{

		float diff = a - b;
		if (diff > 180)
		{
		  diff -= 360;
		}
		else if (diff < -180)
		{
		  diff += 360;
		}
		
		return diff;
	}
}

float utils::rand_float()
{
    return static_cast <float> ( rand() ) / static_cast <float> ( RAND_MAX );
}



float utils::round3(float a)
{
	return a;
//	return roundf(a * 1000) / 1000;
}


void utils::vectorRound3(float vec[])
{
	vec[0] = round3(vec[0]);
	vec[1] = round3(vec[1]);
}
