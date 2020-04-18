import math

def cost_generator(cnr,Draw_deck,Draw_trash,dis1,dis2,R,L,F,Clearing,Enough_card):
    maxx = 3
    midd = 2
    minn = 1
    if(cnr>0.5):
        cost = (dis2*(minn+(R*3+F*2+L)))+(dis1*(midd+(Clearing*3+R*2+F)))+(Draw_trash*(maxx + max(L*3+F*2+R,10*Enough_card)))
    else:
        cost = (dis2*(maxx+(R*3+F*2+L)))+(dis1*(midd+(Clearing*3+R*2+F)))+(Draw_trash*(minn + max(L*3+F*2+R,10*Enough_card)))

    print(cost)

cost_generator(0.6,0,1,0,0,1,0,0,0,0)