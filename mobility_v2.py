py net.plotGraph(max_x=160, max_y=160)
py os.system("python init_flow_add_v2.py")

py net.startMobility(startTime=0)
py net.mobility(sta1, 'start', time=10, position='12.0,48.0,0.0')
py net.mobility(sta1, 'stop', time=50, position='64.0,48.0,0.0')
py net.stopMobility(stopTime=50)
