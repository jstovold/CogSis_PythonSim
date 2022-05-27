#ifndef __CDM_H
#define __CDM_H

#include "mbed.h"
#include <vector>
#include <string>
#include "utils.h"
#include "agent.h"
#include "config.h"
using namespace std;

class Patch;

class CDM
{
	void moveAgentForward(Agent *a, float distance);	
	vector<float> calibrationValues;
  public:
	Patch*		patch;

	long 		timestep;
	int		numAgents;
	vector<Agent*> 	agents;

	CDM(int width, int height, int numAgents, Serial *pc);
	void placeAgents(float centreX, float centreY, float radius, float heading);
	void setupChemGradient(float centreX, float centreY, float radius);

	void getNeighbours();
	void moveAgents(int a);
	void go(int numTicksToGoFor, Serial *pc);
	void tick();

	vector<Agent*>* getAllAgentsInRadius(float radius, bool includeMe, int id);
	vector<Agent*>* getOtherAgentsInRadius(float radius, int id);
	int countNumberAgentsInRadius(float centreX, float centreY, float radius);
	Agent* getClosestAgentInRadius(float radius, int id);

	void displayEnvironment(int xlimit, int ylimit, Serial* pc); 
	void printAllAgentXYPos(Serial *pc); 

	void updateEnvironment(vector<float> sensorValues);
	void initializeEnvironment(int, vector<float>);
	void calibrateSensorValues(vector<float>);
	
	
};

#endif
