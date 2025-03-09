#!/bin/bash
echo Setting up Temperature Sensor
sudo modprobe w1-gpio
sudo modprobe w1-therm
echo Output Showcasing device 
cd /sys/bus/w1/devices/
ls

echo Setup Complete

