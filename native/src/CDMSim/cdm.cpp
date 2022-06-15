#include "cdm.h"
#include <time.h>

    void CDM::moveAgentForward(Agent *a, float distance)
    {
		float dX 	= distance * cos(a->heading);
		float dY 	= distance * sin(a->heading); // -sin...
		
		if (a->xcor + dX >= arenaWidth)
		{
		  a->xcor 	= (a->xcor + dX) - arenaWidth;
		}
		else
		{
		  if (a->xcor + dX <= 0)
		  {
		    a->xcor = arenaWidth + (a->xcor + dX);
		  }
		  else
		  {
		    a->xcor = a->xcor + dX;
		  }
		}
	
		if (a->ycor + dY >= arenaHeight)
		{
		  a->ycor 	= (a->ycor + dY) - arenaHeight;
		}
		else
		{
		  if (a->ycor + dY <= 0)
		  {
		    a->ycor 	= arenaHeight + (a->ycor + dY);
		  }
		  else
		  {
		    a->ycor = a->ycor + dY;
		  }
		}
//
//		a->xcor = fmod((a->xcor + dX), arenaWidth);
//		a->ycor = fmod((a->ycor + dY), arenaHeight);
	
    }
    
    CDM::CDM(int width, int height, int agentCount, Serial *pc)
    {
		arenaWidth 	= width;
		arenaHeight	= height;
		numAgents	= agentCount;
		timestep	= 0l;

		pc->printf("CDM:\t basic assigns\r\n");
		agents.clear();
//		agents.reserve(numAgents);
		pc->printf("CDM:\t agents reserved\r\n");	
//		patches.clear();
		patch = new Patch();
		
		pc->printf("CDM:\t requesting ~%d bytes in memory space\r\n", arenaWidth * arenaHeight * (sizeof(Patch) + sizeof(short) + sizeof(float))); 
		
//		patches.reserve(arenaWidth * arenaHeight);
	//	pc->printf("CDM:\t patches reserved\r\n");	
		
		for (int a = 0; a < numAgents; a++)
		{
		  Agent *tempAgent = new Agent(a, this, agentVision);
		  agents.push_back(tempAgent);
		}
		pc->printf("CDM:\t agents assigned\r\n");
	//        struct timespec now;
	//
	//        clock_gettime(CLOCK_REALTIME, &now);
		srand( time(NULL) );
		return;
    }
	
    void CDM::placeAgents(float centreX, float centreY, float radius, float heading)
    {
	/*
    let x-plusminus floor (get-next-random 2)
    if (x-plusminus = 0)
    [ set x-plusminus -1 ]

    let y-plusminus floor (get-next-random 2)
    if (y-plusminus = 0)
    [ set y-plusminus -1 ]


    let randx (first centre) + ((get-next-random radius) * x-plusminus)
    let randy (last centre) + ((get-next-random radius) * y-plusminus)
    setxy randx randy

    set heading group-heading; + rand-heading     ;; little bit of variation in the heading
    set ave-heading heading
  ]
	for (int a = 0; a < numAgents; a++)
	{
	  Agent *thisAgent = agents[a];
	  float xy[2] = {0, 0};
	  bool conflict = true;

	  while (conflict)
	  {
	    generateXYPos(centreX, centreY, radius, xy);
	    float x = xy[0];
	    float y = xy[1];
	    if (a == 0)
	    {
	      conflict = false;	
	      thisAgent->placeAgent(x, y, heading);
	    }
	    else
	    {
	      conflict = false;
	      for (int aa = 0; aa < a; aa++)
	      {
		if ( (floor(x) == floor(agents[aa]->xcor)) && (floor(y) == floor(agents[aa]->ycor)) )
		{
		  conflict = true;
		  break;
		}

	      }
	      if (!conflict)
	      {
		  thisAgent->placeAgent(x,y,heading);
		  conflict = false;
	      }
	    
	    }
	  }
	}

	*/

	for (int a = 0; a < numAgents; a++)
	{
	  Agent *thisAgent = agents[a];
//	  float xy[2] = {0, 0};
	  int xplusminus 	= utils::rand_float() > 0.5 ? 1 : -1;
	  int yplusminus 	= utils::rand_float() > 0.5 ? 1 : -1;
	  float randx 		= utils::round3(centreX + ((utils::rand_float() * radius) * xplusminus));
	  float randy 		= utils::round3(centreY + ((utils::rand_float() * radius) * yplusminus));
	  thisAgent->placeAgent(randx, randy, heading);
	}

    }

    void CDM::setupChemGradient(float centreX, float centreY, float radius)
    {
		patch->addAttractor(centreX, centreY, radius);
    }


    void CDM::getNeighbours()
    {
		for (int a = 0; a < numAgents; a++)
		{
		  agents[a]->updateNeighbourhood();
		}
    }

    void CDM::moveAgents(int a)
    {
//	for (int a = 0; a < numAgents; a++)
//	{
	  Agent *thisAgent = agents[a];
	  thisAgent->turnTowards(utils::round3(thisAgent->direction));
	  moveAgentForward(thisAgent, utils::round3(min(thisAgent->magnitude, thisAgent->maxSpeed)));
//	}

    }

    void CDM::go(int numTicksToGoFor, Serial *pc)
    {
		for (int t = 0; t < numTicksToGoFor; t++)
		{
			for (int a = 0; a < numAgents; a++)
			{
		
				Agent *thisAgent = agents[a];
		      	thisAgent->updateNeighbourhood();
		    	thisAgent->flock();
		          //cout << setprecision(5) << timestep << "," << thisAgent->id << "," << thisAgent->xcor << "," << thisAgent->ycor << "," << thisAgent->magnitude << "," << thisAgent->heading << "," << thisAgent->direction << endl;
		
		    	moveAgents(a);
			}

		
			tick();	
		}
    }

    void CDM::tick()
    {
		timestep++;
    }

    vector<Agent*>* CDM::getAllAgentsInRadius(float radius, bool includeMe, int id)
    {
        
//        if (agents.empty() || id < 0 || id > numAgents) { return NULL; }


	Agent *thisAgent = agents.at(id);
//	float minX = thisAgent->xcor - radius;
//	float minY = thisAgent->ycor - radius;
//	float maxX = thisAgent->xcor + radius;
//	float maxY = thisAgent->ycor + radius;
//	


	vector<Agent*>* neighbours = new vector<Agent*>();
	for (int a = 0; a < numAgents; a++)
	{
	  if (includeMe) 
	  {
	    if (thisAgent->distanceToAgent(agents.at(a)) <= radius)
	    //if ((agents[a].xcor >= minX && agents[a].xcor <= maxX) && (agents[a].ycor >= minY && agents[a].ycor <= maxY) )
	    {
	      neighbours->push_back(agents.at(a));
	    }
	  }

	  if ( (!includeMe) && a != id)
	  {
	    if (thisAgent->distanceToAgent(agents.at(a)) <= radius)
	    {
	      neighbours->push_back(agents.at(a));
	    }
	  }
	}
	return neighbours;
    }

    vector<Agent*>* CDM::getOtherAgentsInRadius(float radius, int id)
    {
		return getAllAgentsInRadius(radius, false, id);
    }

    int CDM::countNumberAgentsInRadius(float centreX, float centreY, float radius)
    {
		int sum = 0;
		for (int a = 0; a < numAgents; a++)
		{
		  if (agents[a]->distanceToXY(centreX, centreY) <= radius)
		  {  sum++;  }
		}
		return sum;
    }

    Agent* CDM::getClosestAgentInRadius(float radius, int id)
    {
		vector<Agent*>* allAgentsInRadius = getOtherAgentsInRadius(radius, id);
		Agent *thisAgent = agents[id];
		if (allAgentsInRadius->size() > 0)
		{
		  int closest = -1;
		  float closestDist = numeric_limits<float>::max();
		  for (int a = 0; a < allAgentsInRadius->size(); a++)
		  {
		    float dist = thisAgent->distanceToAgent((*allAgentsInRadius)[a]);
		    if (dist < closestDist)
		    {
		      closest 		= a;
		      closestDist 	= dist;
		    }
		  }
		  return agents[closest];
		}

		return NULL;

    }

