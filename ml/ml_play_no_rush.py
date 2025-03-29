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
            x=prediction.dicision_position_up_or_down(scene_info,ball=scene_info["ball"],ball_speed=scene_info["ball_speed"])
            position=prediction.dicision_position_blocker(scene_info,ball=scene_info["ball"],ball_speed=scene_info["ball_speed"])
            speed=scene_info["platform_1P"][0]-self.blocker_before
            whether_hit=prediction.whether_hit_block(scene_info,speed,position,ball=scene_info["ball"],ball_speed=scene_info["ball_speed"])
            if(whether_hit==2) :
                x=prediction.dicision_position_blocker(scene_info,(position,250),(-scene_info["ball_speed"][0],scene_info["ball_speed"][1]))
            elif(whether_hit==1) :
                if(abs(scene_info["ball"][1]-scene_info["platform_1P"][1])<=abs(2*scene_info["ball_speed"][1])) : 
                    if(scene_info["ball_speed"][0]>0): return "MOVE_RIGHT"
                    else: return "MOVE_LEFT"
                
            
            print("frame_used:", scene_info["frame"], "prdiction:", x, "ball_speed:", scene_info["ball_speed"], "ball:",scene_info["ball"],"blocker:",scene_info["blocker"])
            if(x==-1) : command="NONE"
            elif(x<scene_info["platform_1P"][0]+18.5) :
                command="MOVE_LEFT"
            elif(x>scene_info["platform_1P"][0]+22.5):
                command="MOVE_RIGHT"
            # Red 紅色 下方
            


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
