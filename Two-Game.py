#!/usr/bin/python


# V16 now under GIT control
''' special thanks to saltycrane for the timeout_decorator. All
sound effects public domain from freesound.com, photos courtesy
of Bonehenge.  This is a Frobozz Project'''

# IMPORTS START --------------------------------------------------
# makes extensive use of pygame to blit the screen

from random import randrange, shuffle, random, sample
#from random import sample
from time import sleep, time
import sys, pygame
from pygame.locals import *
import pygame.font
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import os
# code to use comma seperated values
import csv
# code to break up long strings
import textwrap
''' this decorater wraps the major functions and methods
to allow resetting the game if they walk away'''
import timeout_decorator

FPS = 30
game1 = False
# game 2 variables
list_file = 'qna_pool.csv'
file_error = False
row_count = 0
donation = False


# IMPORTS END ____________________________________________________

# VARIABLE INITIALIZE START----------------------------------------
max_pic = 12
rnums = []

display_pic = 0
resp = 0
free = False # playing for free flag
win = False # winner flag
payout = 50 # percentage of winners

image_centerx = 960
image_centery = 540
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
# blit location for arrows used throughout
arrow_loc = ((15, 890), (452, 890), (895, 890), (1337, 890), (1775, 890))

# global var that gets set by which_game
game1 = True

pos_resp =['Correct','Got it, Nice','Right','Good Pick','Way to go','On a roll']
neg_resp =['Sorry','Nope','Not that one','Too bad','Gotcha','Maybe next time']
final_resp =['Better Try Again','Keep Working at it','Got a Couple','Pretty Good','Excellent Nice Job','100% Wow!']
# prize names and indexes 
big_prize = ['Blue', 'Fin', 'Humpback', 'Minke', 'Right']
small_prize = ['Bottlenose', 'Dwarf', 'Porpoise', 'Pygmy', 'Spotted']
big_index = 0
small_index = 0
# set the delay for reset if they walk away
MASTER_TIMEOUT = 300
# VARIABLE INITIALIZE END _________________________________________

# GPIO PORTS START ------------------------------------------------
# Define Ports if portList starts with a 0 it is output
# if it starts with a 1 it is input
# Port assignments 1 [in,4-B1,17-B2,27-B3,22-B4,5-B5,6-Rst]
portList = [1,4,17,27,22,5,6]
# Port assignments 2 [in,13-Free,26-Pay]
portList2 = [1,13,26]
# Port assignments 3 [out, 23-Bell, 16 Light Relay, 24 B1,
#                     25 B2, 12 B3, 18 B4, 14 B5]
portList3 = [0, 23, 16, 24, 25, 12, 18, 14]
# GPIO PORT END ___________________________________________________

# DEFINE CLASES START ---------------------------------------------

# DEFINE CLASES END _______________________________________________

# ///////////////////////////////////////////////////////////////////
# METHODS AND FUNCTIONS START --------------------------------------
def init():
    # initialize code can go here
    pass

def portassign(ports):
    # assign ports based on index[0] if 0 Output else Input
    
    if ports[0] == 0:
        #print('Output')
        for index in range(1, len(ports)):
            GPIO.setup(ports[index], GPIO.OUT)
            
            #print(ports[index])
    else:
        #print('Input')
        for index in range(1, len(ports)):
            GPIO.setup(ports[index], GPIO.IN, pull_up_down = GPIO.PUD_UP)
            #print(ports[index])
            




def shuffle_pics():
    '''uses max_pic to randomize pictures
     this is only called once per game and sets
     the lookup order of rnums like this [2,3,0,1,4]
     so each turn has the same layout but
     different chalange pictures '''
    global rnums
    # now gets random sample of a range of numbers to max_pic
    rnums = sample(range( 0, max_pic), 5)
    # rnums is a shuffled list of the picture numbers for choosing
    print('rnums is now>>> ' + str(rnums))
    # iterate to build a list of random numbers

