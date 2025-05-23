"""
The template of the script for the machine learning process in game pingpong
"""
import pygame


class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        """
        Constructor

        @param ai_name A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = ai_name

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
                return "SERVE_TO_RIGHT"           # Red 紅色 下方
            if pygame.K_UP in keyboard:
                command = "SERVE_TO_LEFT"
                self.ball_served = True
            elif pygame.K_DOWN in keyboard:
                command = "SERVE_TO_RIGHT"
                self.ball_served = True
            elif pygame.K_LEFT in keyboard:
                command = "MOVE_LEFT"
            elif pygame.K_RIGHT in keyboard:
                command = "MOVE_RIGHT"
            if(scene_info["ball"][1]>=415-1*abs(scene_info["ball_speed"][1] )) and (scene_info["ball"][1]!=415) :command="MOVE_RIGHT"

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
            if(scene_info["ball"][1]<=80+1*abs(scene_info["ball_speed"][1] )) and (scene_info["ball"][1]!=80) :command="MOVE_RIGHT"
        
        print("side:",self.side,"frame_used:", scene_info["frame"],"ball_speed:", scene_info["ball_speed"], "ball:",scene_info["ball"],"blocker:",scene_info["blocker"],"MOVE:",command)
        return command

    def reset(self):
        """
        Reset the status
        """
        print("reset " + self.side)
        self.ball_served = False
