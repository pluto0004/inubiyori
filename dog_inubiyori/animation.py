import pygame
import os

class Animation:
    def __init__(self, dog_type, growth_stage):
        self.dog_type = dog_type
        self.growth_stage = growth_stage
        self.animations = {}
        self.current_animation = "idle"
        self.frame_index = 0
        self.last_update_time = 0
        self.animation_speed = 200  # ミリ秒単位
        
        # アニメーションの初期化
        self.load_animations()
    
    def load_animations(self):
        """犬種と成長段階に応じたアニメーションをロード"""
        # 各犬種のアニメーションを作成（プレースホルダー）
        self.create_placeholder_animations()
    
    def create_placeholder_animations(self):
        """プレースホルダーアニメーションを作成"""
        # 犬種ごとの色
        colors = {
            "コーギー": (255, 200, 100),
            "ミニチュアダックスフンド": (150, 100, 50),
            "柴犬": (255, 150, 50)
        }
        
        # 成長段階ごとのサイズ
        sizes = {
            "子犬": (100, 80),
            "成犬": (150, 120),
            "老犬": (140, 110)
        }
        
        color = colors[self.dog_type]
        size = sizes[self.growth_stage]
        
        # アイドルアニメーション（瞬き）
        idle_frames = []
        for i in range(4):
            frame = pygame.Surface(size, pygame.SRCALPHA)
            
            # 体
            pygame.draw.ellipse(frame, color, (0, size[1]//3, size[0], size[1]*2//3))
            
            # 頭
            head_size = size[0] // 2
            pygame.draw.circle(frame, color, (size[0] // 4 * 3, size[1] // 3), head_size // 2)
            
            # 耳
            if self.dog_type == "コーギー":
                # コーギーの三角形の耳
                pygame.draw.polygon(frame, color, [
                    (size[0] // 4 * 3, size[1] // 3 - head_size // 2),
                    (size[0] // 4 * 3 + head_size // 2, size[1] // 3 - head_size),
                    (size[0] // 4 * 3 + head_size // 2, size[1] // 3 - head_size // 2)
                ])
            elif self.dog_type == "ミニチュアダックスフンド":
                # ダックスフンドの垂れ耳
                pygame.draw.ellipse(frame, color, (
                    size[0] // 4 * 3 - head_size // 4,
                    size[1] // 3 - head_size // 2,
                    head_size // 2,
                    head_size // 1.5
                ))
            elif self.dog_type == "柴犬":
                # 柴犬の三角形の耳
                pygame.draw.polygon(frame, color, [
                    (size[0] // 4 * 3, size[1] // 3 - head_size // 3),
                    (size[0] // 4 * 3 + head_size // 2, size[1] // 3 - head_size // 1.5),
                    (size[0] // 4 * 3 + head_size // 3, size[1] // 3 - head_size // 3)
                ])
            
            # 目（瞬きのアニメーション）
            if i != 2:  # 2フレーム目以外は目を開いている
                pygame.draw.circle(frame, (0, 0, 0), (size[0] // 4 * 3 - head_size // 4, size[1] // 3), 3)
            
            # 鼻
            pygame.draw.circle(frame, (0, 0, 0), (size[0] // 4 * 3 + head_size // 4, size[1] // 3 + 2), 2)
            
            # 尻尾
            tail_pos = (size[0] // 8, size[1] // 2)
            if i % 2 == 0:  # 尻尾を振るアニメーション
                pygame.draw.line(frame, color, tail_pos, (tail_pos[0] - 10, tail_pos[1] - 10), 5)
            else:
                pygame.draw.line(frame, color, tail_pos, (tail_pos[0] - 5, tail_pos[1] - 15), 5)
            
            idle_frames.append(frame)
        
        # 歩くアニメーション
        walk_frames = []
        for i in range(4):
            frame = pygame.Surface(size, pygame.SRCALPHA)
            
            # 体
            pygame.draw.ellipse(frame, color, (0, size[1]//3, size[0], size[1]*2//3))
            
            # 頭
            head_size = size[0] // 2
            pygame.draw.circle(frame, color, (size[0] // 4 * 3, size[1] // 3), head_size // 2)
            
            # 耳（犬種ごとに異なる）
            if self.dog_type == "コーギー":
                pygame.draw.polygon(frame, color, [
                    (size[0] // 4 * 3, size[1] // 3 - head_size // 2),
                    (size[0] // 4 * 3 + head_size // 2, size[1] // 3 - head_size),
                    (size[0] // 4 * 3 + head_size // 2, size[1] // 3 - head_size // 2)
                ])
            elif self.dog_type == "ミニチュアダックスフンド":
                pygame.draw.ellipse(frame, color, (
                    size[0] // 4 * 3 - head_size // 4,
                    size[1] // 3 - head_size // 2,
                    head_size // 2,
                    head_size // 1.5
                ))
            elif self.dog_type == "柴犬":
                pygame.draw.polygon(frame, color, [
                    (size[0] // 4 * 3, size[1] // 3 - head_size // 3),
                    (size[0] // 4 * 3 + head_size // 2, size[1] // 3 - head_size // 1.5),
                    (size[0] // 4 * 3 + head_size // 3, size[1] // 3 - head_size // 3)
                ])
            
            # 目
            pygame.draw.circle(frame, (0, 0, 0), (size[0] // 4 * 3 - head_size // 4, size[1] // 3), 3)
            
            # 鼻
            pygame.draw.circle(frame, (0, 0, 0), (size[0] // 4 * 3 + head_size // 4, size[1] // 3 + 2), 2)
            
            # 足（歩くアニメーション）
            leg_offset = 5 if i % 2 == 0 else -5
            # 前足
            pygame.draw.line(frame, color, (size[0] // 4 * 3 - 10, size[1] // 3 + head_size // 2),
                            (size[0] // 4 * 3 - 10 + leg_offset, size[1] - 10), 4)
            pygame.draw.line(frame, color, (size[0] // 4 * 3 + 10, size[1] // 3 + head_size // 2),
                            (size[0] // 4 * 3 + 10 - leg_offset, size[1] - 10), 4)
            # 後ろ足
            pygame.draw.line(frame, color, (size[0] // 4, size[1] // 2 + 10),
                            (size[0] // 4 + leg_offset, size[1] - 10), 4)
            pygame.draw.line(frame, color, (size[0] // 4 + 20, size[1] // 2 + 10),
                            (size[0] // 4 + 20 - leg_offset, size[1] - 10), 4)
            
            # 尻尾
            tail_pos = (size[0] // 8, size[1] // 2)
            if i % 2 == 0:
                pygame.draw.line(frame, color, tail_pos, (tail_pos[0] - 10, tail_pos[1] - 10), 5)
            else:
                pygame.draw.line(frame, color, tail_pos, (tail_pos[0] - 5, tail_pos[1] - 15), 5)
            
            walk_frames.append(frame)
        
        # 喜ぶアニメーション
        happy_frames = []
        for i in range(4):
            frame = pygame.Surface(size, pygame.SRCALPHA)
            
            # 体
            pygame.draw.ellipse(frame, color, (0, size[1]//3 + (5 if i % 2 == 0 else 0), size[0], size[1]*2//3))
            
            # 頭
            head_size = size[0] // 2
            head_y = size[1] // 3 + (3 if i % 2 == 0 else 0)
            pygame.draw.circle(frame, color, (size[0] // 4 * 3, head_y), head_size // 2)
            
            # 耳（犬種ごとに異なる）
            if self.dog_type == "コーギー":
                pygame.draw.polygon(frame, color, [
                    (size[0] // 4 * 3, head_y - head_size // 2),
                    (size[0] // 4 * 3 + head_size // 2, head_y - head_size),
                    (size[0] // 4 * 3 + head_size // 2, head_y - head_size // 2)
                ])
            elif self.dog_type == "ミニチュアダックスフンド":
                pygame.draw.ellipse(frame, color, (
                    size[0] // 4 * 3 - head_size // 4,
                    head_y - head_size // 2,
                    head_size // 2,
                    head_size // 1.5
                ))
            elif self.dog_type == "柴犬":
                pygame.draw.polygon(frame, color, [
                    (size[0] // 4 * 3, head_y - head_size // 3),
                    (size[0] // 4 * 3 + head_size // 2, head_y - head_size // 1.5),
                    (size[0] // 4 * 3 + head_size // 3, head_y - head_size // 3)
                ])
            
            # 目（喜んでいる表情）
            pygame.draw.arc(frame, (0, 0, 0),
                          (size[0] // 4 * 3 - head_size // 4 - 5, head_y - 5, 10, 10),
                          0, 3.14, 1)
            
            # 鼻
            pygame.draw.circle(frame, (0, 0, 0), (size[0] // 4 * 3 + head_size // 4, head_y + 2), 2)
            
            # 口（笑顔）
            pygame.draw.arc(frame, (0, 0, 0),
                          (size[0] // 4 * 3 - 10, head_y + 5, 20, 10),
                          0, 3.14, 1)
            
            # 尻尾（激しく振る）
            tail_pos = (size[0] // 8, size[1] // 2)
            if i % 4 == 0:
                pygame.draw.line(frame, color, tail_pos, (tail_pos[0] - 15, tail_pos[1] - 15), 5)
            elif i % 4 == 1:
                pygame.draw.line(frame, color, tail_pos, (tail_pos[0] - 5, tail_pos[1] - 20), 5)
            elif i % 4 == 2:
                pygame.draw.line(frame, color, tail_pos, (tail_pos[0] + 5, tail_pos[1] - 20), 5)
            else:
                pygame.draw.line(frame, color, tail_pos, (tail_pos[0] + 15, tail_pos[1] - 15), 5)
            
            happy_frames.append(frame)
        
        # アニメーションを登録
        self.animations = {
            "idle": idle_frames,
            "walk": walk_frames,
            "happy": happy_frames
        }
    
    def update(self, current_time):
        """アニメーションを更新"""
        if current_time - self.last_update_time > self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_animation])
            self.last_update_time = current_time
    
    def set_animation(self, animation_name):
        """アニメーションを設定"""
        if animation_name in self.animations and self.current_animation != animation_name:
            self.current_animation = animation_name
            self.frame_index = 0
    
    def get_current_frame(self):
        """現在のフレームを取得"""
        return self.animations[self.current_animation][self.frame_index]
