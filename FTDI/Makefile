# CC := gcc
#
# LDFLAGS= -lmpsse -lm
#
# all: i2ctest #spiflash spiflashfast i2ceeprom ds1305 gpio bitbang
#
# spiflash:
# 	$(CC) $(CFLAGS) spiflash.c -o spiflash $(LDFLAGS)
#
# spiflashfast:
# 	$(CC) $(CFLAGS) spiflashfast.c -o spiflashfast $(LDFLAGS)
#
# i2ceeprom:
# 	$(CC) $(CFLAGS) i2ceeprom.c -o i2ceeprom $(LDFLAGS)
#
# ds1305:
# 	$(CC) $(CFLAGS) ds1305.c -o ds1305 $(LDFLAGS)
#
# gpio:
# 	$(CC) $(CFLAGS) gpio.c -o gpio $(LDFLAGS)
#
# bitbang:
# 	$(CC) $(CFLAGS) bitbang.c -o bitbang $(LDFLAGS)
#
# i2ctest: i2ctest.c
# 	$(CC) $(CFLAGS) i2ctest.c -o i2ctest $(LDFLAGS)
#
# clean:
# 	rm -f *.dSYM
# 	rm -f bitbang gpio ds1305 i2ceeprom spiflash spiflashfast
#
# distclean: clean

CC := gcc
SRCDIR := src
BUILDDIR := build
TARGET := bin/main

SRCEXT := c
SOURCES := $(shell find $(SRCDIR) -type f -name *.$(SRCEXT))
OBJECTS := $(patsubst $(SRCDIR)/%,$(BUILDDIR)/%,$(SOURCES:.$(SRCEXT)=.o))
CFLAGS := -g
LIB := -lmpsse -lm
INC := -Iinclude

$(TARGET): $(OBJECTS)
	@echo "Linking..."
	@echo "$(CC) $^ -o $(TARGET) $(LIB)"; $(CC) $^ -o $(TARGET) $(LIB)

$(BUILDDIR)/%.o: $(SRCDIR)/%.$(SRCEXT)
	@mkdir -p $(BUILDDIR)
	@echo "$(CC) $(CFLAGS) $(INC) -c -o $@ $<"; $(CC) $(CFLAGS) $(INC) -c -o $@ $<

clean:
	@echo "Cleaning...";
	@echo "$(RM) -r $(BUILDDIR) $(TARGET)"; $(RM) -r $(BUILDDIR) $(TARGET)
