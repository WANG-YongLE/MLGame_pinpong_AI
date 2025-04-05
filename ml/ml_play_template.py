"""
The template of the script for the machine learning process in game pingpong
"""
import os
import joblib
import numpy as np
class MLPlay:
    def __init__(self,  ai_name,*args,**kwargs):
        """
        Constructor

        @param ai_name A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = ai_name
        print(kwargs)
        model_path = os.path.join(os.path.dirname(__file__), "../knn_model.pkl")

        # 確保模型存在
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件 {model_path} 不存在！請先訓練模型。")     
        # 加載 KNN 模型
        self.knn = joblib.load(model_path)
        self.blocker_before=-1


    def update(self, scene_info, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_RIGHT"
        else:
            platform2_x=1000
            if(scene_info["ball"][1]>=415-1*abs(scene_info["ball_speed"][1] )) and (scene_info["ball"][1]!=415):
                if(scene_info["platform_2P"][0]+20<=66): platform2_x=-1
                elif(scene_info["platform_2P"][0]+20>66 and (scene_info["platform_2P"][0]+20<=133)):platform2_x=0
                else : platform2_x=1
            blocker_d = scene_info["blocker"][0] - self.blocker_before
            feature = np.array([
                scene_info["ball_speed"][0],
                scene_info["ball_speed"][1],
                scene_info["ball"][0],
                scene_info["ball"][1],# 球的位置
                scene_info["platform_1P"][0]+20,
                platform2_x,
                scene_info["blocker"][0], 
                blocker_d,      # 平台的 x 座標                        # 平台的位置
            ]).reshape(1, -1)
            a=self.knn.predict(feature)
            action = a[0]
            #print(a)
            # 轉換成遊戲指令
            self.blocker_before=scene_info["blocker"][0]
            if action == -1:
                return "MOVE_LEFT"
            elif action == 1:
                return "MOVE_RIGHT"
            else:
                return "NONE"



    def reset(self):
        """
        Reset the status
        """
        print("reset "+self.side)
        self.ball_served = False

