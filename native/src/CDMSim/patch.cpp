#include "patch.h"

	Patch::Patch()
	{
		centresX.clear();
		centresY.clear();
		spreads.clear();
		multipliers.clear();
	}

	void Patch::addAttractor(float centreX, float centreY, float spread)
	{
		centresX.push_back(centreX);
		centresY.push_back(centreY);	
		spreads.push_back(spread);
		multipliers.push_back(1.0f);
	}
	
	float Patch::calcAttraction(float xcor, float ycor)
	{
		float thisVal = 0.0f;
		for (int a = 0; a < centresX.size(); a++)
		{
		  int diffX 		= xcor - centresX[a];
		  int diffY 		= ycor - centresY[a];
		  float thisDist 	= sqrt(pow(static_cast<float>(diffX),2) + pow(static_cast<float>(diffY), 2));
		  thisVal 			+= multipliers[a] * (20 * calcGaussian(thisDist, spreads[a]));
		}
		return thisVal;
	}
	
	float Patch::calcGaussian(float distance, float std)
    {
		float power 		= - pow(distance, 2) / (2 * pow(std, 2));
		float numerator 	= exp(power);
		float denominator 	= std * sqrt(2 * PI);
		return numerator / denominator;
    }

	void Patch::updateMultipliers(vector<float> newValues)
	{
		multipliers.clear();
		for (int i = 0; i < newValues.size(); i++)
		{
			multipliers.push_back(newValues[i]);
		}
	}
	
	void Patch::printDetails(Serial *pc)
	{
		for (int i = 0; i < multipliers.size(); i++)
		{
			pc->printf("Multiplier %i:\t%f\r\n", i, multipliers[i]);
		}
	}

