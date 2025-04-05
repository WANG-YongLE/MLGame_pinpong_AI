from ml.prediction import Prediction
import pygame
import os
import pickle
import time
import random
prediction = Prediction()

class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        """
        Constructor

        @param ai_name A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        
        self.ball_served = False
        self.side = ai_name
        self.blocker_before=-1
        self.down=[]
        self.mindow=[]
        self.slide=3
        self.data_buffer = []
    
        #1無
        #2正
        #3反

        self.init=0

        filename = "./ml/record/data3.pkl"  
        data = {}    
# 讀取原本的 pickle 檔案
        if self.side == "1P":
            data["place"] = list(range(0, 160, 5))
            data["key"] = 0
            if os.path.exists(filename):
                with open(filename, "rb") as f:
                    data = pickle.load(f)
            self.init = data["place"][data["key"]]
            data["key"] = (data["key"] + 1) % len(data["place"])
            with open(filename, "wb") as f:
                pickle.dump(data, f) 
            print(self.init)
        self.serve = random.choice([0, 1])
        self.mock_plat2=160
    def update(self, scene_info, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        t=-1
        if scene_info["status"] != "GAME_ALIVE":
            level=abs(scene_info["ball_speed"][1])
            self.pickle_file = f"data/bad_data/slide_{self.slide}/plat2_{self.mock_plat2}/level_{level}//game_data_{int(time.time())}.pkl"
            if level < 10:
                self.pickle_file = f"data/bad_data/slide_{self.slide}/plat2_{self.mock_plat2}/level_0{level}/game_data_{int(time.time())}.pkl"
            if not os.path.exists(os.path.dirname(self.pickle_file)):
                os.makedirs(os.path.dirname(self.pickle_file), exist_ok=True)
            with open(self.pickle_file, mode="ab") as file:
                pickle.dump(self.data_buffer, file)
            self.data_buffer=[]
            return "RESET"
        
        if(scene_info["frame"]%100==1) :
            level=abs(scene_info["ball_speed"][1])
            self.pickle_file = f"data/good_data/slide_{self.slide}/plat2_{self.mock_plat2}/level_{level}/game_data_{int(time.time())}.pkl"
            if level < 10:
                self.pickle_file = f"data/good_data/slide_{self.slide}/plat2_{self.mock_plat2}/level_0{level}/game_data_{int(time.time())}.pkl"
            if not os.path.exists(os.path.dirname(self.pickle_file)):
                os.makedirs(os.path.dirname(self.pickle_file), exist_ok=True)
            with open(self.pickle_file, mode="ab") as file:
                pickle.dump(self.data_buffer, file)
            self.data_buffer=[]
        
        command = "NONE"
        
        if self.side == "1P":
        #    print(self.init)

            if not self.ball_served:
                if(scene_info["platform_1P"][0]>self.init) :return "MOVE_LEFT"
                if(scene_info["platform_1P"][0]<self.init) :return "MOVE_RIGHT"
                self.ball_served = True
                if(self.serve==0):
                    return "SERVE_TO_RIGHT"
                else :return "SERVE_TO_LEFT"
            
            pballx = -10000
            blocker_d = scene_info["blocker"][0] - self.blocker_before
            
            if(scene_info["ball_speed"][0]*scene_info["ball_speed"][1]) :
                down=prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],0,"DOWN",self.slide)
                self.down=down
                mindow=prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],0,"MINDOW",self.slide)
                self.mindow=mindow
                pballx=self.down[0][0]
                future = [None] * 3 
                future[0]=prediction.predict(self.mindow[0],(self.mindow[1][1],self.mindow[1][1]),self.mindow[2],self.mindow[3],self.mindow[4],0,"UP",self.slide) #無
                future[1]=prediction.predict(self.mindow[0],(abs(self.mindow[1][1])+3,self.mindow[1][1]),self.mindow[2],self.mindow[3],self.mindow[4],0,"UP",self.slide)#正
                future[2]=prediction.predict(self.mindow[0],(-self.mindow[1][1],self.mindow[1][1]),self.mindow[2],self.mindow[3],self.mindow[4],0,"UP",self.slide) #反
            # prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],665)
                speed_x=scene_info["ball_speed"][0]
                y_80=[]
                y_415=[]
                t=-1
                d=-1
                if(scene_info["ball"][1]>=415-1*abs(scene_info["ball_speed"][1] )) and (scene_info["ball"][1]!=415):
                    speed_x=self.mindow[1][0]
                    if(self.mindow[0][0]==0 or self.mindow[0][0]==195) : speed_x*=-1 
                    if(speed_x>0) :
                        if(scene_info["platform_1P"][0]+45>200) :
                            future[1]=None
                        elif scene_info["platform_1P"][0]<5 :
                            future[2]=None
                    elif(speed_x<0) :
                        if(scene_info["platform_1P"][0]+45>200) :
                            future[2]=None
                        elif scene_info["platform_1P"][0]<5 :
                            future[1]=None
                    if(not (scene_info["platform_1P"][0]<=pballx and scene_info["platform_1P"][0]+40>=pballx)):
                        future[0]=None
                    

                    for i in range(3):
                        if(future[i]==None) : continue
                        if future[i][0][1]==80 :
                            y_80.append(i)
                        if future[i][0][1]==415:
                            y_415.append(i)
                    for i in y_80:
                        if d < abs(self.mock_plat2+20-future[i][0][0]) :
                            t=i
                            d= abs(self.mock_plat2+20-future[i][0][0])
                            #############
                    d=300
                    if(t!=-1) :
                        for i in y_415:
                            ti=future[i][4]-self.mindow[4]
                            if(abs(self.mindow[0][0]-future[i][0][0])/5<=ti) :
                                if(d>abs(self.mindow[0][0]-future[i][0][0])) :
                                    t=i
                                    d=abs(self.mindow[0][0]-future[i][0][0])
                    
                                                
                        

                        
                if(scene_info["ball_speed"][1]<0 ) :
                    up=prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],0,"UP",1)
                    
                    if(up[0][1]==80): 
                        no_slide=prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],0,"DOWN",1)
                        pos_slide=prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],0,"DOWN",2)
                        neg_slide=prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],0,"DOWN",3)
                        correct=[]
                        if(abs(neg_slide[0][0]-scene_info["platform_1P"][0])/5<=neg_slide[4]-scene_info["frame"] or abs(neg_slide[0][0]-scene_info["platform_1P"][0]+40)/5<=neg_slide[4]-scene_info["frame"]) :correct.append(neg_slide[0][0])
                        else :correct.append(-3000)
                        if(abs(pos_slide[0][0]-scene_info["platform_1P"][0])/5<=pos_slide[4]-scene_info["frame"] or abs(pos_slide[0][0]-scene_info["platform_1P"][0]+40)/5<=pos_slide[4]-scene_info["frame"]) :correct.append(pos_slide[0][0])
                        else :correct.append(3000)
                        if(abs(no_slide[0][0]-scene_info["platform_1P"][0])/5<=no_slide[4]-scene_info["frame"] or abs(no_slide[0][0]-scene_info["platform_1P"][0]+40)/5<=no_slide[4]-scene_info["frame"]) :correct.append(no_slide[0][0])
                        else :correct.append(-15000)
                        correct.sort()
                        middle=(correct[0]+correct[2])/2
                        if(abs(middle-correct[0])/5<=neg_slide[4]-up[4] and 
                        abs(middle-correct[2])/5<=neg_slide[4]-up[4]):
                            pballx=middle
                        elif(abs(correct[1]-correct[0])<=abs(correct[2]-correct[1])):
                            middle=(correct[0]+correct[1])/2
                            if(abs(middle-correct[0])/5<=neg_slide[4]-up[4] and 
                            abs(middle-correct[1])/5<=neg_slide[4]-up[4]):
                                pballx=middle
                        else:
                            middle=(correct[1]+correct[2])/2
                            if(abs(middle-correct[2])/5<=neg_slide[4]-up[4] and 
                            abs(middle-correct[1])/5<=neg_slide[4]-up[4]):
                                pballx=middle                       
            #    print("pballx:",pballx)
            if(pballx==-10000) : command="NONE"
            elif(pballx<scene_info["platform_1P"][0]+11) :
                command="MOVE_LEFT"
            elif(pballx>scene_info["platform_1P"][0]+29):
                command="MOVE_RIGHT"
            if(t!=-1) :

                if(t==0) : command="NONE"
                elif(t==1) :
                    if(speed_x>0) : command="MOVE_RIGHT"
                    else :command="MOVE_LEFT"
                elif(t==2) :
                    if(speed_x>0) : command="MOVE_LEFT"
                    else :command="MOVE_RIGHT"

            # Red 紅色 下方
            
                
            print("frame_used:", scene_info["frame"], "prdiction:", self.down, "ball_speed:", scene_info["ball_speed"], "ball:",scene_info["ball"],"blocker:",scene_info["blocker"],scene_info["platform_1P"][0],command)
            self.save_data(scene_info, command)

        elif self.side == "2P":


        #    print(scene_info["ball"][0])
            if not self.ball_served:
                self.serve = random.choice([0, 1])
                if(self.serve):command = "SERVE_TO_LEFT"
                else :command = "SERVE_TO_RIGHT"
                self.ball_served = True

            elif pygame.K_a in keyboard:
                command = "MOVE_LEFT"
            elif pygame.K_d in keyboard:
                command = "MOVE_RIGHT"
            blocker_d = scene_info["blocker"][0] - self.blocker_before
            if(scene_info["ball_speed"][0]*scene_info["ball_speed"][1]):
                future3=prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],0,"UP",self.slide)

                if(self.slide==1):
                    if(scene_info["ball"][1]<=80-scene_info["ball_speed"][1]) :command="NONE"
                    elif future3 is None:
                        ...
                    elif(future3[0][0]<100) :command = "MOVE_LEFT"
                    else :command = "MOVE_RIGHT"
                elif self.slide==2:
            
                    if(scene_info["ball"][1]<=80-scene_info["ball_speed"][1]) :
                        if(scene_info["ball_speed"][0]<0) : command = "MOVE_LEFT"
                        else :command = "MOVE_RIGHT"      
                    elif(scene_info["ball_speed"][0]<0) : command = "MOVE_RIGHT"
                    else :command = "MOVE_LEFT"               
                elif self.slide==3:
                    if(scene_info["ball"][1]<=80-scene_info["ball_speed"][1]) :
                        if(scene_info["ball_speed"][0]<0) : command = "MOVE_RIGHT"
                        else :command = "MOVE_LEFT"  
                    elif(scene_info["ball_speed"][0]<0) : command = "MOVE_LEFT" 
                    else :command =  "MOVE_RIGHT"  
         
        if(self.blocker_before!=scene_info["blocker"][0]):self.blocker_before = scene_info["blocker"][0]
        return command
        

    def reset(self):
        """
        Reset the status
        """
        print("reset " + self.side)
        self.ball_served = False
    def save_data(self, scene_info, command, *args, **kwargs):
        """
        儲存數據到 CSV 檔案
        """
        ball_speed_x = scene_info["ball_speed"][0]
        ball_speed_y = scene_info["ball_speed"][1]
        move = 0
        ball_x = scene_info["ball"][0]
        ball_y = scene_info["ball"][1]
        platform1_x = scene_info["platform_1P"][0]+20
        platform2_x=1000
        #3表示無視
        #-1表示靠左
        #0 表示靠中
        #1表示靠右
        if(scene_info["ball"][1]>=415-1*abs(scene_info["ball_speed"][1] )) and (scene_info["ball"][1]!=415):
            if(self.mock_plat2+20<=66): platform2_x=-1
            elif(self.mock_plat2+20>66 and (self.mock_plat2+20<=133)):platform2_x=0
            else : platform2_x=1
        
        if command == "MOVE_LEFT":
            move = -1
        elif command == "MOVE_RIGHT":
            move = 1
        elif command == "NONE":
            move = 0
        
        blocker_d = scene_info["blocker"][0] - self.blocker_before
        data_row = [

            ball_speed_x,       # 球的 x 方向速度
            ball_speed_y,       # 球的 y 方向速度
            ball_x,             # 球的當前 x 座標
            ball_y,             # 球的當前 y 座標
            platform1_x,
            platform2_x,
            scene_info["blocker"][0], 
            blocker_d,      # 平台的 x 座標
            move,               # 平台移動方向
            
        ]

        self.data_buffer.append(data_row)