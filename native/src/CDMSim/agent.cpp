#include "agent.h"
//#include <iomanip>

    Agent::Agent(int ID, CDM *env, float vision_in)
    {
		environment      = env;
		id               = ID;
		xcor             = 0;
		ycor             = 0;
		heading          = 0;	 // in radians..?
		magnitude        = 0;
		direction        = 0;
		nearestNeighbour = NULL;
		
		fg[0] 		 	 = 0;
		fg[1] 		 	 = 0;
	
		fgamma[0]        = 0;
		fgamma[1]        = 0;
		fchem[0]         = 0;
		fchem[1]         = 0;
	
		maxSpeed         = 3.0f;
		virtualGoal[0]   = 0;
		virtualGoal[1]   = 0;
	
		prevAveHeading   = 0.0f;
		attrDivisor      = 0;
		
    }


    void Agent::placeAgent(float x, float y, float h)
    {
		heading 	= h;
		xcor 		= x;
		ycor 		= y;
		direction 	= h;
		prevAveHeading 	= h;
    }

    void Agent::updateNeighbourhood()
    {
		// need to clear neighbours out appropriately
		neighbours.clear();
		neighbours = environment->getOtherAgentsInRadius(agentVision, id);
		if (neighbours.size() > 0)
		{
		  nearestNeighbour = environment->getClosestAgentInRadius(agentVision, id);
		}
    }


    void Agent::flock()
    {
		calcFchem();
	
		float Ui[2] = {0,0};
		
		if (neighbours.size() > 0)
		{
		  calcLattice();
		  utils::vectorAdd(fg, fgamma, Ui);
		  utils::vectorAdd(Ui, fchem, Ui);
		}
		else
		{
		  Ui[0] = fchem[0];
		  Ui[1] = fchem[1];
		}
	
		if (id == 1)
		{
		  //cout << setprecision(5) << fchem[0] << "," << fchem[1] << "," << fg[0] << "," << fg[1] << "," << fgamma[0] << "," << fgamma[1] << "," << neighbours.size() << endl;
		}
		float dX = Ui[0];
		float dY = Ui[1];
	
		float Td = 0.005;
		float dir = 0;
		if (dX == 0 && dY == 0)
		{
		  dir = heading;
		}
		else
		{
		  dir = utils::myAtan(dX, dY);
		  dir = fmodf(dir, 2 * PI); //360);
		}
	
		float mag 	= utils::round3(Td * sqrt(pow(dX, 2) + pow(dY, 2)));
		direction	= utils::round3(dir);
	
		if (neighbours.size() > 0)
		{
		  magnitude	= max(mag, 0.05f);
		}
		else
		{
		  magnitude	= max(mag, 0.1f);
		}
    }

    void Agent::calcLattice()
    {
		calcFg();
		calcFgamma(calcAveHeading());
    }

    void Agent::calcFg()
    {
	float cumulativeSum[] = {0, 0};
	int neighbourSize = neighbours.size();
	
	for (int n = 0; n < neighbourSize; n++)
	{
	  Agent *thisNeighbour 		= neighbours[n]; 
	  float diffDistance 		= - distanceToAgent(thisNeighbour);
	  float diffDirection 		= directionToAgent(thisNeighbour);
	  float diffPose[]	 	= {diffDistance * cos(diffDirection), diffDistance * sin(diffDirection)}; // radians // -sin...
	  float auxVecDivide		= 1 / sqrt(1 + eps * diffDistance * diffDistance);
	  float vecNij[]		= {0,0};
	  utils::vectorMult(diffPose, auxVecDivide, vecNij);
	  float sigmaNorm		= utils::calcSigmaNorm(diffPose);
	  float phiAlpha		= utils::calcPhiAlpha(sigmaNorm);
	  if (id == 1)
	  {
	    //cout << setprecision(5) << thisNeighbour->id << "," << environment->timestep << "," << diffPose[0] << "," << diffPose[1] << "," << phiAlpha << "," << sigmaNorm << "," << diffDirection << "," << diffDistance << endl; //<< diffPose[0] << "," << diffPose[1] << endl;
	  }
	  float result[]		= {0,0};
	  utils::vectorMult(vecNij, phiAlpha, result);
	  utils::vectorRound3(result);
	  utils::vectorAdd(cumulativeSum, result, cumulativeSum);
	}
	
	fg[0] = cumulativeSum[0];
	fg[1] = cumulativeSum[1];
    }

    void Agent::calcFgamma(float aveHeading)
    {
	long ticks = environment->timestep;
	if (ticks == 1 || (ticks % virtualGoalUpdateRate) == 0 || (virtualGoal[0] == 0 && virtualGoal[1] == 0))
	{
	  calcVirtualGoalPos(aveHeading, virtualGoal);
	}

	float diffDistance	= distanceToGoal();

	float diffDirection 	= directionToGoal();
	float diffPose[]	= {diffDistance * cos(diffDirection), diffDistance * sin(diffDirection)}; // -sin ..
	float qDiff[]		= {0,0};
	utils::vectorMult(diffPose, c1, qDiff);

	fgamma[0] = qDiff[0];
	fgamma[1] = qDiff[1];
    }

    void Agent::calcFchem()
    {
	float chemS = attractionAt(0,1);
	float chemE = attractionAt(1,0);
	float chemN = attractionAt(0,-1);
	float chemW = attractionAt(-1,0);
	
    if (id == 1)
    {
	//cout << setprecision(5) << environment->timestep << "," << chemN << "," << chemE << "," << chemS << "," << chemW << endl;
    }
	float chemX = chemE - chemW;
	float chemY = chemN - chemS;
	float myChemMult = calcChemMultiplier();
	chemX *= myChemMult;
	chemY *= myChemMult;
	fchem[0] = chemX;
	fchem[1] = chemY;
    } 
   
    void Agent::calcVirtualGoalPos(float aveHeading, float returnVal[])
    {
	float virtXcor 		= (xcor + (distanceToVirtualGoal * cos(aveHeading)));
	float virtYcor 		= (ycor + (distanceToVirtualGoal * sin(aveHeading))); // -sin..
	returnVal[0]		= virtXcor;
	returnVal[1]		= virtYcor;
    }
    
    float Agent::calcAveHeading()
    {
	if (neighbours.size() > 0) 
	{
	  float x = 0.0f;//cos(heading);
	  float y = 0.0f;//sin(heading);
	  int neighbourSize = neighbours.size();

	  for (int n = 0; n < neighbourSize; n++)
	  {
	    x += cos(neighbours[n]->heading);
	    y += sin(neighbours[n]->heading);
	    x += cos(neighbours[n]->prevAveHeading);
	    y += sin(neighbours[n]->prevAveHeading);
	  }
	  prevAveHeading = fmodf(utils::myAtan(x,y), 2 * PI);	
	  return prevAveHeading; //utils::myAtan(x,y); //, 2 * PI); //360);
	}
	else
	{
	  prevAveHeading = heading;
	  return heading;
	}
    }

    float Agent::calcChemMultiplier()
    {
		if (useRefractoryPeriod)
		{
		  if (attractionHere() >= highAttractThreshold)
		  {
		    attrDivisor = min(attrDivisor + 0.0025, 5.0);
		  }
		  else
		  {
		    attrDivisor = max(attrDivisor - 0.05, 0.0);
		  }
	
		  if (attrDivisor >= 1)
		  {
		    return chemMult / attrDivisor;
		  }
		  else
		  {
		    return chemMult;
		  }
		}
		else
		{
		  return chemMult;
		}

    }


    // helper functions:
    float Agent::distanceToXY(float x, float y)
    {
		float diffX = xcor - x;
		float diffY = ycor - y;

		if (diffX > (arenaWidth - diffX) )
		{
			diffX = arenaWidth - diffX;		// shorter distance to wrap around
		}
		
		if (diffY > (arenaHeight - diffY) )
		{
			diffY = arenaHeight - diffY;	// shorter distance to wrap around
		}
		return sqrt(pow(diffX, 2) + pow(diffY, 2));
    }

    float Agent::distanceToAgent(Agent *a)
    {
    	return distanceToXY(a->xcor, a->ycor);
//		float diffX = xcor - a->xcor;
//		float diffY = ycor - a->ycor;
//		return sqrt(pow(diffX, 2) + pow(diffY, 2));
    }

    float Agent::directionToAgent(Agent *a)
    {
		float diffX = xcor - a->xcor;
		float diffY = ycor - a->ycor;
		if (diffX > (arenaWidth - diffX) )
		{
			diffX = arenaWidth - diffX;		// shorter distance to wrap around
		}
		
		if (diffY > (arenaHeight - diffY) )
		{
			diffY = arenaHeight - diffY;	// shorter distance to wrap around
		}
		return utils::myAtan(diffX, diffY);
    }
 

    float Agent::attractionHere()
    {
		return attractionAt(0,0);
    }


	float Agent::attractionAt(float dX, float dY)
	{
		int patchX = fmod(round(xcor + dX), arenaWidth);
//		patchX %= arenaWidth;
		int patchY = fmod(round(ycor - dY), arenaHeight);
//		patchY %= arenaHeight;
		return environment->patch->calcAttraction(patchX, patchY);
	}
