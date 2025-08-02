#!/bin/bash

python -m lerobot.teleoperate \
    --robot.type=so101_follower \
    --robot.port=COM1 \
    --robot.id=my_awesome_follower_arm \
    --teleop.type=so101_leader \
    --teleop.port=COM2 \
    --teleop.id=my_awesome_leader_arm \
    --display_data=true

python -m lerobot.teleoperate \
    --robot.type=so101_follower \
    --robot.port=COM13 \
    --robot.id=my_awesome_follower_arm \
    --teleop.type=gamepad \
    --display_data=true