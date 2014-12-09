#!/bin/bash

avr-gcc -g -Os -mmcu=atmega128 -c force_feedback_avr.c
avr-gcc -g -mmcu=atmega128 -o ffeedback.elf force_feedback_avr.o
avr-objcopy -j .text -j .data -O ihex ffeedback.elf ffeedback.hex
