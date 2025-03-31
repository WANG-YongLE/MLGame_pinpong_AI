"""
The template of the script for the machine learning process in game pingpong
"""
from ml.prediction import Prediction
import pygame

prediction=Prediction()
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
        self.buffer=[]
        self.time_of_hit=0
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
            x=-1
            blocker_d=scene_info["blocker"][0]-self.blocker_before

            v=prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],0)
            x=v[0]
           # prediction.predict(scene_info["ball"],scene_info["ball_speed"],scene_info["blocker"][0],blocker_d,scene_info["frame"],665)

                
            
            
            if(x==-1) : command="NONE"
            elif(x<=scene_info["platform_1P"][0]+10) :
                command="MOVE_LEFT"
            elif(x>=scene_info["platform_1P"][0]+30):
                command="MOVE_RIGHT"
            # Red 紅色 下方
            print("frame_used:", scene_info["frame"], "prdiction:", v, "ball_speed:", scene_info["ball_speed"], "ball:",scene_info["ball"],"blocker:",scene_info["blocker"],scene_info["platform_1P"][0],command)


        elif self.side == "2P":
            # Blue 藍色 上方
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
        self.blocker_before=scene_info["blocker"][0]
        return command

    def reset(self):
        """
        Reset the status
        """
        print("reset " + self.side)
        self.ball_served = False
