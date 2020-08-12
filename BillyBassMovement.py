from DFRobot_RaspberryPi_DC_Motor import DFRobot_DC_Motor_IIC as Board
import RPi.GPIO as GPIO
import time

#GPIO setup
AUDIO_CHANNEL = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(AUDIO_CHANNEL, GPIO.IN)

#Motor setup
board = Board(1, 0x10)

def startProgram() :
    #First, setup the board
    setupMotors()

    #Create the GPIO callback for when noise happens
    GPIO.add_event_detect(AUDIO_CHANNEL, GPIO.BOTH, bouncetime=300)
    GPIO.add_event_callback(AUDIO_CHANNEL, audioOccured)

def setupMotors() :
    #Print the list of boards available
    list = board.detecte()
    print("List of available board:")
    print(list)
    
    #Ensure that the board is setup properly.
    while board.begin() != board.STA_OK:
        print("Failed to setup board!")
        time.sleep(2)
    print("Successfully setup the board!")

    #Setup specific board settings
    board.set_encoder_disable(board.ALL)
    board.set_encoder_reduction_ratio(board.ALL, 43)
    board.set_moter_pwm_frequency(1000)

    #for i in range(20) :
    #    moveHead(0.25)
    #    moveTail(0.25)
    #    openMouth(0.5)

    
    #CW Moves Body
    #CCW moved head
    #Motor 2

def moveHead(duration) :
    board.motor_movement([board.M2], board.CW, 95)
    time.sleep(duration)
    board.motor_stop(board.ALL)

def moveTail(duration) :
    board.motor_movement([board.M2], board.CCW, 95)
    time.sleep(duration)
    board.motor_stop(board.ALL)

def openMouth(duration) :
    board.motor_movement([board.M1], board.CW, 95)
    time.sleep(duration)
    board.motor_stop(board.ALL)

def raiseHead() :
    board.motor_movement([board.M2], board.CW, 95)

def lowerHead() :
    board.motor_movement([board.M2], board.CW, 0)

lastAudioEvent = 0
newEvent = True

def audioOccured(channel) :
    global newEvent
    global lastAudioEvent

    if(newEvent) :
        raiseHead()

    board.motor_movement([board.M1], board.CW,95)
    time.sleep(0.2)
    board.motor_movement([board.M1], board.CW, 0)

    print ("Audio Occured",channel,GPIO.input(channel),time.time())
    
    lastAudioEvent = time.time()
    newEvent = False

if __name__ == "__main__":
    startProgram()

    #Loop infinitely, the next event will be the callback.
    while True:
        ctime = time.time()

        if(ctime - lastAudioEvent > 0.4) :
            print("New Event")
            newEvent = True

            #Move the body back to its normal position
            board.motor_stop(board.ALL)
        
        #Sleep for half a second to save resoruces.
        time.sleep(0.5)