//
//    Patch *CDM::patchAtXY(float x, float y)
//    {
//	int patchID = (int) ( round(y) * arenaWidth + round(x) );
//	if (patchID <= patches.size())
//	{
//	  return &patches[patchID];
//	}
//	else
//	{
//	  return &patches[patchID - arenaWidth];
//	}
//    }

    void CDM::displayEnvironment(int xlimit, int ylimit, Serial *pc)
    {
    	pc->printf("displayEnvironment\r\n");
		vector<int> agentXYList;
		agentXYList.reserve(numAgents);
	
		for (int a = 0; a < numAgents; a++)
		{
		  agentXYList.push_back(floor(agents[a]->ycor) * arenaWidth + floor(agents[a]->xcor));
		}
		
		
		int width = min(xlimit, arenaWidth);
	//	*pc << "max:\t" << maxChemVal << " fchem:\t" << agents[0].fchem[0] << "," << agents[0].fchem[1] << endl;
		string topLine = string(2 * width, '-');
		//*pc << "  " << topLine << endl;
		
	    pc->printf("  %s\r\n", topLine.c_str());
		
	
		for (int y = 0; y < min(ylimit, arenaHeight); y++)
		{	
			string thisLine = string((2 * width) + 2, ' ');
			for (int k = 0; k < (2 * width) + 2; k++)
			{
				thisLine[k] = ' ';
			}
	
			  char *p = &thisLine[0];
			  *p = '|';
			  p++;
			  *p = ' ';
	          p++;
	
			  for (int x = 0; x < width; x++)
			  {
			
			    if (x == 58 && y == 34)
			    {
					*p = 'x';
					p++;
					*p = ' ';
					p++;
			    }
			    else
			    {
			
			        int thisIndex = (y * arenaWidth) + x;
			        //Patch *thisPatch = &patches[thisIndex];
			        bool found = false;
			        for (int a = 0; a < agentXYList.size(); a++)
			        {
			          if (agentXYList[a] == thisIndex)
			          {
			            *p = 'o';
			    	    p++;
					    *p = ' ';
					    p++;
					    found = true;
					
					    break;
			          }
		  		}
		
				if (!found)
		    	{
		    	  *p = ' ';
		    	  p++;
		    	  *p = ' ';
		    	  p++;
		        }
			}
		}
		*p = '|';  //thisLine[arenaWidth * 2] = '|';
        p++;
        *p = '|';
        p++;
        
        *p = ' ';
        p++;
        
        *p = ' ';
        p++;
        
        *p = ' ';
        p++;
        
        *p = ' ';
        p++;
        
        *p = ' ';
        p++;
        
        *p = ' ';
        
        pc->printf("%s\r\n", thisLine.c_str());
	  }
	  pc->printf("  %s\r\n", topLine.c_str());
	  
	patch->printDetails(pc);
	
	printAllAgentXYPos(pc);

    }


    void CDM::printAllAgentXYPos(Serial *pc)
    {
		for (int a = 0; a < numAgents; a++)
		{
		  Agent *thisAgent = agents[a];
		  //*pc << timestep << "," << thisAgent->id << "," << thisAgent->xcor << "," << thisAgent->ycor << endl;
		  pc->printf("ID: %d\t x: %f\t y: %f\r\n", thisAgent->id, thisAgent->xcor, thisAgent->ycor);
		}
    }


	void CDM::initializeEnvironment(int numSensors, vector<float> baselineValues)
	{
//		set mu/sigma values for two sensors for now, this will need extending later
		if (numSensors != 2)
		{
//			throw numSensors;
		}
		else
		{
//			setupChemGradient(58, 34, 15);
//			setupChemGradient(58, 110, 15);
			setupChemGradient(30, 15, 7);
			setupChemGradient(30, 45, 7);
			setupChemGradient(30, 30, 15);
			calibrateSensorValues(baselineValues);
			updateEnvironment(baselineValues);
		}
	}
	

	void CDM::updateEnvironment(vector<float> sensorValues)
	{
		// {temperature, charge}
//		sensorValues[0] = max((sensorValues[0] / calibrationValues[0]) - 1.0f, 0.0f);
		sensorValues[0] = max((calibrationValues[0] / (2 * sensorValues[0])) - 1.0f, 0.0f); // possibility for div/0 error here
		sensorValues[1] = max((calibrationValues[1] / (2 * sensorValues[1])) - 1.0f, 0.0f); // possibility for div/0 error here
		sensorValues.push_back(0.5f);
//		for (int i = 0; i < sensorValues.size(); i++)
//		{
//			sensorValues[i] = sensorValues[i] / calibrationValues[i];
//		}
		patch->updateMultipliers(sensorValues);
		
	}
		
	void CDM::calibrateSensorValues(vector<float> baselineValues)
	{
		calibrationValues.clear();
		for (int i = 0; i < baselineValues.size(); i++)
		{
			calibrationValues.push_back(baselineValues[i]);
		}
	}