# the timeout decorator wraps this so if user walks away
# it will reset
@timeout_decorator.timeout(MASTER_TIMEOUT,use_signals=True)
def free_cash(picture):
    ''' called by both games selects if it is a free game or
    if they put in some money sets global variables'''
    # display rules and wait for input
    global free
    global win
     
    display.blit(picture, (0, 0))
    greeting = 'Press Free Play'
    font_process(60, greeting, white, image_centerx, 200)
    greeting = 'or'
    font_process(60, greeting, white, image_centerx, 280)
    greeting = 'Make a Donation and get a chance to win a Bonehenge Prize'
    font_process(60, greeting, white, image_centerx, 360)
    greeting = 'Prizes are awarded for 5 of 5 or 4 of 5 correct answers'
    font_process(30, greeting, white, image_centerx, 800)
    greeting = 'If you win you will see your winner code word'
    font_process(30, greeting, white, image_centerx, 850)
    pygame.display.flip()
    
    # Select if this is a paid or free play
    # forever loop until timeout_decorator kicks in
    while True:
        sleep(.05)
        #print('in pay detection')
        if GPIO.input(portList2[1]) == GPIO.LOW:
            sleep(.08)
            free = True
            win = False
            print('Free Play')
            break
                
        if GPIO.input(portList2[2]) == GPIO.LOW:
            #print('PLAYBACK SHOULD HAPPEN')
            sleep(.08)
            free = False
            win = False # set it false for now
            Rnd_Chance = int(random() * 100 )
            play_sound('Yay.mp3', .3)
            
            
            if Rnd_Chance <= payout:
                win = True
                print('A Winner')
                
            else:
                win = False
                print('A Loser')
            break


def game1_intro():
    ''' displays rules for the dolphin game'''
    white = (255, 255, 255)
    black = (0, 0, 0,)
    red = (255, 50, 50)
    display.blit(g1_bkg, (0, 0))
    greeting = 'Hello Welcome to ID the Dolphin'
    font_process(60, greeting, white, image_centerx, 100)
    pygame.display.flip()
    sleep(2)

    info = 'We can identify individuals by their dorsal fin shape'
    font_process(50, info, white, image_centerx, 200)
    

    inst = 'See if you can match one on the bottom row to the top picture'
    font_process(50, inst, white, image_centerx, 300)
    pygame.display.flip()
    if not free:
        sleep(2) # allow prev sound to end
    play_sound('pinball-start.mp3', .5)
    sleep(5.5)
    display.blit(g1_bkg, (0, 0))
    pygame.display.flip()


def font_process(size, message, color, x, y):
    ''' combines everthing needed to blit fonts to the screeen,
    called from various methods that use fonts'''
    # attempt to combine all font operations into one call that
    # renders and blits the text
    
    black = (0,0,0)
    d_shadow = 3
    # create a font object from a system font
    font = pygame.font.SysFont('FreeSans', size, True, False)
    # render font on a new surface font.render(text, antialias, bkgnd = none)
    render_message = font.render(message, True, color)
    # render drop shadow in black
    if d_shadow:
        render_ds = font.render(message, True, black)
        render_ds_rect = render_message.get_rect()
    # attempt to center works
    # create a rectangular object for the text surface object
    render_msg_rect = render_message.get_rect()
    
    # center in x, use y from call
    #render_msg_rect.center = (image_centerx, y) # (x,y) x = screen center
    render_msg_rect.center = (x, y) # (x,y) x = screen center
    # blit drop shadow then text to image
    if d_shadow:
        #render_ds_rect.center = (image_centerx + d_shadow, y + d_shadow)
        render_ds_rect.center = (x + d_shadow, y + d_shadow)
        display.blit(render_ds, render_ds_rect)
    display.blit(render_message, render_msg_rect)
    # no flip here up to the caller


# ////////////////////// SMALL UTILITIES \\\\\\\\\\\\\\\\\\\\\
def play_sound(sfile, vol):
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.load(gpath + sfile)
    pygame.mixer.music.play()

def parse_string(long_string, final_length):
    # this handy util breaks up long lines for us
	lines_list = textwrap.wrap(long_string, final_length)
	# will return any number of lines of final_length
	return lines_list 

def change_lights(light_config):
    '''allows for any configuration of the light as they
       can be individually controlled'''
    # central point to control panel lights
    # portList3 = [I/O, [1]-Bell, [2]Light Relay, [3] B1,
    #             [4] B2, [5] B3, [6] B4, [7] B5]
    # For buttons if the port is high light is on
    # For Free/Donate port high = on

    if light_config == 0: # Free/Donate on Buttons off
        ports_high = [portList3[2], ]
        ports_low =[portList3[3],portList3[4], portList3[5],
        portList3[6], portList3[7]] 
        drive_lights(ports_high, ports_low)

    if light_config == 1: # 5 button lights on
        ports_high = [portList3[3],portList3[4], portList3[5],
        portList3[6], portList3[7]] 
        ports_low = [portList3[2]]
        drive_lights(ports_high, ports_low)
    
    if light_config == 2: # Free/Donate off, Buttons 1, 5 on
        ports_high = [portList3[3], portList3[7]]
        ports_low =  [portList3[2], portList3[4], portList3[5], portList3[6]]
        drive_lights(ports_high, ports_low)

    if light_config == 3: # Free/Donate off, Buttons 1, 3, 5 on
        ports_high = [portList3[3], portList3[5], portList3[7]]
        ports_low =  [portList3[2], portList3[4], portList3[6]]
        drive_lights(ports_high, ports_low)


