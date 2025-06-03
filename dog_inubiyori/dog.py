import time  # 時間管理のためのインポート

class Dog:
    def __init__(self, dog_type, name=None, saved_data=None):
        self.dog_type = dog_type
        self.name = name if name else dog_type  # 初期値として犬種を名前にする
        
        # 犬のステータス
        self.hunger = 50      # 満腹度（0-100）
        self.happiness = 50   # 幸福度（0-100）
        self.discipline = 50  # しつけ度（0-100）
        self.cleanliness = 50 # 清潔度（0-100）
        self.energy = 50      # 元気度（0-100）
        
        # 成長段階
        self.growth_stage = "子犬"  # "子犬", "成犬", "老犬"
        
        # 成長と寿命の管理
        self.birth_time = time.time()
        self.last_update_time = self.birth_time
        self.growth_points = 0
        self.lifespan_days = 0  # 生存日数
        
        # 健康状態
        self.is_alive = True
        self.health = 100  # 健康度（0-100）
        self.sick_days = 0  # 病気の日数
        
        # 犬種ごとの特性
        self.set_dog_traits()
        
        # 画像パス（プレースホルダー）
        self.image_path = f"assets/{dog_type.lower()}.png"
        
        # 保存データがある場合は復元
        if saved_data:
            self.restore_from_save(saved_data)
    
    def set_dog_traits(self):
        """犬種ごとの特性を設定"""
        if self.dog_type == "コーギー":
            self.trait = "活発で賢い"
            self.hunger_rate = 1.2  # 食欲が少し高い
            self.energy_rate = 1.5  # 元気いっぱい
            self.growth_rate = 1.0  # 標準的な成長速度
            self.max_lifespan = 30  # 最大寿命（日数）
        elif self.dog_type == "ミニチュアダックスフンド":
            self.trait = "好奇心旺盛"
            self.hunger_rate = 1.0
            self.energy_rate = 1.2
            self.growth_rate = 0.9  # やや遅い成長速度
            self.max_lifespan = 35  # 最大寿命（日数）
        elif self.dog_type == "柴犬":
            self.trait = "忠実で勇敢"
            self.hunger_rate = 1.1
            self.energy_rate = 1.3
            self.growth_rate = 1.1  # やや早い成長速度
            self.max_lifespan = 28  # 最大寿命（日数）
    
    def feed(self, trainer_bonuses=None):
        """ご飯をあげる"""
        if not self.is_alive:
            return f"{self.name}はもういない..."
        
        bonus = 1.0
        if trainer_bonuses:
            bonus = trainer_bonuses["feed_bonus"]
        
        self.hunger = min(100, self.hunger + 30 * bonus)
        self.energy = min(100, self.energy + 10 * bonus)
        self.health = min(100, self.health + 5 * bonus)
        
        # 成長ポイントを加算
        self.growth_points += 1
        
        return f"{self.name}はご飯を美味しそうに食べた！"
    
    def walk(self, trainer_bonuses=None):
        """散歩に行く"""
        if not self.is_alive:
            return f"{self.name}はもういない..."
        
        if self.energy < 20:
            return f"{self.name}は疲れていて散歩に行きたがらない..."
        
        bonus = 1.0
        if trainer_bonuses:
            bonus = trainer_bonuses["happiness_bonus"]
        
        self.happiness = min(100, self.happiness + 20 * bonus)
        self.hunger = max(0, self.hunger - 15)
        self.energy = max(0, self.energy - 20)
        self.cleanliness = max(0, self.cleanliness - 10)
        self.health = min(100, self.health + 10 * bonus)
        
        # 成長ポイントを加算
        self.growth_points += 2
        
        return f"{self.name}と楽しく散歩した！"
    
    def train(self, trainer_bonuses=None):
        """しつけをする"""
        if not self.is_alive:
            return f"{self.name}はもういない..."
        
        if self.energy < 15:
            return f"{self.name}は疲れていてしつけに集中できない..."
        
        bonus = 1.0
        if trainer_bonuses:
            bonus = trainer_bonuses["discipline_bonus"]
        
        self.discipline = min(100, self.discipline + 25 * bonus)
        self.energy = max(0, self.energy - 15)
        self.happiness = max(0, self.happiness - 5)
        
        # 成長ポイントを加算
        self.growth_points += 1.5
        
        return f"{self.name}はしつけを頑張った！"
    
    def clean(self, trainer_bonuses=None):
        """トイレを片付ける"""
        if not self.is_alive:
            return f"{self.name}はもういない..."
        
        bonus = 1.0
        if trainer_bonuses:
            bonus = trainer_bonuses["cleanliness_bonus"]
        
        self.cleanliness = min(100, self.cleanliness + 40 * bonus)
        self.health = min(100, self.health + 5 * bonus)
        
        return f"{self.name}のトイレをきれいに片付けた！"
    
    def play(self, trainer_bonuses=None):
        """おもちゃで遊ぶ"""
        if not self.is_alive:
            return f"{self.name}はもういない..."
        
        if self.energy < 10:
            return f"{self.name}は疲れていて遊びたがらない..."
        
        bonus = 1.0
        if trainer_bonuses:
            bonus = trainer_bonuses["happiness_bonus"]
        
        self.happiness = min(100, self.happiness + 30 * bonus)
        self.energy = max(0, self.energy - 15)
        
        # 成長ポイントを加算
        self.growth_points += 1
        
        return f"{self.name}とおもちゃで楽しく遊んだ！"
    
    def update_status(self):
        """時間経過によるステータス更新"""
        current_time = time.time()
        elapsed_days = (current_time - self.last_update_time) / 86400  # 経過日数（86400秒 = 1日）
        
        # デモ用に時間を早める（1分 = 1日）
        elapsed_days = (current_time - self.last_update_time) / 60
        
        if elapsed_days > 0:
            # 生存日数を更新
            self.lifespan_days += elapsed_days
            
            # ステータスの減少（時間経過に応じて変化）
            self.hunger = max(0, self.hunger - 0.5 * self.hunger_rate * elapsed_days)
            self.happiness = max(0, self.happiness - 0.3 * elapsed_days)
            self.cleanliness = max(0, self.cleanliness - 0.2 * elapsed_days)
            self.energy = min(100, self.energy + 0.1 * self.energy_rate * elapsed_days)
            
            # 健康状態の更新
            self.update_health(elapsed_days)
            
            # 成長ポイントの更新
            if self.is_alive:
                self.update_growth(elapsed_days)
            
            self.last_update_time = current_time
    
    def get_mood(self):
        """現在の気分を取得"""
        avg_status = (self.hunger + self.happiness + self.cleanliness) / 3
        
        if avg_status > 80:
            return "とても幸せ"
        elif avg_status > 60:
            return "幸せ"
        elif avg_status > 40:
            return "普通"
        elif avg_status > 20:
            return "不満"
        else:
            return "不機嫌"
    def update_health(self, elapsed_days):
        """健康状態を更新"""
        # 健康度の計算（満腹度、幸福度、清潔度の平均）
        avg_status = (self.hunger + self.happiness + self.cleanliness) / 3
        
        if avg_status < 30:
            # 健康状態が悪い
            self.health -= 10 * elapsed_days
            self.sick_days += elapsed_days
        else:
            # 健康状態が回復
            self.health = min(100, self.health + 5 * elapsed_days)
            self.sick_days = max(0, self.sick_days - elapsed_days)
        
        # 健康度が0になるか、病気の日数が5日を超えると死亡
        if self.health <= 0 or self.sick_days >= 5:
            self.is_alive = False
    
    def update_growth(self, elapsed_days):
        """成長を更新"""
        # 成長ポイントを加算（基本値 + 健康状態による補正）
        health_factor = self.health / 100
        self.growth_points += self.growth_rate * elapsed_days * health_factor
        
        # 成長段階の更新
        if self.growth_stage == "子犬" and self.growth_points >= 30:
            self.growth_stage = "成犬"
        elif self.growth_stage == "成犬" and self.growth_points >= 100:
            self.growth_stage = "老犬"
        
        # 寿命チェック
        if self.lifespan_days >= self.max_lifespan:
            self.is_alive = False
    
    def get_mood(self):
        """現在の気分を取得"""
        if not self.is_alive:
            return "死亡"
        
        avg_status = (self.hunger + self.happiness + self.cleanliness) / 3
        
        if self.health < 30:
            return "病気"
        elif avg_status > 80:
            return "とても幸せ"
        elif avg_status > 60:
            return "幸せ"
        elif avg_status > 40:
            return "普通"
        elif avg_status > 20:
            return "不満"
        else:
            return "不機嫌"
    
    def get_animation_state(self):
        """アニメーション状態を取得"""
        if not self.is_alive:
            return "idle"  # 死亡時は静止画
        
        mood = self.get_mood()
        
        if mood == "とても幸せ" or mood == "幸せ":
            return "happy"
        elif mood == "病気" or mood == "不機嫌" or mood == "不満":
            return "idle"
        else:
            return "idle"
    
    def to_dict(self):
        """犬のデータを辞書形式で取得"""
        return {
            "dog_type": self.dog_type,
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "discipline": self.discipline,
            "cleanliness": self.cleanliness,
            "energy": self.energy,
            "growth_stage": self.growth_stage,
            "birth_time": self.birth_time,
            "last_update_time": self.last_update_time,
            "growth_points": self.growth_points,
            "lifespan_days": self.lifespan_days,
            "is_alive": self.is_alive,
            "health": self.health,
            "sick_days": self.sick_days
        }
    
    def restore_from_save(self, saved_data):
        """保存データから犬の状態を復元"""
        self.dog_type = saved_data["dog_type"]
        self.name = saved_data["name"]
        self.hunger = saved_data["hunger"]
        self.happiness = saved_data["happiness"]
        self.discipline = saved_data["discipline"]
        self.cleanliness = saved_data["cleanliness"]
        self.energy = saved_data["energy"]
        self.growth_stage = saved_data["growth_stage"]
        self.birth_time = saved_data["birth_time"]
        self.last_update_time = saved_data["last_update_time"]
        self.growth_points = saved_data["growth_points"]
        self.lifespan_days = saved_data["lifespan_days"]
        self.is_alive = saved_data["is_alive"]
        self.health = saved_data["health"]
        self.sick_days = saved_data["sick_days"]
        
        # 犬種ごとの特性を再設定
        self.set_dog_traits()

    def demo_grow(self):
        """デモ用：成長を促進する"""
        if self.growth_stage == "子犬":
            self.growth_stage = "成犬"
            self.growth_points = 30
            return f"{self.name}は成犬に成長した！"
        elif self.growth_stage == "成犬":
            self.growth_stage = "老犬"
            self.growth_points = 100
            return f"{self.name}は老犬になった！"
        else:
            return f"{self.name}はこれ以上成長できない"
    
    def demo_make_sick(self):
        """デモ用：病気にする"""
        self.health = 20
        self.sick_days = 3
        return f"{self.name}は病気になった！"
    
    def demo_kill(self):
        """デモ用：死亡させる"""
        self.is_alive = False
        self.health = 0
        return f"{self.name}は永遠の眠りについた..."
