#include "cdm_init.h"
extern "C" {
  CDM_Init* createCDM() {
    CDM_Init* cdmInit = new CDM_Init();
    cdmInit->initialise_cdm();
    return cdmInit;
  }
  
  bool setRgbReadings(CDM_Init* cdm, int r, int g, int b) {
    cdm->rgb_readings[RED]	= r;
    cdm->rgb_readings[GREEN]	= g;
    cdm->rgb_readings[BLUE]	= b;
    return true;
  }

  int* getRgbReadings(CDM_Init* cdm) {
    static int returnArr[3];
    returnArr[0] = cdm->rgb_readings[RED];    
    returnArr[1] = cdm->rgb_readings[GREEN];    
    returnArr[2] = cdm->rgb_readings[BLUE];    
    return returnArr;
  }
  
  float* getChargeTemp(CDM_Init* cdm) {
    static float returnArr[2];
    returnArr[0] = cdm->get_charge_reading();
    returnArr[1] = cdm->get_temp_reading();
    return returnArr;
  }

  bool* getCDMOutput(CDM_Init* cdm) {
    static bool returnArr[2];
    returnArr[0] = cdm->get_want_charge();
    returnArr[1] = cdm->get_avoid_temp();
    return returnArr;
  }


  bool tick(CDM_Init* cdm)  {
    cdm->cdm_ticker_func();
    return true;
  }

  bool destroyCDM(CDM_Init* cdm) {
    delete cdm;
    return true;
  }

  int getNumAgents(CDM_Init* cdm) {
    return cdm->get_num_agents();
  }

  float* getCurrentXY(CDM_Init* cdm) {
    vector<Agent*> agents = cdm->get_agents();
    static float returnArr[45];
    for (int a = 0; a < 45; a+=3) {
      Agent *thisAgent 	= agents[a/3];
      returnArr[a]     	= thisAgent->xcor;
      returnArr[a + 1] 	= thisAgent->ycor;
      returnArr[a + 2]  = thisAgent->heading;
    }
    return returnArr;    
  }

/*
  float* getCurrentXY(CDM_Init* cdm) {
    // yes, I'm aware how awful this memory management is, but I don't care right now
    vector<Agent*> agents = cdm->get_agents();
    int numAgents = agents.size();
    float* returnArr = (float*)malloc(sizeof(float) * numAgents * 2);
    for (int a = 0; a < numAgents * 2; a+=2) {
      Agent *thisAgent 	= agents[a/2];
      returnArr[a]     	= thisAgent->xcor;
      returnArr[a + 1] 	= thisAgent->ycor;
    }
    return returnArr;
  }
*/

}

