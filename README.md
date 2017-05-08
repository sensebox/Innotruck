# senseBox dashboard for Innotruck project

The sensor station is a modified version of the [senseBox:home](http://www.watterott.com/de/senseBox-Home-LAN) with an additional SDS011 sensor. It sends measurement data over a serial connection to the RPi where it is displayed on a compatible 7" screen. 

Here is a prewiev of the [pyqtgraph](http://www.pyqtgraph.org/) based dashboard for visualizing the sensor data:

![senseBox dashboard](https://pbs.twimg.com/media/C_IWTncXYAAbeZx.jpg)

## Hardware components
* [senseBox:home sensor station](http://www.watterott.com/de/senseBox-Home-LAN)
* [SDS011 PM sensor](http://aqicn.org/sensor/sds011/)
* [RPi3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
* [RPi 7" Display](https://www.element14.com/community/docs/DOC-78156/l/raspberry-pi-7-touchscreen-display)


## Installation instructions


### Prepare RPi
Download and install an OS for the RPi and install it (we use [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) in this example). After that follow the intallation instructions on the [pyqtgraph homepage](http://www.pyqtgraph.org/).

#### Python script
Copy the python script in this directory to the pi home folder and make it executable:
```
sudo chmod -x senseBox-dashboard.py
```
To enable autostart of the script edit `~/.config/lxsession/LXDE-pi/autostart` and add the following line to the end of the file:
```
@sudo /usr/bin/python /home/pi/senseBox-dashboard.py
```

#### Disable screen saver
update the `/etc/lightdm/lightdm.conf` file and add the follwing command on top of the `[SeatDefaults]` section:
``` 	
[SeatDefaults]
xserver-command=X -s 0 -dpms
``` 
#### Adjust brightness of screen
``` 
sudo sh -c "echo n > /sys/class/backlight/rpi_backlight/brightness"
```
where n ∈ [0,...,255]. *Do not set to n < 100!*

#### Flip screen
If you want to change orientation of the display edit `/boot/config.txt` and add this command to the beginning of the file:
```
lcd_rotate=2
```

### Prepare the senseBox 
Connect the SDS011 dust particle sensor to the senseBox:home and use the [Arduino IDE](https://www.arduino.cc/en/Main/Software) with [some additional libraries](resources/libraries/senseBox_Libraries.zip) to upload the Arduino sketch from this repository to the sensor station. Then connect it to the RPi via USB cable.
