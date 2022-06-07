#include "Serial.h"


std::string Serial::getTime() {
  std::time_t result = std::time(nullptr);
  std::string strResult = std::to_string(result);
  return strResult;
}

Serial::Serial() {
  _logFilePath 		= "outputlog.log" + getTime();
  _logFile 		= std::fopen(_logFilePath.c_str(), "w+");
}

Serial::Serial(std::string logFilePath) {
  _logFilePath 		= logFilePath + getTime();
  _logFile 		= std::fopen(_logFilePath.c_str(), "w+");
  
}

Serial::~Serial() {
  std::fflush(_logFile);
  std::fclose(_logFile);
}


int Serial::printf(const char* format, ...) {
  // catch printf commands and direct output to log file
  va_list args;
  va_start(args, format);
  int a = std::vfprintf(_logFile, format, args);
  va_end(args);
  std::fflush(_logFile);
  return(a);
//  return(0);
}


