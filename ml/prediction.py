class Prediction:

    def predict(self, ball, ball_speed, block, blocker_d, time):
        if time == 33:
            return ball

        if block == 0:
            blocker_d = 5
        elif block == 170:
            blocker_d = -5
        new_block=block + blocker_d

        ball_x, ball_y = ball
        ball_speed_x, ball_speed_y = ball_speed

        next_ball_x = ball_x + ball_speed_x
        next_ball_y = ball_y + ball_speed_y

        # 處理牆壁反彈
        if next_ball_x <= 0:
            next_ball_x = 0
            ball_speed_x = -ball_speed_x
        elif next_ball_x >= 195:
            next_ball_x = 195
            ball_speed_x = -ball_speed_x

        # 處理磚塊碰撞（使用軌跡判斷是否穿過）
        block_top, block_bottom = 240, 260
        block_left, block_right = new_block, new_block + 30
        
        a = ball_speed_y / ball_speed_x
        if(ball_speed[1]>0) :
            if(ball_speed[0]>0):
                b = (ball_y+5) - a * (ball_x+5)
                pos_str=self.find_intersection_str(a,b,block)
            if(ball_speed[0]<0):
                b = (ball_y+5) - a * (ball_x)
                pos_str=self.find_intersection_str(a,b,block+30)
            pos_row=self.find_intersection_row(a,b,240)     
        else :
            if(ball_speed[0]>0):
                b = (ball_y) - a * (ball_x+5)
                pos_str=self.find_intersection_str(a,b,block)
            if(ball_speed[0]<0):
                pos_str=self.find_intersection_str(a,b,block+30)
            pos_row=self.find_intersection_row(a,b,0,260)
        


        time+=1
        blocker+=blocker_d
        if(block==0) : blocker_d=5
        elif(block==170) :blocker_d=-5
        return self.predict((ball_x,ball_y),(ball_speed_x,ball_speed_y),block,blocker_d,time)  

    def find_intersection_str(a, b, block):
        x = block
        y = a * x + b
        return (x, y)
    def find_intersection_row(a, b, high):
        y = high
        x = (y - b) / a if a != 0 else None  # 避免除以零的情況
        return (x, y)