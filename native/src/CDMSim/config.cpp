//#include "config.h"
//#include <array>
#include <math.h>
#include "utils.h"
using namespace std;

float eps;
float a;
float b;
float c;
float d;
float r;
float rNorm[2];
float dNorm[2];

float h;
float c1;
int virtualGoalUpdateRate;
int distanceToVirtualGoal;
bool useRefractoryPeriod;

float highAttractThreshold;
int chemMult;

float maxTurn;
float agentVision;
float rSigma;
float dSigma;
vector <float> randomVal_v;
int randomCounter;

int arenaWidth;
int arenaHeight;

void init_CDM_workspace()
{

	eps = 0.5f;
	a = 5;
	b = 5;
	c = fabs(a - b) / sqrt(4 * a * b);
	d = 2.5; //1.0; //.5;
	r = 1.2 * d;
	rNorm[0] = r;
	rNorm[1] = 0;
	dNorm[0] = d;
	dNorm[1] = 0;

	h = 0.5;
	c1 = -1.0;
	virtualGoalUpdateRate = 25;
	distanceToVirtualGoal = 30;

	useRefractoryPeriod = true;

	highAttractThreshold = 0.3;
	chemMult = 185;

	maxTurn = 3.5 * PI / 180.0; //3.5;
//	agentVision = 2.0f;
	agentVision = 8.4f;

//	randomVal_v.reserve(200);
	//utils::setup_rand();
	//randomCounter = 0;

	rSigma = utils::calcSigmaNorm(rNorm);
	dSigma = utils::calcSigmaNorm(dNorm);
	arenaWidth = 140;
	arenaHeight = 140;	
}

