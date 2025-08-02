#!/bin/bash

python -m lerobot.teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=my_awesome_follower_arm \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=my_awesome_leader_arm \
    --display_data=true

python -m lerobot.teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=my_awesome_follower_arm \
    --teleop.type=gamepad \
    --display_data=true

python -m lerobot.teleoperate \
  --robot.type=so100_follower_end_effector \
  --robot.port=/dev/ttyACM0 \
  --robot.id=my_awesome_follower_arm \
  --robot.urdf_path="/mnt/d/repos/lerobot/so101_new_calib.urdf" \
  --teleop.type=gamepad \
  --display_data=true
