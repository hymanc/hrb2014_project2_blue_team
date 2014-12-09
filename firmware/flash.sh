#!/bin/bash
avrdude -P usb -c avrispmkii -p m128 -U ffeedback.hex
