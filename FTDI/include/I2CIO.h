#pragma once

/* C */
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <string.h>
#include <math.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

/* mpasse */
#include <mpsse.h>

#include "consts.h"


int I2Cwrite( struct mpsse_context *i2c, uint32_t addr, uint32_t data);
int I2Cread( struct mpsse_context *i2c, uint32_t addr, uint32_t *data, uint32_t ndata );
