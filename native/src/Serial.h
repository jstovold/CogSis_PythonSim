#ifndef __SERIAL_H
#define __SERIAL_H

#include <stdio.h>
#include <stdarg.h>
#include <ctime>
#include <string>


// this file is written specifically to sit in for the mbed Serial connection (which allows us to direct printf 
// commands through the UART connection back to our computer.

class Serial {
  // yes I know this is C-like, but the robot code relies on a C-like interface to its serial connection, so for 
  // minimal disruption to the code, this is easier.

  std::string 	_logFilePath;
  std::FILE* 	_logFile;
  std::string   getTime();
  public: 
    Serial();
    Serial(std::string logFilePath);
    ~Serial();
    int printf(const char* format, ...);
};


#endif
