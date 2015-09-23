#!/bin/bash

(
   flock -x -w 10 200
   fswebcam $@
) 200>/var/lock/.fswebcam.exclusivelock
