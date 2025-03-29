class Prediction:

    def dicision_position_up_or_down(self,scene_info):
        if scene_info["ball_speed"][1]<0 and scene_info["ball"][1]>260:
            return self.caculate_position_be_flip(scene_info,260)
        elif scene_info["ball_speed"][1]>0 and scene_info["ball"][1]>260:
            return self.caculate_position_be_flip(scene_info,420)   
        elif scene_info["ball_speed"][1]<0 and scene_info["ball"][1]<240:
            return self.caculate_position_be_flip(scene_info,80) 
        elif scene_info["ball_speed"][1]>0 and scene_info["ball"][1]<240:
            return self.caculate_position_be_flip(scene_info,240)  
        else :return -1  
    def caculate_position_be_flip(self, scene_info,high):
        x = self.caculate_position(scene_info,high)
        x = abs(x)
        times = int(x // 200)
        if times == 0:
            return x
        elif times % 2:
            return 200 - abs(x - 200 * times)
        else:
            return abs(x - 200 * times)
    def caculate_position(self, scene_info,high):
        if scene_info["ball"][0] == 0:  # 防止除以零
            return 0
        slope = scene_info["ball_speed"][0] / scene_info["ball_speed"][1]
        return scene_info['ball'][0] + (abs(high - scene_info['ball'][1])) / slope