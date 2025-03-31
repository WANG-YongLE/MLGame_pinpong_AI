from ml.prediction import Prediction
import pygame

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
        self.slide=1
        #1無
        #2正
        #3反
    def update(self, scene_info, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"
        
        command = "NONE"
        
        if self.side == "1P":
            if not self.ball_served:
                self.ball_served = True
                return "SERVE_TO_RIGHT"
            
            pballx = -1
            blocker_d = scene_info["blocker"][0] - self.blocker_before
            if( self.down and self.down[4]<=scene_info["frame"]+10) : self.down=[]

            down=prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],0,"DOWN",self.slide)
            self.down=down
            mindow=prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],0,"MINDOW",self.slide)
            self.mindow=mindow
            pballx=self.down[0][0]
            future1=prediction.predict(self.mindow[0],(self.mindow[1][1],self.mindow[1][1]),self.mindow[2],self.mindow[3],self.mindow[4],0,"UP",self.slide)
            future2=prediction.predict(self.mindow[0],(self.mindow[1][1]+3,self.mindow[1][1]),self.mindow[2],self.mindow[3],self.mindow[4],0,"UP",self.slide)
            future3=prediction.predict(self.mindow[0],(-self.mindow[1][1],self.mindow[1][1]),self.mindow[2],self.mindow[3],self.mindow[4],0,"UP",self.slide)
           # prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],665)
            
                
            
            
            if(pballx==-1) : command="NONE"
            elif(pballx<scene_info["platform_1P"][0]+12) :
                command="MOVE_LEFT"
            elif(pballx>scene_info["platform_1P"][0]+28):
                command="MOVE_RIGHT"

            # Red 紅色 下方
            print("frame_used:", scene_info["frame"], "prdiction:", self.down, "ball_speed:", scene_info["ball_speed"], "ball:",scene_info["ball"],"blocker:",scene_info["blocker"],scene_info["platform_1P"][0],command)


        elif self.side == "2P":


                #future3=prediction.predict(mindow[0],(-mindow[1][1],mindow[1][1]),mindow[2],mindow[3],mindow[4],0,"UP",self.slide)
            if pygame.K_q in keyboard:
                command = "SERVE_TO_LEFT"
                self.ball_served = True
            elif pygame.K_e in keyboard:
                command = "SERVE_TO_RIGHT"
                self.ball_served = True
            elif pygame.K_a in keyboard:
                command = "MOVE_LEFT"
            elif pygame.K_d in keyboard:
                command = "MOVE_RIGHT"
        
        self.blocker_before = scene_info["blocker"][0]
        return command

    def reset(self):
        """
        Reset the status
        """
        print("reset " + self.side)
        self.ball_served = False