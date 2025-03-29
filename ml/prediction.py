class Prediction:

    def dicision_position_up_or_down(self, scene_info, ball, ball_speed):
        if ball_speed[1] > 0:
            return self.caculate_position_be_flip(scene_info, 420, ball)
        elif ball_speed[1] < 0:
            return self.caculate_position_be_flip(scene_info, 80, ball)
        else:
            return -1

    def dicision_position_blocker(self, scene_info, ball, ball_speed):
        if ball_speed[1] < 0 and ball[1] > 260:
            return self.caculate_position_be_flip(scene_info, 260, ball)
        elif ball_speed[1] > 0 and ball[1] < 240:
            return self.caculate_position_be_flip(scene_info, 240, ball)
        else:
            return self.caculate_position_be_flip(scene_info, 250, ball)

    def whether_hit_block(self, scene_info, speed, position, ball, ball_speed):
        if position == -1:
            return 0
        if ball[1] < 240 and ball_speed[1] > 0:
            if ball_speed[1] == 0:
                return -1
            time = (240 - ball[1]) / ball_speed[1]
            sit = scene_info["blocker"][0] + speed * time
            place = self.flip(sit)
            if place <= position and place + 30 >= position:
                return 1
            elif ball[1] < 250 and ball_speed[1] > 0:
                time = (250 - ball[1]) / ball_speed[1]
                sit = scene_info["blocker"][0] + speed * time
                place = self.flip(sit)
                if place <= position and place + 30 >= position:
                    return 2
            else:
                return 0

    def caculate_position_be_flip(self, scene_info, high, ball):
        x = self.caculate_position(scene_info, high, ball)
        return self.flip(x)

    def flip(self, x):  # 添加self参数
        x = abs(x)
        times = int(x // 200)
        if times == 0:
            return x
        elif times % 2:
            return 200 - abs(x - 200 * times)
        else:
            return abs(x - 200 * times)

    def caculate_position(self, scene_info, high, ball):
        if scene_info["ball_speed"][1] == 0:  # 防止除以零
            return 0
        slope = scene_info["ball_speed"][0] / scene_info["ball_speed"][1]
        return ball[0] + (abs(high - ball[1])) / slope