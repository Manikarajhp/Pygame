from pygame import *
init()
width=height=500
scr_height=700
win=display.set_mode((width,scr_height))

#image
sqr_a=int(width/5)
snail_img=image.load("snail.png")
home_img=image.load("home.png")
leaf_img=image.load("leaf.png")
wall_img=image.load("wall.png")
reload_img=image.load("reload.png")

snail_img=transform.scale(snail_img,(sqr_a,sqr_a))
leaf_img=transform.scale(leaf_img,(sqr_a,sqr_a))
home_img=transform.scale(home_img,(sqr_a,sqr_a))
wall_img=transform.scale(wall_img,(sqr_a,sqr_a))
next_img=image.load("button.png")
next_img=transform.scale(next_img,(100,100))
next_img=transform.rotate(next_img,180)
left_img=transform.rotate(next_img,180)
up_img=transform.rotate(next_img,90)
down_img=transform.rotate(next_img,270)

door_img=image.load("door.png")
door_img=transform.scale(door_img,(100,100))


data_file=open("data.txt","r")
read_data=data_file.readlines()
data_file.close()

level=int(read_data[0])
lvl_lis=(read_data[level]).split(":")

goals=list(lvl_lis[0].split(","))
leaves=list(lvl_lis[1].split(","))
blocks=list(lvl_lis[2].split(","))
player=list(lvl_lis[3].split("\n"))


count=1
pos=(0,0)
for i in range(0,width,sqr_a):
    for j in range(0,width,sqr_a):
        if str(count) in goals:
            goals[goals.index(str(count))]=(i,j)
        if str(count) in leaves:
            leaves[leaves.index(str(count))]=(i,j)
        if str(count) in blocks:
            blocks[blocks.index(str(count))]=(i,j)
        if str(count) in player:
            player[player.index(str(count))]=(i,j)
        count+=1

def restart():
    global goals,leaves,blocks,player
    data_file=open("data.txt","r")
    read_data=data_file.readlines()
    data_file.close()

    lvl_lis=(read_data[level]).split(":")

    goals=list(lvl_lis[0].split(","))
    leaves=list(lvl_lis[1].split(","))
    blocks=list(lvl_lis[2].split(","))
    player=list(lvl_lis[3].split("\n"))

    count=1
    for i in range(0,width,sqr_a):
        for j in range(0,width,sqr_a):
            if str(count) in goals:
                goals[goals.index(str(count))]=(i,j)
            if str(count) in leaves:
                leaves[leaves.index(str(count))]=(i,j)
            if str(count) in blocks:
                blocks[blocks.index(str(count))]=(i,j)
            if str(count) in player:
                player[player.index(str(count))]=(i,j)
            count+=1


def end_game():
    global level
    win.blit(door_img,((width/2)-50,(height/2)-100))
    win.blit(next_img,((width/2)-50,(height/2)+50))
    if ((width/2)-50<pos[0]<(width/2)-50+100) and ((height/2)-100<pos[1]<(height/2)):
        quit()
    if ((width/2)-50<pos[0]<(width/2)-50+100)  and ((height/2)+50<pos[1]<(height/2)+150):
        level+=1
        data_file=open("data.txt","w")
        read_data[0]=str(level)+"\n"
        data_file.writelines(read_data)
        data_file.close()
        restart()
    
def player_move(place,side):
    global player,leaves
    if place in leaves:
        leaf=leaves[leaves.index(place)]
        if side=='r':
            leaf=(leaf[0],leaf[1]+sqr_a)
            if leaf not in blocks and leaf[1]<width and leaf not in leaves:
                leaves[leaves.index(place)]=leaf
                player[0]=place
        if side=='l':
            leaf=(leaf[0],leaf[1]-sqr_a)
            if leaf not in blocks and leaf[1]>=0 and leaf not in leaves:
                leaves[leaves.index(place)]=leaf
                player[0]=place
        if side=='u':
            leaf=(leaf[0]-sqr_a,leaf[1])
            if leaf not in blocks and leaf[0]>=0 and leaf not in leaves:
                leaves[leaves.index(place)]=leaf
                player[0]=place
        if side=='d':
            leaf=(leaf[0]+sqr_a,leaf[1])
            if leaf not in blocks and leaf[0]<height and leaf not in leaves:
                leaves[leaves.index(place)]=leaf
                player[0]=place  
    else:
        player[0]=place
        
