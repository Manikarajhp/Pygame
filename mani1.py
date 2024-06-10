from pygame import *
from pygame import mixer
import random
init()

##FONT STYLE DEFINTION
font1=font.Font("freesansbold.ttf",18)
font=font.Font("freesansbold.ttf",28)

##CLOCK SPEED TI CONTROL FRAME RATE
clock=time.Clock()

##DISPLAY SETTING
width=415
height=725
win=display.set_mode((width,height))

##IMAGE LOADING SECTION
bg_road=image.load("road.png")
coin_img=image.load("dollar.png")
coin_img=transform.scale(coin_img,(32,32))
start_btn=image.load("start.png")
start_btn=transform.scale(start_btn,(128,128))
car1=image.load("car.png")
car2=image.load("car1.png")
car3=image.load("car2.png")
car4=image.load("car3.png")
car5=image.load("car4.png")
car1=transform.scale(car1,(64,64))##TRANSFORM THE SIZE OF CAR
car2=transform.scale(car2,(64,64))
car3=transform.scale(car3,(64,64))
car4=transform.scale(car4,(64,64))
car5=transform.scale(car5,(64,64))
rcar1=transform.rotate(car1,(-180))
rcar2=transform.rotate(car2,(-180))
rcar3=transform.rotate(car3,(-180))
rcar4=transform.rotate(car4,(-180))
rcar5=transform.rotate(car5,(-180))
buy_btn=image.load("buy.png")
replay_img=image.load("replay.png")
quit_img=image.load("door.png")

##DATA FILE LOADING SECTION
data_file=open("data.txt","r")
read_lines=data_file.readlines()
data_file.close()

##COMMON VARIABLES DECLARATION
wallet=int(read_lines[0])
hi_score=int(read_lines[1])
owned_cars=read_lines[2].split()
pos=(0,0)##MOUSEPOSITION
selected_car=car1
option=0##CONTROLL THE ENTIRE GAME
speed=1##SPEED OF THE PLAYER CAR
top_speed=0##TOP SPEED OF THE PLAYER CAR
buy_car=car1

##CARS LIST AND IT'S FEATURES
car_list=[{"name":car1,"rate":0,"speed":5,"disp":((width/2)-115,(height/2)-190)},
          {"name":car2,"rate":2000,"speed":10,"disp":((width/2)-32,(height/2)-190)},
          {"name":car3,"rate":5000,"speed":20,"disp":((width/2)+53,(height/2)-190)},
          {"name":car4,"rate":8000,"speed":30,"disp":((width/2)-80,(height/2)-90)},
          {"name":car5,"rate":12000,"speed":50,"disp":((width/2)+15,(height/2)-90)}]


def starting_page():
    global selected_car,wallet,owned_cars,option,top_speed,buy_car
    win.blit(bg_road,(0,0))##BACKGROUND FILLING
    win.blit(coin_img,(25,15))##BLIT COIN AT TOP LEFT CORNER
    txt_wallet=font.render(str(wallet),True,("white"))
    win.blit(txt_wallet,(60,18))##BLIT TOTAL AMOUNT COLLECTED AT TOP LEFT CORNER
    draw.rect(win,("lightblue"),((width/2)-125,(height/2)-200,250,200),0,10)##GARAGE BACKGROUND
    draw.rect(win,("black"),((width/2)-125,(height/2)-200,250,200),3,10)##GAREAGE BG OUTLINE
    win.blit(start_btn,((width/2)-64,(height/2)))##BLIT START BUTTON
    txt_hi=font.render("High Score:"+str(hi_score),True,("white"))
    win.blit(txt_hi,(200,18))##BLIT HI AT TOP RIGHT CORNER
    
    if ((width/2)-64<pos[0]<(width/2)+64) and ((height/2)<pos[1]<(height/2)+64):##CHANGE THE OPTION VALUE WHEN STAT BUTTON CLICKED
        option=1
    if ((width/2)-32<pos[0]<(width/2)+32) and (height-150<pos[1]<height-150+64):##TO BUY THE SELECTED CAR
        for car in car_list:
            if car["name"]==buy_car:
                if wallet>=car["rate"]:
                    wallet-=car["rate"]
                    owned_cars[car_list.index(car)]='1'
                else:
                    draw.rect(win,("black"),((width/2)-120,height-200,265,25),0,10)
                    txt_alert=font1.render("you don't have enough money.",True,("yellow"))##ALERT MESSAGE AT BOTTOM CENTER
                    win.blit(txt_alert,((width/2)-115,height-200))
    for car in car_list:
        win.blit(car["name"],car["disp"])
        txt_rate=font1.render("$"+str(car["rate"]),True,("blue"))
        win.blit(txt_rate,(car["disp"][0]+10,car["disp"][1]+70))
        if (car["disp"][0]<pos[0]<car["disp"][0]+64) and (car["disp"][1]<pos[1]<car["disp"][1]+64):##TO SELECT THE CAR
            draw.rect(win,("black"),(car["disp"][0],car["disp"][1],64,64),2,10)
            txt_feat=font.render("Speed:"+str(car["speed"]),True,("yellow"))
            win.blit(txt_feat,((width/2)-64,120))##SHOW THE SPEED OF CAR AT THE TOP OF GAREAGE
            if owned_cars[car_list.index(car)]=='1':
                selected_car=car["name"]
                top_speed=car["speed"]
            else:
                buy_car=car["name"]
                selected_car=car1
                top_speed=5
                draw.rect(win,("black"),((width/2)-160,height-200,330,32),0,10)
                txt_alert=font.render("you don't own the car.",True,("yellow"))
                win.blit(txt_alert,((width/2)-145,height-200))
                win.blit(buy_btn,((width/2)-32,(height-150)))
        else:
            top_speed=5
            
