#ifndef __UTILS_H
#define __UTILS_H

//#include <array>
#include <cmath>
#include <cstdlib>
//#include <fstream>
#include "config.h"


using namespace std;

// Converts degrees to radians.
#define radians(angleDegrees) (angleDegrees) //   angleDegrees * M_PI / 180.0)
 
// Converts radians to degrees.
#define degrees(angleRadians) (angleRadians) // * 180.0 / M_PI) 

#define toDegrees(angleRadians) (angleRadians * 180.0 / M_PI)

#define cosd(x) (cos(fmodf((x), 360) * M_PI / 180))
#define round(x) (floor(x + 0.5))

class utils
{
public:

//	template <typename T>
//	static array<T,2> vectorAdd(array<T,2> a, array<T,2> b);
	static void vectorAdd(float a[], float b[], float returnVec[]);

//	template <typename T>
//	static array<T,2> vectorDivide(array<T,2> a, float b);
	static void vectorDivide(float a[], float b, float returnVec[]);

//	template <typename T>
//	static float vectorDot(array<T,2> a, array<T,2> b);
	static float vectorDot(float a[], float b[]);

//	template <typename T>
//	static array<T,2> vectorMult(array<T,2> a, float);
	static void vectorMult(float a[], float b, float returnVec[]);

	static float myAtan(float x, float y);

	static float calcSigmaNorm(float* z);
	
	static float calcPhiAlpha(float z);
	static float calcRho(float z);
	static float calcPhi(float z);
	static float calcSigma1(float z);

	static float subtractHeadings(float a, float b);
	static float rand_float();
	static float round3(float a);
	static void vectorRound3(float vec[]);
};

#endif