//
//    Patch* Agent::patchAt(float dX, float dY)
//    {
//		int patchX = round(xcor + dX);
//		int patchY = round(ycor - dY);
//		return environment->patchAtXY(patchX, patchY);
//    }
	

    float Agent::distanceToGoal()
    {
		float virtX = virtualGoal[0];
		float virtY = virtualGoal[1];
		float diffX = xcor - virtX;
		float diffY = ycor - virtY;
		
		if (diffX > (arenaWidth - diffX) )
		{
			diffX = arenaWidth - diffX;		// shorter distance to wrap around
		}
		
		if (diffY > (arenaHeight - diffY) )
		{
			diffY = arenaHeight - diffY;	// shorter distance to wrap around
		}
	
		return sqrt(pow(diffX, 2) + pow(diffY, 2));
    }

    float Agent::directionToGoal()
    {
		float virtX = virtualGoal[0];
		float virtY = virtualGoal[1];
		float diffX = xcor - virtX;
		float diffY = ycor - virtY;
		if (diffX > (arenaWidth - diffX) )
		{
			diffX = arenaWidth - diffX;		// shorter distance to wrap around
		}
		
		if (diffY > (arenaHeight - diffY) )
		{
			diffY = arenaHeight - diffY;	// shorter distance to wrap around
		}
		return utils::myAtan(diffX, diffY);
    }

   // float Agent::headingToAgent(Agent *a)
//    {
////		float aX = a->xcor;
////		float aY = a->ycor;
////		float diffX = aX - xcor;
////		float diffY = aY - ycor;
////		
////		return utils::myAtan(diffX, diffY);
//    }

    void Agent::turnTowards(float desiredDirection)
    {
		float diff = utils::subtractHeadings(desiredDirection, heading);
		if (diff > maxTurn)
		{
		  diff = maxTurn;
		}
		else if (diff < -maxTurn)
		{
		  diff = -maxTurn;
		}
		heading += diff;
		heading = fmodf(heading, 2 * PI); // 360);
    }

    void Agent::turnAwayFrom(Agent *a)
    {
		float dir 	= directionToAgent(a);
		float diff 	= utils::subtractHeadings(dir, heading);
		if (diff > maxTurn)
		{
		  diff = maxTurn;
		}
		else if (diff < -maxTurn)
		{
		  diff = -maxTurn;
		}
		heading -= diff;
		heading = fmodf(heading, 2 * PI); // 360);
    }