##ENEMY CAR RANDOM GENERATION AND ITS POSITIONS
enemy_list=[{"name":car1,"speed":random.randint(1,speed),"disp":[55,-64],"way":'l'},
            {"name":car2,"speed":random.randint(1,speed),"disp":[135,-128],"way":'l'},
            {"name":rcar3,"speed":random.randint(speed+1,speed+4),"disp":[220,-32],"way":'r'},
            {"name":rcar5,"speed":random.randint(speed+1,speed+4),"disp":[305,-96],"way":'r'}]
coins_list=[{"disp":[55,-64]},{"disp":[135,-128]},{"disp":[220,-188]},{"disp":[305,-256]}]

##VARIABLES FOR RACE FUNCTION USE
bg_motion=speed
car_motion=int((width/2)-32)
bg1_pos=0
bg2_pos=-(height)+1
direction=0
speed_ctrl=0
list_of_cars=[[car1,car2,car3,car4,car5],[rcar1,rcar2,rcar3,rcar4,rcar5]]
score=0
collected_coins=0


def race():
    global car_motion,bg1_pos,bg2_pos,speed,collected_coins,option,pos,score
##    SPEED CONTROLLING SYSTEM
    if speed>=top_speed:
        speed=top_speed
    if speed<=0:
        speed=1
    speed+=speed_ctrl
##    BG CONTROLLING SYSTEM
    bg1_pos+=speed
    bg2_pos+=speed
    if bg2_pos>height:
        bg2_pos=-(height)+1
        score+=1
    if bg1_pos>=height:
        bg1_pos=-(height)+1
        score+=1
##    IF CAR CROSSE THE LEFT AND RIGHT BORDER GAMEOVER
    if car_motion<20 or car_motion>330:
        pos=(0,0)
        option=2
##        DISPLAYING THE BG ROAD
    win.blit(bg_road,(0,bg1_pos))
    win.blit(bg_road,(0,bg2_pos))
##    ENEMY CAR DISPLAY SYSTEM
    for ecar in enemy_list:
        win.blit(ecar["name"],tuple(ecar["disp"]))
        ecar["disp"][1]+=ecar["speed"]
##        PLAYER CAR HIT WITH ENEMY CAR OPERATION
        if ((ecar["disp"][0]+16<car_motion+48<ecar["disp"][0]+48) or (ecar["disp"][0]+16<car_motion+16<ecar["disp"][0]+48)) and ((ecar["disp"][1]<(height-100)<ecar["disp"][1]+32) or (ecar["disp"][1]<(height-100+64)<ecar["disp"][1]+32)):
            pos=(0,0)
            option=2
##            ENEMY CAR CROSSES BOTTOM OF DISPLAY IT WILL BE AGAIN STATING AT FROM TOP
        if ecar["disp"][1]>height:
            if ecar["way"]=='l':
                ecar["name"]=random.choice(list_of_cars[0])
                ecar["speed"]=random.randint(1,speed)
            else:
                ecar["name"]=random.choice(list_of_cars[1])
                ecar["speed"]=random.randint(speed+1,speed+4)
            ecar["disp"][1]=random.randint(-128,-64)
##    COIN MANAGEMENT AND DISPLAY SYSTEM
    for coin in coins_list:
        win.blit(coin_img,tuple(coin["disp"]))
        coin["disp"][1]+=speed
##        COIN CROSSES DISPLAY
        if coin["disp"][1]>height:
            coin["disp"][1]=random.randint(-256,-32)
