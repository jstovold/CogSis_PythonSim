#include "cdm_init.h"

CDM *cdm;

#define CDM_SPEED 	1

#define EEPROM_OUTPUT           0
#define DEBUG_OUTPUT            1
#define BASIC_OUTPUT            1

// lighting thresholds for following lab setup:
// 1 blue spot
// 1 green/orange combo spot
// workshop lights ON
// lab lights OFF (except far ceiling lights on lowest level)
//#define CHARGING_THRESHOLD      450
//#define TEMPERATURE_THRESHOLD   250
#define RED_LIGHT_THRESHOLD     400
#define GREEN_LIGHT_THRESHOLD   100000          // reality gap... (non-perfect filters etc.)
#define BLUE_LIGHT_THRESHOLD    30000

// simulation environment (values between 0 and 255)
#define CHARGING_THRESHOLD      120
#define TEMPERATURE_THRESHOLD   100

// temperature and charge light colours
#define CHARGE_LIGHT_COLOUR     RED
#define TEMP_LIGHT_COLOUR       RED

// temperature and charge parameters
#define DISCHARGE_SPEED         0.02
#define CHARGING_SPEED          0.05
#define TEMP_INCREASE_SPEED     1.8
#define TEMP_DECREASE_SPEED     0.8

//Serial 	pc; // new Serial.h redirects this to a standard log file instead of the UART
int	numAgents;
bool	displaying;

float  	temperature;
float  	charge;

bool    cooling;
bool 	charging;

bool  	highTemp;
bool 	avoidTemp;
bool 	needCharge;
bool	wantCharge;

int  	cLED;

vector<float> 	cdm_sensorValues;

CDM_Init::~CDM_Init() {
 delete pc;
}

void init_local()
{
  numAgents 	= 15;
  temperature 	= 20.0f;
  charge	= 5.0f;
  highTemp	= false;
  avoidTemp	= false;
  needCharge	= false;
  wantCharge	= false;

  cdm_sensorValues.push_back(0.0);  
  cdm_sensorValues.push_back(0.0);  
}

void CDM_Init::initialise_cdm() {
  init_local(); 	// this file
  init_CDM_workspace(); // config.cpp

  pc = new Serial("outputlog.log");
  pc->printf("CDM_Init::initialise_cdm();\r\n");

  cdm = new CDM(60,60,numAgents, pc);
  cdm->placeAgents(15, 30, 2.0, 0);

  // set up the environment, link to sensors...
  vector<float> sensorValues;
  temperature = 10.0f;
  charge      = 5.0f;
  sensorValues.push_back(temperature);
  sensorValues.push_back(charge);
  cdm->initializeEnvironment(2, sensorValues);
  charge      = 3.0f;
  temperature = 20.0f;

  // print out the environment to show that we are set up and ready to go
  printEnv();
}

void CDM_Init::printEnv() {
  displaying = true;
  cdm->displayEnvironment(60, 60, pc);
  displaying = false;
}

// this function is called every tick from NetLogo, CDM_SPEED defines how much faster the CDM runs than the NetLogo sim
void CDM_Init::cdm_ticker_func() {
    charge_ticker_func();
    temperature_ticker_func();

    pc->printf("CDM_Init::cdm_ticker_func();\r\n");
    cdm_sensorValues[0] = temperature;
    cdm_sensorValues[1] = charge;
    cdm->updateEnvironment(cdm_sensorValues);
    cdm->go(CDM_SPEED, pc);

    if (DEBUG_OUTPUT) {pc->printf("Timestep:\t%d\r\n", cdm->timestep);}

    int tempNum     = cdm->countNumberAgentsInRadius(30,15, 7);
    int chargeNum   = cdm->countNumberAgentsInRadius(30,45, 7);
    int noneNum     = cdm->countNumberAgentsInRadius(30,30, 15);

    if ((BASIC_OUTPUT || DEBUG_OUTPUT) && !displaying) 
    { 
	pc->printf("timestep: %d\t tempNum: %d\t chargeNum:%d\t noneNum:%d\t temperature: %f\t charge: %f\r\n", 
		cdm->timestep, tempNum, chargeNum, noneNum, temperature, charge);
    }
    
    avoidTemp   = tempNum >= numAgents / 2;
    wantCharge  = chargeNum >= numAgents / 2;
    
    if (wantCharge)
    {
        cLED = BLUE;
    }
    if (avoidTemp)
    {
        cLED = GREEN;
    }

//    printEnv();	

    if (DEBUG_OUTPUT) {pc->printf("avoidTemp:\t%s\r\n", avoidTemp ? "true" : "false");}
    if (DEBUG_OUTPUT) {pc->printf("highTemp:\t%s\r\n", highTemp ? "true" : "false");}
    if (DEBUG_OUTPUT) {pc->printf("wantCharge:\t%s\r\n", wantCharge ? "true" : "false");}
    if (DEBUG_OUTPUT) {pc->printf("needCharge:\t%s\r\n", needCharge ? "true" : "false");}
  //  if (DEBUG_OUTPUT && (cdm->timestep % 5 == 0)) { printEnv(); }
}


