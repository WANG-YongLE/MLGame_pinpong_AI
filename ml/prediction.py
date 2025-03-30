class Prediction:

    def predict(self, ball, ball_speed, block, blocker_d, frame, time):
        if (time != 0 and frame % 100 == 0):
            ball_speed = (ball_speed[0] + (1 if ball_speed[0] > 0 else -1),
                          ball_speed[1] + (1 if ball_speed[1] > 0 else -1))
        if(time>=666) :return ball
        if block == 0:
            blocker_d = 5
        elif block == 170:
            blocker_d = -5
        new_block = block + blocker_d

        ball_x, ball_y = ball
        ball_speed_x, ball_speed_y = ball_speed

        next_ball_x = ball_x + ball_speed_x
        next_ball_y = ball_y + ball_speed_y

        # 處理牆壁反彈


        if next_ball_y >= 415:
            next_ball_y = 415
            ball_speed_y = -ball_speed_y
            return (next_ball_x,next_ball_y)
        elif next_ball_y <= 80:
            next_ball_y = 80
            if(abs(ball_speed_x)!=abs(ball_speed_y)) :
                if(ball_speed_x<0) :ball_speed_x+=3
                else : ball_speed_x-=3
            ball_speed_y = -ball_speed_y


        if next_ball_x <= 0:
            next_ball_x = 0
            ball_speed_x = -ball_speed_x
        elif next_ball_x >= 195:
            next_ball_x = 195
            ball_speed_x = -ball_speed_x

        if (((next_ball_y-235)*(ball_y-235)<=0 or (next_ball_y-265)*(ball_y-265)<=0) and ((next_ball_x-new_block+5)*(ball_x-new_block+5)<=0 or(next_ball_x-new_block-35)*(ball_x-new_block-35<=0))) :
            print((ball_x,ball_y),ball_speed_x,ball_speed_y,block,"K",frame)
            a = ball_speed_y / ball_speed_x
            pos_str=(-2,-1)
            pos_row=(-1,-2)
            if(ball_speed[1]>0) :
                if(ball_speed[0]>0):
                    b = (ball_y+5) - a * (ball_x+5)
                    pos_str=self.find_intersection_str(a,b,new_block)
                    if(pos_str[1]>=240 and pos_str[1]<=260+5) :
                        next_ball_x=new_block-5
                        ball_speed_x=-ball_speed_x 
                    pos_row=self.find_intersection_row(a,b,240)
                    if(pos_row[0]>=new_block and pos_row[0]<=new_block+35) :
                        next_ball_y=240-5
                        ball_speed_y=-ball_speed_y

                if(ball_speed[0]<0):
                    b = (ball_y+5) - a * (ball_x)
                    pos_str=self.find_intersection_str(a,b,new_block+30)
                    if(pos_str[1]>=240 and pos_str[1]<=260+5) :
                        next_ball_x=new_block-5
                        ball_speed_x=-ball_speed_x 
                    pos_row=self.find_intersection_row(a,b,240)
                    if(pos_row[0]>=new_block-5 and pos_row[0]<=new_block+30) :
                        next_ball_y=240-5
                        ball_speed_y=-ball_speed_y                    
            else :
                if(ball_speed[0]>0):
                    b = (ball_y) - a * (ball_x+5)
                    pos_str=self.find_intersection_str(a,b,new_block)
                    if(pos_str[1]>=240-5 and pos_str[1]<=260) :
                        next_ball_x=new_block-5
                        ball_speed_x=-ball_speed_x 
                    pos_row=self.find_intersection_row(a,b,260)
                    if(pos_row[0]>=new_block and pos_row[0]<=new_block+35) :
                        next_ball_y=240-5
                        ball_speed_y=-ball_speed_y   
                if(ball_speed[0]<0):
                    b=(ball_y)-a*ball_x
                    pos_str=self.find_intersection_str(a,b,new_block+30)
                    if(pos_str[1]>=240-5 and pos_str[1]<=260) :
                        next_ball_x=new_block-5
                        ball_speed_x=-ball_speed_x 
                    pos_row=self.find_intersection_row(a,b,260)
                    if(pos_row[0]>=new_block-5 and pos_row[0]<=new_block+30) :
                        next_ball_y=240-5
                        ball_speed_y=-ball_speed_y   




            if(pos_row[0]>=new_block and pos_row[0]<=new_block+30) :
                if(ball_speed_y>0) : 
                    next_ball_y=240-5
                else : 
                    next_ball_y=260
                ball_speed_y=-ball_speed_y
            
            if(pos_str[1]>=240 and pos_str[1]<=260) :
                if(ball_speed_x>0) :
                    next_ball_x=new_block-5
                else : 
                    next_ball_x=new_block+30
                ball_speed_x=-ball_speed_x
            print((next_ball_x,next_ball_y),pos_str,pos_row,ball_speed_x,ball_speed_y,new_block,"S",frame+1)

        
        return self.predict((next_ball_x,next_ball_y),(ball_speed_x,ball_speed_y),new_block,blocker_d,frame+1,time+1)  

    def find_intersection_str(self, a, b, block):
        x = block
        y = a * x + b
        return (x, y)

    def find_intersection_row(self, a, b, high):
        y = high
        x = (y - b) / a if a != 0 else None  # 避免除以零的情況
        return (x, y)