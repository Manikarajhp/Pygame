from pygame import *
import random
init()
width=height=500
win=display.set_mode((width,height))


font=font.Font("freesansbold.ttf",32)
bw=100
boxes=[]
correct_boxes=[]
start=int((width/2)-((bw/2)+bw))
end=int((height/2)+((bw/2)+bw))
values=[i for i in range(1,10)]
empty_space=()
count=1
for i in range(start,end+1,bw+10):
    for j in range(start,end+1,bw+10):
        value=random.choice(values)
        boxes.append((i,j,value))
        if value==9:
            empty_space=(i,j,value)
        values.remove(value)
        correct_boxes.append((i,j,count))
        count+=1
print(correct_boxes,"\n",boxes)
def box_show():
    for i in boxes:
        if i[2]==9:
            pass
        else:
            draw.rect(win,("red"),(i[0],i[1],bw,bw))
            txt=font.render(str(i[2]),True,"white")
            win.blit(txt,(i[0]+int(bw/2),i[1]+int(bw/2)))
def box_move(pos):
    global empty_space,boxes
    for i in boxes:
        if (pos[0]>i[0] and pos[0]<i[0]+bw) and (pos[1]>i[1] and pos[1]<i[1]+bw):
            temp=i[2]
            boxes[boxes.index(i)]=(i[0],i[1],9)
            boxes[boxes.index(empty_space)]=(empty_space[0],empty_space[1],temp)
            empty_space=(i[0],i[1],9)
    print(boxes,"\n",correct_boxes,"\n\n")
    if boxes==correct_boxes:
        quit()
def game():
    while 1:
        win.fill("lightblue")
        for eve in event.get():
            if eve.type==QUIT:
                quit()
            if eve.type==MOUSEBUTTONDOWN:
                if eve.button==1:
                    pos=mouse.get_pos()
                    box_move(pos)
        box_show()
        display.update()
game()
