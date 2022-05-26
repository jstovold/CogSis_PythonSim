// replacement for actual mbed header to include my fake headers in place.

// identical to actual mbed.h header define, which prevents both being loaded:
#ifndef MBED_H
#define MBED_H

#include "../Serial.h"

// from light_seeker.h:
#define NONE    0
#define RED     1
#define GREEN   2
#define BLUE    3




#endif
