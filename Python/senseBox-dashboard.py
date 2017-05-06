# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import serial


app = QtGui.QApplication([])
win = QtGui.QMainWindow()
win.showMaximized()
#win.showFullScreen()
win.setWindowTitle('senseBox:home Visualization')
pg.setConfigOptions(antialias=True) # Enable antialiasing for prettier plots

cw = QtGui.QWidget()
win.setCentralWidget(cw)
l = QtGui.QGridLayout()
cw.setLayout(l)
l.setSpacing(0)
l.setMargin(0)

p1 = pg.PlotWidget(name='Plot1')
l.addWidget(p1,0,0)
p2 = pg.PlotWidget(name='Plot2')
l.addWidget(p2,0,1)
p3 = pg.PlotWidget(name='Plot5')
l.addWidget(p3,0,2)
p4 = pg.PlotWidget(name='Plot3')
l.addWidget(p4,1,0)
p5 = pg.PlotWidget(name='Plot4')
l.addWidget(p5,1,1)
p6 = pg.PlotWidget(name='Plot4')
l.addWidget(p6,1,2)

p1.setLabel('left',units='Temperatur in °C')
p1.showAxis('bottom', False)
c1 = p1.plot(pen=(255,50,0))
p2.setLabel('left',units='Rel. Luftfeuchtigkeit in %')
p2.showAxis('bottom', False)
c2 = p2.plot(pen=(50,150,255))
p3.setLabel('left',units='Luftdruck in hPa')
p3.showAxis('bottom', False)
c3 = p3.plot(pen='w')
p4.setLabel('left',units='Beleuchtungsst&auml;rke in lx')
p4.showAxis('bottom', False)
c4 = p4.plot(pen='y')
p5.setLabel('left',units='UV Intensit&auml;t in µW/m²')
p5.showAxis('bottom', False)
c5 = p5.plot(pen=(255,0,255))
p6.setLabel('left',units='Feinstaubkonzentration in µg/m³')
p6.showAxis('bottom', False)
c6 = p6.plot(pen=(255,150,50))
c7 = p6.plot(pen=(150,255,50))

p1.addLegend()
l1 = p1.plotItem.legend
l1.anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,10))
p2.addLegend()
l2 = p2.plotItem.legend
l2.anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,10))
p3.addLegend()
l3 = p3.plotItem.legend
l3.anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,10))
p4.addLegend()
l4 = p4.plotItem.legend
l4.anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,10))
p5.addLegend()
l5 = p5.plotItem.legend
l5.anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,10))
p6.addLegend()
l6 = p6.plotItem.legend
l6.anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,10))

p1.enableAutoRange('x', True)
p2.enableAutoRange('x', True)
p3.enableAutoRange('x', True)
p4.enableAutoRange('x', True)
p5.enableAutoRange('x', True)
p6.enableAutoRange('x', True)

temp = '0' + u"\u2103"
humi = '0' + '%'
pres = '0' + 'hPa'
illu = '0' + 'lx'
uvra = '0' + u"\u00b5" + 'W/m' + u"\u00b2"
pm25 = '0' + u"\u00b5" + 'g/m' + u"\u00b3"
pm10 = '0' + u"\u00b5" + 'g/m' + u"\u00b3"

measurements = range(7) #data from serial port as array
sensors = np.zeros((7,60)) #data to be displayed

def connectSenseBox(baud = 9600):
	global senseBox
	from serial.tools import list_ports
	ports_avaiable = list(list_ports.comports())
	senseBox_port = tuple()
	for port in ports_avaiable:
		if port[1].startswith("Genuino"):
			senseBox_port = '/dev/' + port.name
	if senseBox_port:
		senseBox = serial.Serial(senseBox_port, baud, timeout=1)
		print('Port ' + senseBox.name + ' is now open!')
	else:
		print('No senseBox found!')

def readSenseBox():
	global measurments, senseBox
	if 'senseBox' not in globals():
		connectSenseBox()	
	if senseBox.isOpen():
		serialData = senseBox.readline()
		serialData = serialData.strip().split(',')
		obs = len(serialData)		
		if obs == 7:	
			for i in range(0,7):
				measurements[i] = float(serialData[i])
			print(measurements)	
	return np.array(measurements)
	
def update():
	global sensors,temp,humi,pres,illu,uvra,pm25,pm10

	# remove old values from legend	
	l1.removeItem(temp)
	l2.removeItem(humi)
	l3.removeItem(pres)
	l4.removeItem(illu)
	l5.removeItem(uvra)
	l6.removeItem(pm25)
	l6.removeItem(pm10)

	#senseBox software updates measurements each 2 secs
	data = readSenseBox()	

	# update data to be displayed in graphs
	sensors = np.roll(sensors, -1, axis=1)
	sensors[:, -1:] = np.reshape(data,(7,1))

	p1.setYRange(min(sensors[0,]),max(sensors[0,]) + (max(sensors[0,])-min(sensors[0,]))*20/100)
	p2.setYRange(min(sensors[1,]),max(sensors[1,]) + (max(sensors[1,])-min(sensors[1,]))*20/100)
	p3.setYRange(min(sensors[2,]),max(sensors[2,]) + (max(sensors[2,])-min(sensors[2,]))*20/100)
	p4.setYRange(min(sensors[3,]),max(sensors[3,]) + (max(sensors[3,])-min(sensors[3,]))*20/100)
	p5.setYRange(min(sensors[4,]),max(sensors[4,]) + (max(sensors[4,])-min(sensors[4,]))*20/100)
	p6.setYRange(min(sensors[5,]),max(sensors[6,]) + (max(sensors[6,])-min(sensors[5,]))*25/100)

	c1.setData(sensors[0]) #temperature
	c2.setData(sensors[1]) #humidity
	c3.setData(sensors[2]) #pressure
	c4.setData(sensors[3]) #illuminance
	c5.setData(sensors[4]) #uv radiation
	c6.setData(sensors[5]) #pm2.5
	c7.setData(sensors[6]) #pm10	

	# prepare text for legend entries
	temp = '%0.2f' % (data[0]) + u"\u2103"
	humi = '%0.2f' % (data[1]) + '%'
	pres = '%0.2f' % (data[2]) + 'hPa'
	illu = '%0.1d' % (data[3]) + 'lx'
	uvra = '%0.1d' % (data[4]) + u"\u00b5" + 'W/m' + u"\u00b2"
	pm25 = '%0.1f' % (data[5]) + u"\u00b5" + 'g/m' + u"\u00b3" + ' (PM 2.5)'
	pm10 = '%0.1f' % (data[6]) + u"\u00b5" + 'g/m' + u"\u00b3" + ' (PM 10)'

	# insert new values to legend	
	l1.addItem(c1, temp)
	l2.addItem(c2, humi)
	l3.addItem(c3, pres)
	l4.addItem(c4, illu)
	l5.addItem(c5, uvra)
	l6.addItem(c6, pm25)
	l6.addItem(c7, pm10)
	
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)#update intervall

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

