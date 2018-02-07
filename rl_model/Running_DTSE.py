
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import traci
import numpy as np
import DTSE as dtse
#importing python modules from the $SUMO_HOME/tools directory

try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools")) 
    from sumolib import checkBinary 
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")



#///////////////////////////////////////////////////////////////////////////////////////////////////////////
def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options
#////////////////////////////////////////////////////////////////////////////////////////////////////////////
## generating the DTSE 

def get_data ():
	
	x ,y =  dtse.DTSE_Generator.get_traffic_state("-road4_0","out",15,5)
	print(x)
	print(y)

	s,p = dtse.DTSE_Generator.get_traffic_lights_state("node1")
	print(s)
	print(p)

#////////////////////////////////////////////////////////////////////////////////////////////////////////////
def run():
    step =0
    while (step != 10000):
        traci.simulationStep()
        step += 1
        get_data()
    traci.close()
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "newnet.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"],)
    
    run()