def drive_lights(ports_high, ports_low):
    # get two lists of ports to turn on or off
    for items in ports_high:
        GPIO.output(items, True)
    for items in ports_low:
        GPIO.output(items, False)

def reset_pressed(port):
    print('Shutdown Button Pressed')
    GPIO.cleanup()
    sys.exit()
    

# ////////////////////// END SMALL UTILITIES \\\\\\\\\\\\\\\\\\\\\


# ------------------------- Where all the action happens --------------
@timeout_decorator.timeout(MASTER_TIMEOUT,use_signals=True)
def play_loop():
    '''this is the big kahona it calls send_to_screen that puts up
    the pictures, which_pic2 that waits for a button press and
    returns an answer, play_loop returns final_score to the 
    main program'''
    right_ans = 0  # scoring
    wrong_ans = 0  # scoring
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    turn = 0  # used to access comp_pic

    # set the content of the two lists to be equal
    display_pics = rnums[:]
    # now scramble order of display
    shuffle(display_pics)
    #print('display pics is now ' + str(display_pics))
    #print('rnums is now--- ' + str(rnums))
   
    # use display_pic to put up that pic on top (chalange pic)
    # use rnums to show all pics on bottom (computer pics)
    change_lights(1) # turn on the button lights


    # ========= Loop Start ============
    for items in rnums:
        #shuffle_pics()
        
        display_pic = display_pics[turn]  # picks a new one each turn
        caption = 'Match this Fin: Chance # ' + str(turn + 1)
        send_to_screen(display_pic, rnums, caption)  # put up the challenge screen

        #  go get user response
        resp = which_pic2() #  go and wait for button input return pic#
        print('back from which pic resp= '+ str(resp) + ' for pic# ' + str(display_pic))

        if resp == -1:
            score_msg = ('Delay Timeout')
            break

        if rnums[resp] == display_pic:
            pgm_rsp = pos_resp[randrange(len(pos_resp))]
            right_ans = right_ans + 1
            play_sound('Quick-win.mp3', .3)
            print(pgm_rsp)
            show_glow(rnums.index(display_pic), resp)
        else:
            pgm_rsp = neg_resp[randrange(len(neg_resp))]
            print(pgm_rsp)
            wrong_ans = wrong_ans + 1
            play_sound('Downer.mp3', .2)
            show_glow(rnums.index(display_pic), resp)

        
        score_msg = ('Current Score  '+ str(right_ans)+ ' right  '+ str(wrong_ans)+' wrong')
        # clear screen of old score and put up new one 
        display.blit(g1_bkg, (0, 0))
        font_process(60, score_msg, white, image_centerx, 500)
        font_process(60, pgm_rsp, white, image_centerx, 600)
        pygame.display.flip()
        turn = turn + 1
        
        sleep(1)
        # now display just the turn and score no response
        if turn != 5:
            display.blit(g1_bkg, (0, 0))
            font_process(60, score_msg, white, image_centerx, 500)
            pygame.display.flip()
    # =========== Loop End =============  
      
    return [right_ans, wrong_ans]
    # final score
    
def show_glow(green_pos, red_pos):
    # gets the green and red positions and blits screen
    #print('show_glow has green/red' + str(green_pos) + '/' + str(red_pos))
    start_x = 24
    glow_posx = [start_x, start_x + 380, start_x + 760, start_x + 1140, start_x + 1520]
    glow_posy = 570
    # display green alway
    display.blit(green_glow, (glow_posx[green_pos], glow_posy))
    if green_pos != red_pos:
        #display red also
        display.blit(red_glow, (glow_posx[red_pos], glow_posy))
    pygame.display.flip()
    sleep(2)


def which_pic2():
    '''this version uses the push buttons instead of touch screen
    gets called from play_loop and returns the answer.
    decided to do it as a polling loop rather than interrupts '''
    
    
    ans = -1 # this value will be set and returned to Play_Loop
    
        
        # run through all assigned pins
        # we start with an index of 1 to skip the Input/Output selector
    while True:
        for index in range(1, len(portList)):
            #sleep(.03) # debounce time
            if GPIO.input(portList[index]) == GPIO.LOW:
                ans = portList[index] # first pull the value
                ans = portList.index(portList[index]) -1 # then locate it in the list
                print('Button Press: ',str(ans))
            # reset game when free play is pressed
            #if GPIO.input(13) == GPIO.LOW:
                #raise timeout_decorator.TimeoutError
            
        if ans in range(0, 5):
            break # got our answer break out of forever loop
    return ans
                
            

    



