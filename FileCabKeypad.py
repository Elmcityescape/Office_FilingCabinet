import RPi.GPIO as GPIO
from time import sleep
# 1. Attach matrix 7-pin interface to 7 GPIO pins
# 2. Setup column pins as outputs and set high
# 3. Setup row pins as inputs with pull-up resistors (inputs are set high)
# 4. Set outputs low, one at a time.
# 5. When a button is pressed, input becomes low, indicating which button has been pressed

# things to add: 1. use 1s delay to take in input; 2. display numbers on a small LCD screen; 3. use dual coloed LEDs to show right/wrong.
###########   SET-UP  ##########

#debug!
print("Initialize")



GPIO.setmode(GPIO.BCM)

# Define Keypad matrix

MATRIX = [ [1, 2, 3],
           [4, 5, 6],
           [7, 8, 9],
           ['*',0,'#'] ]

# Define Keypad GPIO pins

ROW = [21, 20, 16, 12]
COL = [26, 19, 13]

# Define Maglock GPIO pins

RD=17
ACCT=18
HR=27

# Set up outputs, establish as off

for j in range(3):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 0)

# Set up inputs as pull up and establish event triggers

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    #Add event for detecting input
    GPIO.add_event_detect(ROW[i],GPIO.RISING)
    

GPIO.setup(RD, GPIO.OUT) # r&d output
GPIO.setup(ACCT, GPIO.OUT) # accounting output
GPIO.setup(HR, GPIO.OUT) # Human Resources output
GPIO.output(RD, 0)
GPIO.output(ACCT, 0)
GPIO.output(HR, 0)


# function takes two inputs: 1. a string representing the button that has been pressed; 2. answer string
# fuction appends input to the answer string, and returns the newly updated answer string.
def appendAnswer(input, answer):
    inputStr = str(input)
    answer += inputStr
    return answer


# function takes two inputs: 1. user input; 2. correct answer;
# function returns a string: if correct answer, return "correct"; if wrong answer, return "wrong".
def checkAnswer(answer, key):
    if answer == key:
        result = "correct"
    else:
        result = "wrong"
    return result


###########   MAIN  ##########
answer = ""
rdKey = "0509"
accntKey = "1234"
hrKey = "9999"

print("GO")

try:
    while(True):

        # Incriment outputs
        
        for j in range(3):

            # Turn on column power
            GPIO.output(COL[j],1)
            sleep(0.001)

            # Poll for inputs
            
            for i in range(4):
                if GPIO.event_detected(ROW[i]) and GPIO.input(ROW[i]) == 1:


                    
                    pressed = str(MATRIX[i][j])
                    
                    # when a button is pressed, print the button number.
                    # print(pressed)
                    
                    # when a button is pressed, add it to the answer string by calling a function.

                    #Old code block for # to answer
#                    if pressed != "#":
#                        answer = appendAnswer(pressed, answer)
#                        print(answer)
#                        sleep(0.1)
#                    else:
#                        rdJudge = checkAnswer(answer, rdKey)
#                        accntJudge = checkAnswer(answer, accntKey)
#                        hrJudge = checkAnswer(answer, hrKey)
#                        if rdJudge == "correct":
#                            print("rd password is correct")
#                            GPIO.output(RD, 1)
#                        elif accntJudge == "correct":
#                            print("accounting password is correct")
#                            GPIO.output(ACCT, 1)
#                        elif hrJudge == "correct":
#                            print("hr password is correct")
#                            GPIO.output(HR, 1)
#                        else:
#                            print(answer + "is wrong! The correct rd answer is: "+ rdKey+ " The correct accnt answer is: "+ accntKey+ " TRY AGAIN!")
#                        answer = ""

                    #New code block, 4 numbers
                    answer = appendAnswer(pressed, answer)
                    print(answer)
                    if len(answer)==4:
                        rdJudge = checkAnswer(answer, rdKey)
                        accntJudge = checkAnswer(answer, accntKey)
                        hrJudge = checkAnswer(answer, hrKey)
                        if rdJudge == "correct":
                            print("rd password is correct")
                            GPIO.output(RD, 1)
                        elif accntJudge == "correct":
                            print("accounting password is correct")
                            GPIO.output(ACCT, 1)
                        elif hrJudge == "correct":
                            print("hr password is correct")
                            GPIO.output(HR, 1)
                        else:
                            print(answer + "is wrong! The correct rd answer is: "+ rdKey+ " The correct accnt answer is: "+ accntKey+ " TRY AGAIN!")
                        answer = ""
                    
                    
                    sleep(0.2)
                    #1/5 second pause to avoid double click
            
            GPIO.output(COL[j],0)
            sleep(0.001)
except KeyboardInterrupt:
    print("quitting")
    GPIO.cleanup()