def game():
    global player,leaf,pos
    while 1:
        win.fill("green")
        draw.rect(win,("black"),(0,0,width,height),1)
        win.blit(left_img,((width/2)-250,(scr_height-125)))
        win.blit(down_img,((width/2)-150,(scr_height-125)))
        win.blit(up_img,((width/2)+50,(scr_height-125)))
        win.blit(next_img,((width/2)+150,(scr_height-125)))
        win.blit(reload_img,((width/2)-25,(scr_height-150)))
        
        for i in range(0,width+1,sqr_a):
            for j in range(0,width+1,sqr_a):
                if (i,j) in goals:
                    win.blit(home_img,(j,i))
                if (i,j) in player:
                    win.blit(snail_img,(j,i))
                if (i,j) in blocks:
                    win.blit(wall_img,(j,i))
                if (i,j) in leaves:
                    win.blit(leaf_img,(j,i))    
        for eve in event.get():
            if eve.type==QUIT:
                quit()
            if eve.type==KEYDOWN:
                if eve.key==K_RIGHT:
                    update=player[0][1]+sqr_a
                    if update<width and (player[0][0],update) not in blocks:
                        player_move((player[0][0],update),'r')
                if eve.key==K_LEFT:
                    update=player[0][1]-sqr_a
                    if update>=0 and (player[0][0],update) not in blocks:
                        player_move((player[0][0],update),'l')
                if eve.key==K_UP:
                    update=player[0][0]-sqr_a
                    if update>=0 and (update,player[0][1]) not in blocks:
                        player_move((update,player[0][1]),'u')
                if eve.key==K_DOWN:
                    update=player[0][0]+sqr_a
                    if update<height and (update,player[0][1]) not in blocks:
                        player_move((update,player[0][1]),'d')
                if eve.key==K_SPACE:
                    restart()
            if eve.type==MOUSEBUTTONDOWN:
                if eve.button==1:
                    pos=mouse.get_pos()
                    if ((width/2)-250<pos[0]<(width/2)-250+100) and ((scr_height-125)<pos[1]<(scr_height-125)+100):##left
                        update=player[0][1]-sqr_a
                        if update>=0 and (player[0][0],update) not in blocks:
                            player_move((player[0][0],update),'l')
                    if ((width/2)-150<pos[0]<(width/2)-150+100) and ((scr_height-125)<pos[1]<(scr_height-125)+100):#right
                        update=player[0][0]+sqr_a
                        if update<height and (update,player[0][1]) not in blocks:
                            player_move((update,player[0][1]),'d')                        
                    if ((width/2)+50<pos[0]<(width/2)+50+100) and ((scr_height-125)<pos[1]<(scr_height-125)+100):#up
                        update=player[0][0]-sqr_a
                        if update>=0 and (update,player[0][1]) not in blocks:
                            player_move((update,player[0][1]),'u')
                    if ((width/2)+150<pos[0]<(width/2)+150+100) and ((scr_height-125)<pos[1]<(scr_height-125)+100):#down
                        update=player[0][1]+sqr_a
                        if update<width and (player[0][0],update) not in blocks:
                            player_move((player[0][0],update),'r')
                    if ((width/2)-25<pos[0]<(width/2)-25+64) and ((scr_height-150)<pos[1]<(scr_height-150)+64):
                        restart()
        
        leaves.sort()
        if leaves==goals:
            end_game()
        display.update()
game()