def which_pic():
    while True:
        #  find out where the mouse/touch happened and return value
        #  this is an endless loop until right input
        '''  legacy code from touch screen, no longer used '''
        event = pygame.event.wait()
        ans = -1
        click_spot = (0, 0)
        #  setting a timer here so if they walk away it will cycle through
        #  and reset
        time_out = pygame.USEREVENT
        pygame.time.set_timer(time_out, 40000) #  40 seconds
        # if idle for too long bail out
        if event.type == time_out:
            print('time out happened')
            ans = 0
            break
        #  press or touch mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_spot =(pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            pygame.event.clear() #  flush out any time_out events


        if 5  <= click_spot[0] <= 155 and 40 <= click_spot[1] <= 190:
            print('selected 0')
            ans = 0
        if 165 <= click_spot[0] <= 315 and 40 <= click_spot[1] <= 190:
            ans = 1
            print('selected 1')
        if 325 <= click_spot[0] <= 475 and 40 <= click_spot[1] <= 190:
            ans = 2
            print('selected 2')
        if 485 <= click_spot[0] <= 635 and 40 <= click_spot[1] <= 190:
            ans = 3
            print('selected 3')
        if 645 <= click_spot[0] <= 795 and 40 <= click_spot[1] <= 190:
            ans = 4
            print('selected 4')
        if 0 <= click_spot[0] <= 50 and 430 <= click_spot[1] <= 480:
            # extreem lower left hidden exit
            pygame.quit()
            sys.exit()
        if ans in range(0, 5):
            break #  get out of endless loop
    return ans


def send_to_screen(challange, rnums, caption):
    '''called by play_loop puts up challange and user pictures from the 
    lists below'''
    # display_pic is challenge picture
    # should do the background graphic here
    your_pic = [uw1, uw2, uw3, uw4, uw5, uw6, uw7, uw8, uw9, uw10, uw11, uw12]
    comp_pic = [cw1, cw2, cw3, cw4, cw5, cw6, cw7, cw8, cw9, cw10, cw11, cw12]
    # enable the line below for easier testing
    #comp_pic = [uw1, uw2, uw3, uw4, uw5, uw6, uw7, uw8, uw9, uw10, uw11, uw12]
    # display the challenge pic
    # pygame.draw.rect(display, (128,128,255, 20), (815,16,350,350))
    display.blit(gray_glow,(802, 2)) # Gray background

    display.blit(comp_pic[challange],(840,40)) # Challange pic location
    # display the other pictures from list on bottom
    choicesx = 50
    choicesy = 600
    i = 0
    font_process(60, caption, (255,255,255), image_centerx, 400)
    
    for items in rnums:
        # use the rnums list to index your_pic list to get the pictures
        display.blit(blue_arrow, arrow_loc[i])
        display.blit(gray_glow,(choicesx - 38, choicesy - 38)) # Gray background
        display.blit(your_pic[items],(choicesx, choicesy))
        i = i + 1
        choicesx = choicesx + 380 # spacing for choices pics


    pygame.display.flip()

def which_game():
    ''' puts up select screen and sets game1 T or F'''
    # needs to light only buttons 1 & 5
    global game1
    change_lights(2) # turn on just 1 and 5
    print('which game will it be? ')
    display.blit(game_choice, (0, 0))
    greeting = 'Please select a game to play'
    font_process(80, greeting, white, image_centerx, 300)
    # first the left side
    greeting = 'Photo-ID Challenge'
    x = 430
    y = 600
    font_process(70, greeting, white, x, y)
    # chop these up
    y = y + 90
    greeting = 'See if you can match dolphin dorsal fins'
    parsed_lines = parse_string(greeting, 30)
    for item in parsed_lines:
        font_process(60, item, white, x, y)
        y = y + 70
    display.blit(blue_arrow, (arrow_loc[0]))
    # now the right side
    x = 1430
    y = 600
    greeting = 'Bonehenge Tour Quiz'
    font_process(70, greeting, white, x, y)
    y = y + 90
    greeting = 'Answer some questions about what you learned on your tour'
    parsed_lines = parse_string(greeting, 30)
    for item in parsed_lines:
        font_process(60, item, white, x, y)
        y = y + 70
    display.blit(blue_arrow, (arrow_loc[4]))
    
    
    
    pygame.display.flip()
    
    # forever polling loop
    while True:
    
        # wait for button press
        sleep(.05)
        if GPIO.input(portList[1]) == GPIO.LOW:
            game1 = True
            break
        if GPIO.input(portList[5]) == GPIO.LOW:
            game1 = False
            break
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('got the mouse')
            reset_pressed(6)
        # shutdown code goes here press buttons 2 & 4 
        if GPIO.input(portList[2]) == GPIO.LOW and GPIO.input(portList[4]) == GPIO.LOW:
            sleep(2)
            # are they still pressed?
            if GPIO.input(portList[2]) == GPIO.LOW and GPIO.input(portList[4]) == GPIO.LOW:
                GPIO.cleanup()
                os.system("sudo shutdown -h now")

        
    change_lights(0) # turn off the button lights   


