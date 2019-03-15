#include "export.h"

int writeToFile(char* buffer) {
  time_t rawtime;
  struct tm *info;
  char buff[80];
  time( &rawtime );
  info = localtime( &rawtime );
  strftime(buff,80,"data/%Y%m%d%H%M%S.dat", info);

  FILE *file = fopen(buff, "w");

  int results = fputs(buffer, file);
  if (results == EOF) {
    return results;
  }
  fclose(file);
  return 0;
}
