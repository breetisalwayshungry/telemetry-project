#!/bin/bash

# Handle Ctrl + C
trap 'cleanup' SIGINT

cleanup() {
	echo "Stopping all processes..."
	kill $(jobs -p) &>/dev/null
	exit 0
}

echo "Activating virtual environment..."
cd /home/pi/projects
source env_projects/bin/activate

echo "Starting telemetry system..."
echo "10 seconds..."
sleep 5 # gives me 10 seconds to switch systems
echo "5 seconds..."
sleep 5

echo "Starting camera..."
[ -p /tmp/camera_pipe ] || mkfifo /tmp/camera_pipe # creates named pipe
ffmpeg -i /tmp/camera_pipe -c:v copy -movflags +frag_keyframe+empty_moov ~/Videos/video_$(date +"%Y%m%d_%H%M%S").mp4 &
sleep 2
libcamera-vid -t 30000 --output /tmp/camera_pipe & # time to record. this dev version is for 30 seconds. Prior to flight, this will be changed to 600000 (10 min)

sleep 10

echo "Running sensors.py"
python3 /home/pi/projects/flightpi/sensors.py &

wait
