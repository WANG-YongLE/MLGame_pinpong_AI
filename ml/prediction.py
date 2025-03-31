from pygame import Rect
from mlgame.game import physics
class Prediction:
    def predict(self, ball, ball_speed, block, blocker_d, frame, time,string,slide):
        if (time != 0 and frame % 100 == 0):
            ball_speed = (ball_speed[0] + (1 if ball_speed[0] > 0 else -1),
                          ball_speed[1] + (1 if ball_speed[1] > 0 else -1))
        if(time>=666) :return (ball,ball_speed,block,blocker_d,frame)
        if((string=="DOWN" or string=="MINDOW" )and ball[1]==415) :
            return (ball,ball_speed,block,blocker_d,frame)
        if(string =="UP" and time >=4 and ball[1]==415) :
            return (ball,ball_speed,block,blocker_d,frame)
        if(string =="UP" and time >=4 and ball[1]==80) :
            return (ball,ball_speed,block,blocker_d,frame)       
        if block == 0:
            blocker_d = 5
        elif block == 170:
            blocker_d = -5
        new_block = block + blocker_d
        ball_x, ball_y = ball
        ball_speed_x, ball_speed_y = ball_speed
        if(ball_speed_x==0): return None
        next_ball_x = ball_x + ball_speed_x
        next_ball_y = ball_y + ball_speed_y
        # 處理牆壁反彈
        if next_ball_y >= 415:
            next_ball_y = 415
            if(string=="DOWN") :
                a=0
                if(ball_speed_x==0) : return None
                else : a= ball_speed_y / ball_speed_x
                b = ball_y - a * ball_x
                next_ball_x,next_ball_y=self.find_intersection_row(a,b,415)

            ball_speed_y = -ball_speed_y
                
                
            
        elif next_ball_y <= 80:
            next_ball_y = 80
            origin_ball_speed=abs(ball_speed_y)
            if(slide==2) :
                origin_ball_speed+=3
            elif(slide==3) :
                origin_ball_speed*=-1
            ball_speed_x=origin_ball_speed if ball_speed[0] > 0 else -origin_ball_speed
            ball_speed_y = -ball_speed_y
            


        if next_ball_x <= 0:
            next_ball_x = 0
            ball_speed_x = -ball_speed_x
        elif next_ball_x >= 195:
            next_ball_x = 195
            ball_speed_x = -ball_speed_x


        ball_rect = Rect(ball_x, ball_y, 5, 5)
        ball_speed=[ball_speed_x,ball_speed_y]
        # 定義障礙物（擋板）
        blocker_rect = Rect(block, 240, 30, 20)
        blocker_speed = [blocker_d, 0]  

        # 計算下一個位置
        next_ball_rect = ball_rect.move(ball_speed)
        next_blocker_rect = blocker_rect.move(blocker_speed)

        # 創建模擬的 "Sprite" 類來符合 `moving_collide_or_contact` 需求
        class MockSprite:
            def __init__(self, rect, last_pos):
                self.rect = rect
                self.last_pos = last_pos

        # 設定球與擋板的當前與上一幀位置
        ball_sprite = MockSprite(next_ball_rect, ball_rect)
        blocker_sprite = MockSprite(next_blocker_rect, blocker_rect)

        # 測試碰撞
        is_collision = physics.moving_collide_or_contact(ball_sprite, blocker_sprite)           
        if is_collision :
            next_ball_rect,next_speed=physics.bounce_off(
                next_ball_rect,ball_speed,
                next_blocker_rect,blocker_speed)
      #      print((next_ball_rect.x,next_ball_rect.y),next_speed,new_block,frame+1,"S")
            return self.predict((next_ball_rect.x,next_ball_rect.y),next_speed,new_block,blocker_d,frame+1,time+1,string,slide)
        
        return self.predict((next_ball_x,next_ball_y),(ball_speed_x,ball_speed_y),new_block,blocker_d,frame+1,time+1,string,slide)  

    def find_intersection_str(self, a, b, block):
        x = block
        y = a * x + b
        return (x, y)

    def find_intersection_row(self, a, b, high):
        y = high
        x = (y - b) / a if a != 0 else None  # 避免除以零的情況
        return (x, y)