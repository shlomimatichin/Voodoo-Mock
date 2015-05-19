all: all-targets

ifeq ($(V),1)
  Q =
else
  Q = @
endif

TARGET_mapexample = cpp/MapExample/main.cpp
ifeq ($(OS),Windows_NT)
mapexample_LIBRARIES =
else 
mapexample_LIBRARIES = -lpthread
endif

#SHAREDLIBRARY_example = cpp/Namespace/object1.cpp cpp/Namespace/object2.cpp
#example_LIBRARIES = -ldl -lrt
#Namespace_object1_o_CFLAGS = -fPIC -DPIC
#Namespace_object2_o_CFLAGS = -fPIC -DPIC

CONFIGURATION ?= DEBUG
SHELL := /bin/bash
COMMON_CXXFLAGS = -Ic -Icpp -I/usr/include/python2.7 -std=gnu++0x -Werror -Wall
DEBUG_CXXFLAGS = -ggdb -DDEBUG
RELEASE_CXXFLAGS = -O3
COMMON_CFLAGS = -Ic -Werror -Wall
DEBUG_CFLAGS = $(DEBUG_CXXFLAGS)
RELEASE_CFLAGS = $(RELEASE_CXXFLAGS)
CXXFLAGS = $(COMMON_CXXFLAGS) $($(CONFIGURATION)_CXXFLAGS)
CFLAGS = $(COMMON_CFLAGS) $($(CONFIGURATION)_CFLAGS)

include tools/make/rules.Makefile