##        COIN HIT WITH CAR
        if ((coin["disp"][0]<car_motion+16<coin["disp"][0]+32) or (coin["disp"][0]<car_motion+32<coin["disp"][0]+32)) and ((coin["disp"][1]<(height-100)<coin["disp"][1]+32) or (coin["disp"][1]<(height-100+64)<coin["disp"][1]+32)):
            collected_coins+=1
            coin["disp"][1]=random.randint(-256,-32)
##            BLITTING COIN
    win.blit(coin_img,(25,15))
    txt_coin=font.render(str(collected_coins),True,("white"))
    win.blit(txt_coin,(60,18))##DISPLAY THE COLLECTED COIN AT THE TOP LEFT CORNER 
    txt_km=font.render("KM:"+str(score),True,("white"))
    win.blit(txt_km,(25,50))##DISPLAY THE KM SCORE AT THE TOP LEFT CORNER
    txt_speed=font.render("SPEED:"+str(speed),True,("white"))
    win.blit(txt_speed,(25,80))##DISPLAY THE SPEEDD OF CAR AT THE TOP LEFT CORNER
    car_motion+=direction
    win.blit(selected_car,(car_motion,height-100))##DISPLAYING THE PLAYER SELECTED CAR

    
def gameover():
    win.blit(bg_road,(0,0))
    win.blit(selected_car,(car_motion,height-100))
    for ecar in enemy_list:
        win.blit(ecar["name"],tuple(ecar["disp"]))
    win.blit(replay_img,((width/2)-64,(height/2)-100))##REPLAY BUTTON
    win.blit(quit_img,((width/2)-64,(height/2)+50))##QUIT BUTTON
    txt_hi=font.render("High Score:"+str(hi_score),True,("white"))
    win.blit(txt_hi,((width/2)-70,(height/2)-250))##DISPLAY THE HI AT THE TOP LEFT CORNER
    txt_score=font.render("Score:"+str(score),True,("white"))
    win.blit(txt_score,((width/2)-55,(height/2)-200))
    win.blit(coin_img,((width/2)-35,(height/2)-150))
    txt_coin=font.render(str(collected_coins),True,("white"))
    win.blit(txt_coin,((width/2)+10,(height/2)-150))
##    UPDATEING THE VALUES TO BE STORED IN DATA FILE
    read_lines[0]=str(wallet+collected_coins)+"\n"
    if hi_score<score:    
        read_lines[1]=str(score)+"\n"
    temp=""
    for i in owned_cars:
        temp+=(i+' ')
    read_lines[2]=temp
    data_file=open("data.txt","w")
    data_file.writelines(read_lines)
    data_file.close()
    if ((width/2)-64<pos[0]<(width/2)-64+128) and ((height/2)-100<pos[1]<(height/2)-100+128):
        replay()
    if ((width/2)-64<pos[0]<(width/2)-64+128) and ((height/2)+50<pos[1]<(height/2)+50+128):
        quit()


def replay():
    global read_lines,wallet,hi_score,owned_cars,pos,selected_car,option,speed,score,top_speed,buy_car,enemy_list,coins_list,collected_coins
    data_file=open("data.txt","r")
    read_lines=data_file.readlines()
    data_file.close()
    wallet=int(read_lines[0])
    hi_score=int(read_lines[1])
    owned_cars=read_lines[2].split()
    pos=(0,0)##MOUSEPOSITION
    selected_car=car1
    option=0
    speed=1
    score=0
    top_speed=5
    buy_car=car1
    collected_coins=0
    enemy_list=[{"name":car1,"speed":random.randint(1,2),"disp":[55,-64],"way":'l'},
                {"name":car2,"speed":random.randint(1,3),"disp":[135,-128],"way":'l'},
                {"name":rcar3,"speed":random.randint(1,2),"disp":[220,-32],"way":'r'},
                {"name":rcar5,"speed":random.randint(1,3),"disp":[305,-96],"way":'r'}]
    coins_list=[{"disp":[55,-64]},{"disp":[135,-128]},{"disp":[220,-188]},{"disp":[305,-256]}]


def game():
    global pos,direction,speed_ctrl,option
    while 1:
        win.fill("brown")
        for eve in event.get():
            if eve.type==QUIT:
                quit()
            if eve.type==MOUSEBUTTONDOWN:
                if eve.button==1:
                    pos=mouse.get_pos()
                    
            if eve.type==KEYDOWN:
                if eve.key==K_LEFT:
                    direction=-5
                if eve.key==K_RIGHT:
                    direction=5
                if eve.key==K_UP:
                    speed_ctrl=1
                if eve.key==K_DOWN:
                    speed_ctrl=-1
                if eve.key==K_RETURN:
                    option=1
                
            if eve.type==KEYUP:
                direction=0
                speed_ctrl=0
        if option==0:
            starting_page()
        elif option==1:
            race()
        elif option==2:
            gameover()
        clock.tick(60)
        display.update()
game()
