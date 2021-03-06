#!/bin/bash
#run with "source schedule_maintenance.sh [arg1] [arg2] [arg3]"
#pass dates as "m/d/y@hour:min"
if (( $# > 0 ))
then
  if [ $1 == "true" ]; then
    export IS_MAINTENANCE_SCHEDULED=$1
    echo "Schedule Maintenance Message has been enabled."
  elif [ $1 == "false" ]; then
    export IS_MAINTENANCE_SCHEDULED=$1
    echo "Schedule Maintenance Message has been disabled."
  else
    printf "The value of arg1:IS_MAINTENANCE_SCHEDULED must be a boolean.\n"
  fi
else
  printf "Not enough arguements. Please enter arguements [IS_MAINTENANCE_SCHEDULED] [MAINTENANCE_START_DATETIME] [MAINTENANCE_END_DATETIME]\n"
fi

if (( $# > 1)); then
  export MAINTENANCE_START_DATETIME=$2
  echo "Scheduled Maintenance starts at " $MAINTENANCE_START_DATETIME
fi

if (( $# > 2)); then
  export MAINTENANCE_END_DATETIME=$3
  echo "Schedule Maintenance ends at " $MAINTENANCE_END_DATETIME
fi
