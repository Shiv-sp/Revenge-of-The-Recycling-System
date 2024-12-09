def imports (): 
    import time 

def sleep (seconds): 
    time.sleep (seconds)


def botTime (): 
    time.time ()

def userInput ():
    userContainer = int(input("Please enter a container ID that you would like to dispose of (In the form of 0#, where # is the specific ID): "))
    return userContainer 

def bot_dispense_container (containerID): 
    # Activating sensor
    bot.activate_line_following_sensor() #Line sensor
    bot.activate_color_sensor() #Colour sensor 

    '''Time stuff'''
    while True: 
        try:
            '''time_difference= program_running_time - initial_time
            if time_difference >= time_taken:'''

            '''Bot movement'''
            colour_readings = bot.read_color_sensor()
            rgbValues = colour_readings[1]

            if rgbValues[0] > 140 and containerID == 2 or rgbValues[0] > 140 and containerID == 5:
                #Red colour
                bot.stop()
                sleep (4)
                bot_unload_container()
                break

            elif rgbValues[1] > 140 and container == 3:
                #Green colour
                bot.stop()
                sleep (4)
                bot_unload_container()
                break

            elif rgbValues[2] > 140 and container == 1:
                #Blue colour
                bot.stop()
                sleep (4)
                bot_unload_container()
                break
            elif rgbValues[0] == 0 and rgbValues[1] == 0 and rgbValues[2] == 0 and container == 4 or rgbValues[0] == 0 and rgbValues[1] == 0 and rgbValues[2] == 0 and container == 6:
                #Black colour
                bot.stop()
                sleep (4)
                bot_unload_container()
                break

        

        except: 
            sleep(10)
            bot.stop()

        lineFollowValues = bot.line_following_sensors()
                
        lineFollowLeft = lineFollowValues[0]
        lineFollowRight = lineFollowValues[1]

        if lineFollowLeft == 1 and lineFollowRight == 1:
            bot.set_wheel_speed([0.1,0.1])

        elif lineFollowLeft == 1 and lineFollowRight == 0:
            bot.set_wheel_speed([0,0.03])

        elif lineFollowLeft == 0 and lineFollowRight == 1:
            bot.set_wheel_speed([0.03,0])
        else:
            bot.set_wheel_speed([0.5,0.2])
    

def bot_unload_container (): 
    bot.stop()

    bot.activate_linear_actuator()
    bot.linear_actuator_out(3)

    sleep(6)

    bot.linear_actuator_in(3)
    
    sleep(3)

    return None


def main (): 
    imports ()
    userContainer = userInput ()
    bot_dispense_container (userContainer)

