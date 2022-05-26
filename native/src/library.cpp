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
  }

  bool tick(CDM_Init* cdm)  {
  }

  bool destroyCDM(CDM_Init* cdm) {
    delete cdm;
    return true;
  }

}

