# -*- coding: utf-8 -*-

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.syncLogger import SyncLogger
import math
import time
import pandas as pd


uri = "radio://0/23/2M"   
dt=[]
size = 5
trackingV =0.5
def pos_data(timestamp, data, logconf):
    position = [
        data['peerdist.distance2peer20'], 
    ]
    print( position )
    dt.append((position[0],time.time()))

def distance_measurement():
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        lpos = LogConfig(name='distance', period_in_ms=100)    
        lpos.add_variable('peerdist.distance2peer20')
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(pos_data)
        lpos.start()
        time.sleep(40+2)    #siample time
    df = pd.DataFrame(dt,columns=['distance','time'])
    df.to_csv('./distForEstVeloBy100ms.csv',index=False)
    print("done")
    return

if __name__ == '__main__':
    # init drivers mandatory
    cflib.crtp.init_drivers(enable_debug_driver=False)
    distance_measurement()