# ------------------- GAME 2 CODE START --------------------------

def get_file(list_file):
    global row_count
    global file_error
    try:
        ''' call with file and get back list of lists'''
        with open(list_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rowlist = []
            questions_list = []
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    # avoids the header line
                    rowlist = [row[0]] # initalizes the list
                    rowlist.append(row[1])
                    rowlist.append(row[2])
                    rowlist.append(row[3])
                    questions_list.append(rowlist)
                    # this is a 0 based list of lists
                    # access questions_list[q# - 1][column]
                line_count += 1
            #print(f'Processed {line_count} lines.')
            row_count = line_count - 1
            return [questions_list]
    except FileNotFoundError:
        print('qna_pool.csv data file not found')
        # print message on screen
        file_error = True
        


def pick_some(qpicks,rstart,rend):
    '''takes a number and returns list of randoms nums in a range'''
    pics_list = sample(range(rstart, rend), qpicks)
    print('game2 pics_list :' + str(pics_list))
    return [pics_list]     

def q_to_screen(rand_pick, questions):
    ''' gets the next question as a list and 
    moves answers around, gets called each turn'''
    this_one = questions[rand_pick]
    # randomize the next three and assign to buttons
    #print('this one in q to scrn ' + str(this_one))
    # this gives us a scramble list
    screen_order = sample(range(1,4),3)
    # a list like [1,2,3] or [3,1,2] that orders the answers
    # put screen stuff together with font_process
    return screen_order


def get_user_ans(rand_pic, right_ans, questions, screen_order):
    ''' matches user input to correct answer '''
    #print('get usr ans has ' + str(right_ans))
    # display stuff
    white = (255, 255, 255)
    arrow_y = 900
    # print('Question is ' + str(questions[rand_pic][0]))
    ans_font = 60
    display.blit(g2_bkg, (0, 0))

    # now chop up the lines and display question
    parsed_lines = parse_string(str(questions[rand_pic][0]), 30)
    x = 990
    y = 100
    for item in parsed_lines:
        font_process(60, item, white, x, y)
        y = y + 70
    # puts all parsed answers in list for highlighting
    all_answers_parsed = []

    # now chop up the lines and display answers left first
    parsed_lines = parse_string(str(questions[rand_pic][screen_order[0]]), 20)
    all_answers_parsed.append(parsed_lines)
    x = 320
    y = 500 # this gets reset each time in case answer is multi line
    for item in parsed_lines:
        font_process(ans_font, item, white, x, y)
        y = y + 70
    display.blit(blue_arrow, (arrow_loc[0])) 
    # middle answer  
    parsed_lines = parse_string(str(questions[rand_pic][screen_order[1]]), 20)
    all_answers_parsed.append(parsed_lines)
    x = 990
    y = 500
    for item in parsed_lines:
        font_process(ans_font, item, white, x, y)
        y = y + 70 
    display.blit(blue_arrow, (arrow_loc[2])) 
    # right most answer   
    parsed_lines = parse_string(str(questions[rand_pic][screen_order[2]]), 20)
    all_answers_parsed.append(parsed_lines)
    x = 1600
    y = 500
    for item in parsed_lines:
        font_process(ans_font, item, white, x, y)
        y = y + 70    
    display.blit(blue_arrow, (arrow_loc[4])) 
    pygame.display.flip()
    # now display the reorderd choices
    # the index below questions is the big list then
    # [rand_pic] pics which of the questions and
    # [screen_order[X]] points the the reordered answers
    #user_ans = input('Select 1-3 ')
    user_ans = game2_input()
    # code below to be replaced with button input
    if user_ans == right_ans:
        correct = True
        play_sound('Quick-win.mp3', .3)
        show_answer(all_answers_parsed, user_ans, right_ans, ans_font)
    else:
        correct = False
        play_sound('Downer.mp3', .2)
        show_answer(all_answers_parsed, user_ans, right_ans, ans_font)
    return correct


def show_answer(all_answers, user_ans, right_ans, ans_font):
    ''' reblits text in red and green'''
    red = (255, 0, 0)
    green = (0, 255, 0)
    ans_xlocate = [320, 990, 1600]
    y = 500
    # first always blit the green answer
    for item in all_answers[right_ans - 1]:
        font_process(ans_font, item, green, ans_xlocate[right_ans -1], y)
        y = y + 70  
    y = 500
    # if they got it wrong put up the red text
    if user_ans != right_ans:
        for item in all_answers[user_ans - 1]:
            font_process(ans_font, item, red, ans_xlocate[user_ans -1], y)
            y = y + 70  

    pygame.display.flip()

    sleep(2)
    


def game2_input():
    ''' this waits for a port to go low, the slight delay is needed to 
    slow the polling'''
    
    #while GPIO.input(portList[1]) == GPIO.HIGH and GPIO.input(portList[3]) == GPIO.HIGH and GPIO.input(portList[5]) == GPIO.HIGH:
    while True:
        sleep(.05)
        if GPIO.input(portList[1])  == GPIO.LOW:
            ans = 1
            break
        if GPIO.input(portList[3])  == GPIO.LOW:
            ans = 2
            break
        if GPIO.input(portList[5])  == GPIO.LOW:
            ans = 3
            break
        # game reset from free play button
        #if GPIO.input(13) == GPIO.LOW:
                #raise timeout_decorator.TimeoutError
    return ans

# timer decorator

@timeout_decorator.timeout(MASTER_TIMEOUT,use_signals=True)
def take_turns():
    ''' like play_loop for game 1 this is the guts of game 2'''
    right_count = 0
    wrong_count = 0
    # get random q & a for this round
    q_pics = pick_some(5, 0, row_count )
    change_lights(3) # turn on 1, 3 and 5
    for turn_no in range(0,5):
        # put up the questions
        rand_pic = q_pics[0][turn_no]
        # rand_pic points to the index of the question 0 to row_count -1
        screen_order = q_to_screen(rand_pic, questions)
        right_ans = screen_order.index(1) + 1
        # go get answers lots of stuff in this call but it needs
        # all of it
        correct = get_user_ans(rand_pic, right_ans, questions, screen_order)
        # check if we can reuse code from game 1
        if correct:
            print('got it')
            pgm_rsp = pos_resp[randrange(len(pos_resp))]
            #play_sound('Quick-win.mp3', .3)
            right_count += 1
        else:
            print('no such luck')
            pgm_rsp = neg_resp[randrange(len(neg_resp))]
            #play_sound('Downer.mp3', .2)
            wrong_count += 1
        # display current score and message
        if turn_no != 4:
            score_msg = ('Current Score  '+ str(right_count)+ ' right  '+ str(wrong_count)+' wrong')
            # clear screen of old score and put up new one 
            display.blit(g2_bkg, (0, 0))
            font_process(60, score_msg, white, image_centerx, 500)
            font_process(60, pgm_rsp, white, image_centerx, 600)
            pygame.display.flip()
            sleep(2)
    return [right_count, wrong_count]        
# -------------------  GAME 2 CODE END ---------------------------

# -------------------- SHARED CODE FOR END ----------------------
def final_display(right_ans, wrong_ans):
    # final score
    global small_index
    global big_index
    global big_prize
    global small_prize
    score_msg = ('Final Score  '+ str(right_ans)+ ' right  '+ str(wrong_ans)+' wrong')
    final_msg = (final_resp[right_ans])
    final_sound = final_audio[right_ans]
    final_volume = final_vol[right_ans]
    play_sound(final_sound, final_volume)
    display.blit(finalscore, (0, 0))
    font_process(80, score_msg, white, image_centerx, 500)
    font_process(60, final_msg, white, image_centerx, 600)
    pygame.display.flip()
    sleep(1)
    msg_vert = 700
    if (right_ans == 5 or right_ans == 4) and not free:
        font_process(75,'You are a WINNER!!',red, image_centerx, msg_vert)
        font_process(75,'Please see one of our Staff for your prize',red, image_centerx, msg_vert + 100)
        if right_ans == 5:
            # award big prize
            if big_index < 4: # pick a winner code
                big_index += 1
            else:
                big_index = 0
            winner_code = big_prize[big_index]
            print('Large Prize')
            font_process(75,'Tell them your winner code is '+ '"' + winner_code + '"', red, image_centerx, msg_vert + 200)
        if right_ans == 4 and not free:    
            # award small prize
            if small_index < 4:
                small_index += 1
            else:
                small_index = 0
            print('Small Prize')
            winner_code = small_prize[small_index]
            font_process(75,'Tell them your winner code is '+ '"' + winner_code + '"', red, image_centerx, msg_vert + 200)
        sleep(3) # let sound above play out
        play_sound('fanfare.mp3', 1)
        GPIO.output(portList3[1], True) # turn on the bell
        sleep(.5)
        GPIO.output(portList3[1], False) # turn it off

    
    if right_ans < 4 and not free: 
        font_process(60,'Sorry, you did not win a prize this time', (175,175,255), image_centerx, 1000)

    pygame.display.flip()
    # change_lights(0) # turn off the button lights

    #  add delay here
    sleep(5)






# METHODS AND FUNCTIONS END _________________________________________
# ///////////////////////////////////////////////////////////////////


# INITIALIZE RUN ONCE CODE START ------------------------------------
#region
pygame.init()
pygame.mixer.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
screen_width = 1920
screen_height = 1080
bgColor = (0,0,0)
size = (screen_width, screen_height)

# assign I/O ports
portassign(portList) # main buttons
portassign(portList2) # free or pay
portassign(portList3) # output for bell and lights relays
GPIO.output(portList3[1], False) # no bell
change_lights(0) # no lights

# for developement uncomment the line below
#display = pygame.display.set_mode(size)
# for autostart to work properly uncomment the line below
display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#display = pygame.display.set_mode((1920,1080))

pygame.display.set_caption('ID The Dolphin')
pygame.mixer.music.set_volume(1.0)
# load the pics 'c' for computer 'u' for user
gpath = '/home/pi/My-Code/Dolphin-Project/graphics/'
udol1 = gpath + '25b.jpg'
udol2 = gpath + '26b.jpg'
udol3 = gpath + '75a.jpg'
udol4 = gpath + '86a.jpg'
udol5 = gpath + '100b.jpg'
udol6 = gpath + '126b.jpg'

udol7 = gpath + '271c.jpg'
udol8 = gpath + '454b.jpg'
udol9 = gpath + '618a.jpg'
udol10 = gpath + '706b.jpg'
udol11 = gpath + '1142b.jpg'
udol12 = gpath + '1726a.jpg'




# now set pointers to computer picks
cdol1 = gpath + '25a.jpg'
cdol2 = gpath + '26a.jpg'
cdol3 = gpath + '75b.jpg'
cdol4 = gpath + '86c.jpg'
cdol5 = gpath + '100a.jpg'
cdol6 = gpath + '126a.jpg'

cdol7 = gpath + '271b.jpg'
cdol8 = gpath + '454a.jpg'
cdol9 = gpath + '618b.jpg'
cdol10 = gpath + '706a.jpg'
cdol11 = gpath + '1142a.jpg'
cdol12 = gpath + '1726b.jpg'



g1_open_pict = gpath + 'game_1.jpg'
g2_open_pict = gpath + 'game_2.jpg'
#free_donate_pict = gpath + 'free_donate.jpg' #(not used)
game_choice_pict = gpath + 'game_choice.jpg'
finalscore_pict = gpath + 'finalscore.jpg'
# arrows
r_arro = gpath + 'red_arrow.png'
y_arro = gpath + 'yellow_arrow.png'
b_arro = gpath + 'blue_arrow.png'
# glows
g_gl = gpath + 'g-glow.png'
r_gl = gpath + 'r-glow.png'
gr_gl = gpath + 'gray-glow.png'
# path to sounds
awefile = gpath + 'Awe.mp3'
yayfile = gpath + 'Yay.mp3'
# audio files for final score
# had to convert a couple to mp3, pygame didn't like the wav version
final_audio = ('0_right.wav','1_right.wav','2_right.mp3','3_right.wav',
               '4_right.mp3','5_right.wav')
final_vol = (.3,1,1,.5,1,1)
# now to actually load them same letters this has to be done in two steps
# first the user pictures
uw1 = pygame.image.load(udol1).convert_alpha()
uw2 = pygame.image.load(udol2).convert_alpha()
uw3 = pygame.image.load(udol3).convert_alpha()
uw4 = pygame.image.load(udol4).convert_alpha()
uw5 = pygame.image.load(udol5).convert_alpha()
uw6 = pygame.image.load(udol6).convert_alpha()
uw7 = pygame.image.load(udol7).convert_alpha()
uw8 = pygame.image.load(udol8).convert_alpha()
uw9 = pygame.image.load(udol9).convert_alpha()
uw10 = pygame.image.load(udol10).convert_alpha()
uw11 = pygame.image.load(udol11).convert_alpha()
uw12 = pygame.image.load(udol12).convert_alpha()
# now the computer pictures
cw1 = pygame.image.load(cdol1).convert_alpha()
cw2 = pygame.image.load(cdol2).convert_alpha()
cw3 = pygame.image.load(cdol3).convert_alpha()
cw4 = pygame.image.load(cdol4).convert_alpha()
cw5 = pygame.image.load(cdol5).convert_alpha()
cw6 = pygame.image.load(cdol6).convert_alpha()
cw7 = pygame.image.load(cdol7).convert_alpha()
cw8 = pygame.image.load(cdol8).convert_alpha()
cw9 = pygame.image.load(cdol9).convert_alpha()
cw10 = pygame.image.load(cdol10).convert_alpha()
cw11 = pygame.image.load(cdol11).convert_alpha()
cw12 = pygame.image.load(cdol12).convert_alpha()
# full 1920 x 1080 images for backgrounds
g1_bkg = pygame.image.load(g1_open_pict).convert_alpha()
g2_bkg = pygame.image.load(g2_open_pict).convert_alpha()
#free_donate = pygame.image.load(free_donate_pict).convert_alpha() # not used
game_choice = pygame.image.load(game_choice_pict).convert_alpha()
finalscore = pygame.image.load(finalscore_pict).convert_alpha()
# small arrow with alpha
blue_arrow = pygame.image.load(b_arro).convert_alpha()

green_glow = pygame.image.load(g_gl).convert_alpha()
red_glow = pygame.image.load(r_gl).convert_alpha()
gray_glow = pygame.image.load(gr_gl).convert_alpha()

# path to qna file
ppath = '/home/pi/My-Code/Dolphin-Project/'
#endregion
# game 2 run once ------------------------
try:
    [questions] = get_file(ppath + list_file)
except:
    print('FILE IS MISSING')
    #once this is inside a loop ADD BREAK 
    

print('there are ' + str(row_count) + ' rows')
# pick 5 questions out of how many are in file
# this is a list of questions to be asked
# just need to do it once per game
# q_pics = pick_some(5, 0, row_count -1)
# whatever is in the 1 slot is correct pick
turn_no = 0
# game 2 run once end --------------------
# hardware reset on port 6
GPIO.add_event_detect(6, GPIO.FALLING, callback = reset_pressed)
pygame.mouse.set_visible(False) # kill the cursor

# INITIALIZE RUN ONCE CODE END _________________________________________

# ************************ MAIN START **********************************

def main():
    try:
        init()
        main_loop = True
        global game1
        # note init only runs once
        
        while main_loop:
            ''' here we choose the game and then drop into that game's
            loops. The timeout_decorator returns to this loop'''
            which_game()
            if game1:
                print('game one picked')
                
                print('Main Program')
                try:
                    free_cash(g1_bkg)
                except timeout_decorator.TimeoutError:
                    print('timeout from free_cash')
                    change_lights(0) # turn off the button lights
                    continue
                    
                
                game1_intro()
                shuffle_pics()
                try:
                    final_score = play_loop() # this is where all the work is done might want to break it up
                except timeout_decorator.TimeoutError:
                    print('timeout from play_loop')
                    change_lights(0) # turn off the button lights
                    continue

                final_display(final_score[0], final_score[1])
                sleep(3)
                print('Your final score is '+str(final_score[0])+' right and '+str(5 -final_score[0])+ ' wrong')
            

            else:
                print('picked game 2')
                
            
                # make it go
                # at start donation or free play?
                try:
                    free_cash(g2_bkg)
                except timeout_decorator.TimeoutError:
                    print('timeout from free_cash')
                    change_lights(0) # turn off the button lights
                    continue
                # globals free and win are now set
                try:
                    final_score = take_turns()
                except timeout_decorator.TimeoutError:
                    print('timeout from take_turns')
                    change_lights(0) # turn off the button lights
                    continue

                final_display(final_score[0], final_score[1])
                sleep(5)
                print('Your final score is '+str(final_score[0])+' right and '+str(5 -final_score[0])+ ' wrong')
            
            


    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        GPIO.cleanup()

if __name__ == '__main__':
    main()