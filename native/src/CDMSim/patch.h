#ifndef __PATCH_H
#define __PATCH_H

#include "config.h"
#include "mbed.h"
#include <cmath>
#include <vector>

using namespace std;

class Patch
{
  	vector<float> centresX;   // mu/sigma pairs
  	vector<float> centresY;
  	vector<float> spreads;   
	vector<float> multipliers;
	
  public:  	
    
    Patch();
    void 	addAttractor(float centreX, float centreY, float spread);
  	float 	calcAttraction(float x, float y);
  	float	calcGaussian(float distance, float std);
  	void 	updateMultipliers(vector<float> newValues);
  	void	printDetails(Serial *pc);
};

#endif
