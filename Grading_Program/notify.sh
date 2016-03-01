#!/bin/bash

case $2 in
  -1)
    DISPLAY=:0 zenity  --info  --text "$1" --title="System wide message" --timeout=0 --width=350 --height=100
    exit 0
    ;;
  0)
    message="you should not see this, tell the people patrolling that you got a \"status 0\""
    ;;
  1)
    message="Good Job, it works!"
    ;;
  2)
    message="formatting error"
    ;;
  3)
    message="compile error"
    ;;
  4)
    message="no main class found"
    ;;
  5)
    message="run time error"
    ;;
  6)
    message="ran for too long > 1min"
    ;;
  7)
    message="outputs do not match"
    ;;
  *)
    message="Something happend with your submission, we are tring to fix it"
    ;;
esac
DISPLAY=:0 zenity  --info  --text "$message" --title="Problem $1" --timeout=0 --width=350 --height=100