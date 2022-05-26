
#ifndef __CONFIG_H
#define __CONFIG_H
#define PI (3.141592653589793)

//#include <array>
#include <cmath>
#include <vector>

using namespace std;
/*
extern const float eps = 0.5f;
extern const float a = 5;
extern const float b = 5;
extern const float c = fabs(a - b) / sqrt(4 * a * b);
extern const float d = 2.5;
extern const float r = 1.2 * d;
extern const array<float, 2> rNorm = {r, 0};
extern const array<float, 2> dNorm = {d, 0};

extern const float h = 0.5;
extern const float c1 = -1.0;
extern const int virtualGoalUpdateRate = 25;
extern const int distanceToVirtualGoal = 30;

extern const bool useRefractoryPeriod = false;

extern const float highChemThreshold = 0.2;
extern const int chemMult = 185;

extern const float maxTurn = 3.5;
extern const float agentVision = 7.0f;
*/

/*
void setupVariables();

static float eps;
static float a;
static float b;
static float c;
static float d;
static float r;
static array<float, 2> rNorm;
static array<float, 2> dNorm;

static float h;
static float c1;
static int virtualGoalUpdateRate;
static int distanceToVirtualGoal;
static bool useRefractoryPeriod;

static float highChemThreshold;
static int chemMult;

static float maxTurn;
static float agentVision;


void setupVariables();

*/


extern float eps;
extern float a;
extern float b;
extern float c;
extern float d;
extern float r;
extern float rNorm[2];
extern float dNorm[2];

extern float h;
extern float c1;
extern int virtualGoalUpdateRate;
extern int distanceToVirtualGoal;
extern bool useRefractoryPeriod;

extern float highAttractThreshold;
extern int chemMult;

extern float maxTurn;
extern float agentVision;
extern float rSigma;
extern float dSigma;

extern int arenaWidth;
extern int arenaHeight;

//extern int randomCounter;
//extern vector<float> randomVal_v;
void init_CDM_workspace(void);

#endif
