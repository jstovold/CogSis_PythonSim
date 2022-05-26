#ifndef __AGENT_H
#define __AGENT_H

//#include <iostream>
#include <vector>
//#include <array>
//#include <algorithm>
#include <math.h>
#include "utils.h"
#include "patch.h"
#include "config.h"
using namespace std;

class CDM;
class Agent
{

	
	void calcFg();
	void calcFgamma(float aveHeading);
	void calcFchem();
	void calcVirtualGoalPos(float aveHeading, float returnVal[]);
 	float calcAveHeading();
	float calcChemMultiplier();
	
	float attractionHere();
	float attractionAt(float dX, float dY);
	
	float distanceToGoal();
	float directionToGoal();
//	float headingToAgent(Agent *a);

    public:
	    //float vision;
		float xcor, ycor, heading, magnitude, direction, maxSpeed, attrDivisor, prevAveHeading;//, dx, dy;//, oldxcor, oldycor;
		float fg[2];
		float fgamma[2];
		float fchem[2];
		float virtualGoal[2]; 
	
		int id;
		vector<Agent*> neighbours;
		Agent* nearestNeighbour;
		CDM *environment;
		

    	Agent(int, CDM *environment, float vision);	 	// constructor
    	void placeAgent(float x, float y, float heading);
		void updateNeighbourhood();
		void flock();
		void calcLattice();
	
		// helper functions:
		float distanceToXY(float x, float y);
		float distanceToAgent(Agent *a);
		float directionToAgent(Agent *a);
	
		void turnTowards(float desiredDirection);
		void turnAwayFrom(Agent *a);

};

#include "cdm.h"

#endif

