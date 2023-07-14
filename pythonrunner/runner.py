#THIS FILE IS TO RUN TM_DRIVER CPP COMMANDS - Isaac Merwin June 2023
import subprocess
import time
import argparse
import random as rd
import magnetControl as mC
#import robonet



#Position Data
zeroArray = [0,0,0,0,0,0] #sets to what ill call the zero point
gondolaArray = [0,-0.610865,-0.610865,1.13446,-1.58,0] #TODO fix this, this is the stopping gondola point
homeArray = [1,1.5,1.5,1.5,0,0] #TODO fix this, away position so users can see the screen
wavePos1 = [1.58,-1.58,1.58,1.58,0,1.58]
wavePos2 = [1.58,1.58,-1.58,-1.58,0,-1.58]
blackMarker = [] #TODO
greenMarker = [] #TODO
redMarker = [] #TODO 
blueMarker = [] #TODO
roboVelocity = 1.0
roboAccelTime = 0.4

#Parse args
parser = argparse.ArgumentParser()
parser.add_argument('-r','--random',action='store_true',default=False)
parser.add_argument('-hp','--home',action='store_true',default=False)
parser.add_argument('-gp','--gondola',action='store_true',default=False)
parser.add_argument('-wave','--wave',action='store_true',default=False)
parser.add_argument('-sp','--setpos', type=float, nargs=6, default=zeroArray)
args = parser.parse_args()
j1 = str(args.setpos[0])
j2 = str(args.setpos[1])
j3 = str(args.setpos[2])
j4 = str(args.setpos[3])
j5 = str(args.setpos[4])
j6 = str(args.setpos[5])
#start rand gen
rd.seed(a=None, version=2)

def setArray(a1,a2,a3,a4,a5,a6):
    temp_array = [a1,a2,a3,a4,a5,a6]
    if(len(temp_array)<6):
        raise Exception("set Array did not get enough data to set array breaking - setArray in runner.py")
    return(temp_array)

def robo_sp(positionsArray):
    if(len(positionsArray) == 6):
        pA = positionsArray
    else:
        print("To little points given to robo_sp in runner.py")
        print("going home")
        pA = zeroArray
    j1 = pA[0]
    j2 = pA[1]
    j3 = pA[2]
    j4 = pA[3]
    j5 = pA[4]
    j6 = pA[5]
    j1 = str(j1)
    j2 = str(j2)
    j3 = str(j3)
    j4 = str(j4)
    j5 = str(j5)
    j6 = str(j6)
    rVelocity = str(roboVelocity)
    rAccelTime = str(roboAccelTime)
    print("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+j4+" "+j5+" "+j6+" "+rVelocity+" "+rAccelTime)
    output = subprocess.getoutput("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+j4+" "+j5+" "+j6+" "+rVelocity+" "+rAccelTime)
    print(output)
    #roboVelocity = 0.4
    #roboAccelTime = 0.2

def robo_random():
    robo_sp(setArray(j1,j2,j3,j4,j5,j6))
    time.sleep(6)
    #j1 = rd.choice([1])*rd.random()
    #j2 = rd.choice([1])*rd.random()
    #j3 = rd.choice([-1,1])*rd.random()
    #j4 = rd.choice([-1,1])*rd.random()
    #j5 = rd.choice([-1,1])*rd.random()
    #j6 = rd.choice([-1,1])*rd.random()
    
    
def robo_wave():
    robo_sp(wavePos1)
    time.sleep(18)
    robo_sp(wavePos2)
    time.sleep(18)


def robo_magnet(magIsOn):
    if(magIsOn):
        mC.set_high()
    else:
        mC.set_low()
#TODO NOT TRUE

def moveMarker(toOrFrom,positionsArray):
    #toOrFrom = True: going to gondola, False: coming from gondola
    #positionsArray: Array of joint positions of the marker in question
    #TODO FIX TIMINGS
    pA = positionsArray
    if(toOrFrom):
        robo_sp(zeroArray)
        robo_sp(pA)
        time.sleep(15)
        robo_magnet(True) #Turn magnet on
        print("Magnet On")
        time.sleep(0.3)
        robo_sp(zeroArray)
        robo_sp(gondolaArray)
        time.sleep(15)
        robo_magnet(False) #Turn magnet off
        print("Magnet Off")
        time.sleep(0.3)
        robo_sp(zeroArray)
        robo_sp(homeArray)
        time.sleep(15)
    else:
        robo_sp(zeroArray)
        robo_sp(gondolaArray)
        time.sleep(15)
        robo_magnet(True) #Turn magnet on
        print("Magnet On")
        time.sleep(0.3)
        robo_sp(zeroArray)
        robo_sp(pA)
        time.sleep(15)
        robo_magnet(False) #Turn magnet off
        print("Magnet Off")
        time.sleep(0.3)
        robo_sp(zeroArray)
        robo_sp(homeArray)
        time.sleep(15)
        
        


test_bool = True

#Make this some kind of listener 

while(test_bool):
    robo_magnet(False)
    if(args.home):
        robo_sp(homeArray)
    if(args.gondola):
        robo_sp(gondolaArray)
    if(not args.gondola and not args.home and not args.random and not args.wave):
        robo_sp(setArray(j1,j2,j3,j4,j5,j6))
    if(args.random):
        robo_random()
    time.sleep(2)

