import subprocess
import time
import os

def randomize_traffic():
    os.chdir(r"D:\My study\5th year\Graduation Project\traffic-optimization\test_environments\single_intersection_no_traffic\newnet.sumocfg")
    p = subprocess.Popen(["python", r'C:\Program Files (x86)\DLR\Sumo\tools\randomTrips.py', '-n', 'newnet.net.xml',
                          '-e', '800', '-p', '1.2', '-r', 'newnet.rou.xml'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    time.sleep(.1)
