#!/bin/bash
date >> /tmp/autostart_time.log
echo "Whoami: $(whoami)" >> /tmp/autostart_time.log
echo "Path: $PATH" >> /tmp/autostart_time.log
which python3 >> /tmp/autostart_time.log