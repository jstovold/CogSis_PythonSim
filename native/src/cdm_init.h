#ifndef __CDM_INIT_H
#define __CDM_INIT_H

#include "Serial.h"
#include "CDMSim/config.h"
#include "CDMSim/cdm.h"

using namespace std;

class CDM;

class CDM_Init 
{
    Serial* pc;

  public:
    ~CDM_Init();
    float get_charge_reading();
    float get_temp_reading();
    volatile int rgb_readings[4];
    int charge_light_level();
    int temperature_light_level();

    int get_current_red_value();
    int get_current_green_value();
    int get_current_blue_value();

    void initialise_cdm();
    void cdm_ticker_func();
    void charge_ticker_func();
    void temperature_ticker_func();
    void printEnv();

    int get_num_agents();
    vector<Agent*> get_agents();
};


#endif
