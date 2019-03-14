#include "export.h"

int writeToFile(char* buffer, char* filename) {
  FILE *file = fopen(filename, "w");

  int results = fputs(buffer, file);
  if (results == EOF) {
    return results;
  }
  fclose(file);
  return 0;
}