void CDM_Init::charge_ticker_func()
{
    pc->printf("CDM_Init::charge_ticker_func();\r\n");
    // mimics the change in battery level based on our `charging station' and the never-ending march of time...

    // 0.02, 0.05
    charge = max ((float)(charge - DISCHARGE_SPEED), 0.01f);  // every second, reduce charge by this amount, even when we are charging...

    if (DEBUG_OUTPUT) {pc->printf("Charge level: %f\r\n", charge);}
    if (charge_light_level() > CHARGING_THRESHOLD)      // in charging station
    {
        charging = true;
        charge = min((float)(charge + CHARGING_SPEED), 6.0f);              // upper limit on charge
    }
    else
    {
        charging = false;
    }

    needCharge = charge < 2.5f;

    if (needCharge)
    {
        cLED     = RED;
    }

    if (charge < 0.1f)
    {
        // out of battery
        //piswarm.play_tune("MS>DRCRD", 5);
        //piswarm.set_oled_colour(255,0,0);
        //all_oleds(255);
        //piswarm.forward(0.0f);
        if (!BASIC_OUTPUT && !DEBUG_OUTPUT) { } //wait(35.0f);}
        else {pc->printf("Waiting...");}
    }

}


void CDM_Init::temperature_ticker_func()
{
    pc->printf("CDM_Init::temperature_ticker_func();\r\n");
    // as with charge_ticker_func, but inverted
    temperature = max((float)(temperature - TEMP_DECREASE_SPEED), 10.0f);      // minimum temperature of 10...
    if (DEBUG_OUTPUT) {pc->printf("Temperature: %f\r\n", temperature); }
    if (temperature_light_level() > TEMPERATURE_THRESHOLD)
    {
        temperature = min((float)(temperature + TEMP_INCREASE_SPEED), 60.0f);       // maximum of 50...
        cooling = false;
    }
    else
    {
        cooling = true;
    }

    if (temperature > 25.0f)
    {
        highTemp = true;

        if (temperature > 30.0f)
        {
            if (temperature > 35.0f)
            {
                if (temperature > 40.0f)
                {
                    if (temperature > 45.0f)
                    {
                        if (temperature > 50.0f)
                        {
                            if (temperature > 55.0f)
                            {
//                                if (temperature >= 60.0f)
//                                {
                                    // too hot.
                                    //piswarm.play_tune("MS>DRCRD", 5);
                                    //piswarm.set_oled_colour(0,0,255);
                                    //all_oleds(255);
                                    //piswarm.forward(0.0f);
                                    if (!BASIC_OUTPUT && !DEBUG_OUTPUT) {}//wait(35.0f);}
                                    else {pc->printf("Waiting...");}
//                                }
//                                else
//                                {
//                                    piswarm.play_tune("MS>GRRRR", 5);
//                                }
                            }
                            else
                            {
                               // piswarm.play_tune("MS>FRRRR", 5);

                            }
                        }
                        else
                        {
                           // piswarm.play_tune("MS>ERRRR", 5);

                        }
                    }

                    else
                    {
                       // piswarm.play_tune("MS>DRRRR", 5);
                    }
                }
                else
                {
                    // 35
                    //piswarm.play_tune("MS>CRRRR", 5);
                }
            }
            else
            {
                // 30
                //piswarm.play_tune("MSBRRRR", 5);
            }
        }
        else
        { // 25
            //piswarm.play_tune("MSARRRR", 5);
        }
    }
    else
    {
        highTemp = false;
    }
}



int CDM_Init::charge_light_level()
{
    switch (CHARGE_LIGHT_COLOUR)
    {
        case RED:
            return get_current_red_value();
        case GREEN:
            return get_current_green_value();
        case BLUE:
            return get_current_blue_value();
        default:
            return 0;
    }
}

int CDM_Init::temperature_light_level()
{
    switch (TEMP_LIGHT_COLOUR)
    {
        case RED:
            return get_current_red_value();
        case GREEN:
            return get_current_green_value();
        case BLUE:
            return get_current_blue_value();
        default:
            return 0;
    }
}


int CDM_Init::get_current_red_value() {
  return rgb_readings[RED]; // red
}

int CDM_Init::get_current_green_value() {
  return rgb_readings[GREEN];
}

int CDM_Init::get_current_blue_value() {
  return rgb_readings[BLUE];
}

float CDM_Init::get_charge_reading() {
  pc->printf("CDM_Init::get_charge_reading(); \r\n");
  return charge;
}

float CDM_Init::get_temp_reading() {
  pc->printf("CDM_Init::get_temp_reading(); \r\n");
  return temperature;
}


int CDM_Init::get_num_agents() {
  return cdm->agents.size();
}

vector<Agent*> CDM_Init::get_agents() {
  return cdm->agents;
}

bool CDM_Init::get_want_charge() {
  return wantCharge;
}

bool CDM_Init::get_avoid_temp() {
  return avoidTemp;
}

