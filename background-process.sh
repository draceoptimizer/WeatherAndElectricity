#/usr/bin/env bash
#  Input process
GETWEATHER1=0
PROCUTILITY1=0
while getopts wu option
do
case "${option}"
in
w) GETWEATHER1=1;;
u) PROCUTILITY1=1;;
esac
done
GATHERWEATHERSTAT="./gather-weather-stats.out"

if [ ${GETWEATHER1} -eq 1 ]
then
    echo "Starting weather gather in background."
    echo $(date) > ${GATHERWEATHERSTAT}
    nohup ./weather_model_driver.py --gather-weather 2>&1 >> ${GATHERWEATHERSTAT}  &
    echo "Running test in background."
fi
