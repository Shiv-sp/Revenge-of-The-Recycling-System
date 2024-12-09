ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P3B' # Enter the project identifier i.e. P2A or P2B

# SERVO TABLE CONFIGURATION
short_tower_angle = 315 # enter the value in degrees for the identification tower 
tall_tower_angle = 90 # enter the value in degrees for the classification tower
drop_tube_angle = 180 # enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# BIN CONFIGURATION
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.13 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin1_metallic = False

bin2_offset = 0.13
bin2_color = [0,1,0]
bin2_metallic = False

bin3_offset = 0.13
bin3_color = [0,0,1]
bin3_metallic = False

bin4_offset = 0.13
bin4_color = [5,2,3]
bin4_metallic = False
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
if project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
else:
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color],[bin1_metallic,bin2_metallic, bin3_metallic,bin4_metallic]]
    configuration_information = [table_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bot = qbot(0.1,ip_address,QLabs,project_identifier,hardware)
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
'''
Title: P3: Revenge of Recycling System Simulation Code
Description: Project 3 simulation (Quanser) virtual environment code
Created By: Shiv Patel (pates302), Himesh Mistry (mistrh13)
Course: ENGINEER 1P13
Design Studio Section: T04
Date Created: 28/01/2024
Date Last Modified: 
'''

#Empty list to store container information (Global variable so multiple functions can access it and so its information is always accessible) - Himesh Mistry
container_info_list = []

# Imports all the required libraries - Shiv Patel
def imports (): 
    import time 
    import random 
    import sys

#System exit function, in case user decides to terminate program - Shiv Patel
def systemExit ():
    return sys.exit()

# Sleep function - Shiv Patel
def sleep (seconds): 
    time.sleep (seconds)

# Stores the coordinates of the Q-bot's home position - Shiv Patel
def initialHomePositionBot(): 
    botHomePosition = bot.position ()
    return botHomePosition

# Dispenses a randome container and returns the properties of the container - Shiv Patel
def dispenseContainer(): 
    containerNumber = random.randint (1,6)
    containerInfo = table.dispense_container(containerNumber, True)
    #containerInfo = table.dispense_container(6, True)
    return containerInfo  

# Q-arm will load contianers onto the Q-bot. 'Counter' is a variable that counts the number of containers on the Q-bot - Himesh Mistry
def container_drop_off(counter): 

    # All required coordinates for positions 
    container_location = [0.640, 0.0, 0.230] #Coordinates of the conatiner thats dispensed on the table in a list
    arm_home = [0.012,-0.376,0.621] #Coordinates of the conatiner in home position

    no_container = [0.012, -0.637, 0.531] #Coordinates for arm to place container on bot if no containers are present
    one_container = [0.017, -0.521, 0.498] #Coordinates for arm to place container on bot if one containers are present
    two_container = [0.00, -0.462, 0.478] #Coordinates for arm to place container on bot if two containers are present

    arm.move_arm(container_location [0], container_location [1], container_location [2]) 
    sleep(1)
    arm.control_gripper(45)
    sleep (1.5)
    arm.move_arm(arm_home [0], arm_home [1], arm_home [2])
    sleep (1.5)

    # Need to figure out where to place the container on the Q-bot. Depending on the amount of containers ('counter'), the Q-arm will place the container in a certain position on the Q-bot
    if counter == 0:
        arm.move_arm(no_container [0], no_container [1], no_container [2])
        sleep (1.5)
        arm.control_gripper(-40)
        sleep (1.5)
        arm.rotate_shoulder(-20)
        sleep (1.5)
        arm.home()

    elif counter == 1:
        arm.move_arm(one_container [0], one_container [1], one_container [2])
        sleep (1.5)
        arm.control_gripper(-40)
        sleep (1.5)
        arm.rotate_shoulder(-20)
        sleep (1.5)
        arm.home()

    else:
        arm.move_arm(two_container [0], two_container [1], two_container [2])
        sleep (1.5)
        arm.control_gripper(-40)
        sleep (1.5)
        arm.rotate_shoulder(-20)
        sleep (1.5)
        arm.home()
    
    return False

'''
This function checks to see if more containers can be added on the Q-bot based on the three conditions:
 - if less than 3 containers are on the Q-bot
 - the container on the table will also go to the same bin as the containers on the Q-bot
 - The mass of the containers on the Q-bot and the mass of the new container is less than 90 grams
'''
def loadContainer (cycles): #Himesh Mistry & Shiv Patel
    #Initializing Variables
    totalMass = 0  # The total mass of the containers
    counter = 0   # The number of containers 

    # Mass of the table without any containers
    tableMass = table.load_cell_sensor(0.2)[0]

    #Iterating till three bottles are dropped or conditions are met
    while 3 > counter:

        # This is for the first container. The mass of the table is not zero and no container is on the bot and it isn't the first cycle 
        if cycles != 1 and counter == 0 and tableMass != 0.0:


            # Load the container on the Q-bot and add the mass of the container to the total mass
            container_drop_off(counter)
            totalMass += tableMass

            # Clears all the elements of the list that contains the bin locations of the dispensed container, excpet for the last container and adds the last container to the list
            temporary = container_info_list[-1]
            container_info_list.clear()
            container_info_list.append(temporary)
            counter += 1

            continue

        # If there are no containers, then clear the list
        if counter == 0:
            container_info_list.clear()

        # Dispsenses container, appending the bin location to the list and adding the mass of the container to the total mass
        containerTraits = dispenseContainer()
        container_info_list.append(containerTraits[2])
        totalMass += containerTraits[1]
        print("Total mass of the " + str(counter+1)+" container(s) is: ", totalMass, "g.")

        # If the total mass of the containers (on the Q-bot and one container on the table) is less than 90
        if totalMass < 90:
            if counter == 0:
                print(containerTraits[2])
                #Q-arm moves the container onto the Q-bot
                container_drop_off(counter)
                counter += 1
                sleep(2)

                
            # If the dispensed bottle (on the table) is going to the same bin destination as the previous container, then the Q-arm will move the container to the Q-bot
            elif container_info_list[counter - 1] == containerTraits[2] and counter != 0 :
                container_drop_off(counter)
                counter += 1
                sleep(2)

            else:
                # If the bottle on the table is not going to the same bin destination as the bottle on the Q-arm, the the function will end
                break
        else:
            # If the total mass is greater than or equal to 90
            break

        
    return container_info_list

    
# Tranfers the container(s) to the right bin
def containerTransfer(cycles): #Shiv Patel

    #Dispenses and loads container
    container_info_list = loadContainer(cycles)

    print(container_info_list)
    print ("\nThe container(s) will be deposited into", container_info_list[0]+".")
    print ("\n\nAdditionally, the container on the table will be dispensed into",container_info_list[len(container_info_list)-1]+" during the next run." )
    

    # Activiates the line following and color sensor
    bot.activate_line_following_sensor()
    sleep(0.5)
    bot.activate_color_sensor()


    # variables used to indicate if the sensor is on or off
    ultrasonicStatus = False
    colorSensorOff = False
    
    while True == True:
        lineFollowValues = bot.line_following_sensors()
        
        lineFollowLeft = lineFollowValues[0]
        lineFollowRight = lineFollowValues[1]

        # When the bot is on the line, the bot goes straight
        if lineFollowLeft == 1 and lineFollowRight == 1:
            bot.set_wheel_speed([0.1,0.1])
        # When the right wheel is off the line, then the bot will pivot on the left wheel
        elif lineFollowLeft == 1 and lineFollowRight == 0:
            bot.set_wheel_speed([0,0.03])
        # When the left wheel is off the line, then the bot will pivot on the right wheel
        elif lineFollowLeft == 0 and lineFollowRight == 1:
            bot.set_wheel_speed([0.03,0])
        else:
            bot.set_wheel_speed([0.5,0.2])

        
        # Once the ultrasonic sensor was turned on, the color sensor will turn off
        if ultrasonicStatus == False:
            colorSensorInfo = bot.read_color_sensor()
        elif ultrasonicStatus == True and colorSensorOff == False :
            bot.deactivate_color_sensor()
            colorSensorOff = True

        
        # If the color sensor matches the correct bin location, the ultrasonic sensor is turned on.
        if ultrasonicStatus == True and container_info_list[0] == 'Bin01' or container_info_list[0] == 'Bin01' and colorSensorInfo[0][0] == 1:
            if ultrasonicStatus == False:
                bot.activate_ultrasonic_sensor()
                ultrasonicStatus = True

            # When the Q-bot is a certain distance away from the bin, the Q-bot will drop the container into the bin
            ultrasonicSensorInfo = bot.read_ultrasonic_sensor()
            print(ultrasonicSensorInfo) 
            if ultrasonicSensorInfo < 0.065:
                container_unload()
                break

        elif ultrasonicStatus == True and container_info_list[0] == 'Bin02' or container_info_list[0] == 'Bin02' and colorSensorInfo[0][1] == 1:
            if ultrasonicStatus == False:
                bot.activate_ultrasonic_sensor()
                ultrasonicStatus = True
                
            ultrasonicSensorInfo = bot.read_ultrasonic_sensor()
            print(ultrasonicSensorInfo)
            if ultrasonicSensorInfo <= 0.020:
                container_unload()
                break

        elif ultrasonicStatus == True and container_info_list[0] == 'Bin03' or container_info_list[0] == 'Bin03' and colorSensorInfo[0][2] == 1:
            if ultrasonicStatus == False:
                bot.activate_ultrasonic_sensor()
                ultrasonicStatus = True
                
            ultrasonicSensorInfo = bot.read_ultrasonic_sensor()
            print(ultrasonicSensorInfo) 
            if ultrasonicSensorInfo <= 0.038:
                container_unload()
                break

        elif ultrasonicStatus == True and container_info_list[0] == 'Bin04' or container_info_list[0] == 'Bin04' and colorSensorInfo[0][0] == 5:
            if ultrasonicStatus == False:
                bot.activate_ultrasonic_sensor()
                ultrasonicStatus = True
                
            ultrasonicSensorInfo = bot.read_ultrasonic_sensor()
            print(ultrasonicSensorInfo) 
            if ultrasonicSensorInfo <= 0.025:
                container_unload()
                break


    return None


# The actuator will activate and the container will drop in the box - Himesh Mistry
def container_unload(): 
    '''
    In order to make sure the containers do not go flying when they are being transferred to the bins,
    The hopper is incremented slowly with pauses in between to allow for a smooth transfer. 
    '''
    bot.stop()

    #The actuator is slowly getting lifted in order for the container to be dropped off and not be thrown. 
    bot.activate_linear_actuator()
    bot.rotate_hopper (30)
    sleep(1.5)
    bot.rotate_hopper(60)
    sleep(1.5)
    bot.rotate_hopper(90)

    sleep(1.5)
    bot.rotate_hopper (0)
    bot.deactivate_linear_actuator()


    bot.deactivate_color_sensor()

''' Function to return bot to home position after dropping off container'''
def bot_return_home(bot_home_position): #Himesh Mistry & Shiv Patel

    #Home coordinates 

    home_position = bot_home_position
    current_position = []
    bot.activate_line_following_sensor()
    
    while True == True:
        lineFollowValues = bot.line_following_sensors()
        lineFollowLeft = lineFollowValues[0]
        lineFollowRight = lineFollowValues[1]
        current_position = bot.position()
        
        '''
        Home position is passed as a parameter and
        if current position is within a 5% difference on the x and y coordinates, bot stops.
        The bot must also be oriented straightly to stop.
        '''
        # Bot stops if its on or close to the home position
        if current_position[0]/home_position[0] >= 0.95 and current_position[1]/home_position[1] >= 0.95 and lineFollowValues[0] == 1 and lineFollowValues[1] == 1:
            bot.stop()
            break
        
        # Following the Q-bot path
        if lineFollowLeft == 1 and lineFollowRight == 1:
            bot.set_wheel_speed([0.1,0.1])

        elif lineFollowLeft == 1 and lineFollowRight == 0:
            bot.set_wheel_speed([0,0.03])
        elif lineFollowLeft == 0 and lineFollowRight == 1:
            bot.set_wheel_speed([0.03,0])
        else:
            bot.set_wheel_speed([0.5,0.2])


    # Small adjustement to the bot. (rotating the bot so it's in the right position
    sleep(3)
    bot.rotate(-15)
    sleep(3)
    bot.forward_time(2.5)
    sleep(3)
    bot.rotate(100)
    sleep(3)
    bot.forward_time(0.9)
    sleep(3)
    bot.rotate(-100)
    return None

# Function that is implemented in main() to allow user to continue or terminate the code, based on their preference
def userInput (): # Shiv Patel
    print ("\n")
    userChoice = input("Would you like to continue? ('Y' for yes or 'N' for no): ")
    while userChoice != "Y" and userChoice != "N": 
        userChoice = input("Would you like to continue? ('Y' for yes or 'N' for no): ")
    else: 
        if userChoice == "Y": 
            return True
        else: 
            return False

# Where all the functions will be called - Himesh Mistry
def main ():
    cycle_count = 1
    imports ()

    continuation = True
    
    bot_home_position = initialHomePositionBot()

    while continuation == True: #Indefinite loop is set, unless the value of continuation is changed
    
        sleep(1.5)

        containerTransfer(cycle_count)

        sleep(3)

        bot_return_home(bot_home_position)

        sleep(1.5)

        containerTransfer(cycle_count+1)

        sleep(3)

        bot_return_home(bot_home_position)

        continuation = userInput () #User can decide whether they would like to terminate or continue

        cycle_count+= 1 

    else: 
        systemExit ()


# Calling the main() function
main ()











#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

