#!/bin/bash
cd /home/pi/LED-Display
echo "===== starting =====" >> log.txt
sudo python main.py -c 4 --led-no-hardware-pulse hej >> log.txt 2>&1 &
cd -
