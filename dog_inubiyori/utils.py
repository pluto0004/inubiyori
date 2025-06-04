import platform
import os
import json
import pygame
import time
from datetime import datetime

class Utils:
    @staticmethod
    def get_japanese_font(size):
        """OSに応じた日本語フォントを取得する"""
        system = platform.system()
        
        if system == "Windows":
            # Windowsの場合
            try:
                # まずはシステムフォントパスを試す
                font_paths = [
                    "C:\\Windows\\Fonts\\msgothic.ttc",
                    "C:\\Windows\\Fonts\\meiryo.ttc",
                    "C:\\Windows\\Fonts\\YuGothM.ttc"
                ]
                
                for path in font_paths:
                    if os.path.exists(path):
                        return pygame.font.Font(path, size)
            except:
                pass
            
            # フォールバック: SysFontを試す
            try:
                return pygame.font.SysFont("Arial", size)
            except:
                pass
                
        elif system == "Darwin":  # macOS
            # macOSの場合
            try:
                # システムフォントパスを試す
                font_paths = [
                    "/System/Library/Fonts/Hiragino Sans GB.ttc",
                    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
                    "/System/Library/Fonts/AppleGothic.ttf",
                    "/Library/Fonts/Osaka.ttf"
                ]
                
                for path in font_paths:
                    if os.path.exists(path):
                        return pygame.font.Font(path, size)
            except:
                pass
            
            # フォールバック: SysFontを試す
            try:
                return pygame.font.SysFont("Arial", size)
            except:
                pass
        
        # 最終フォールバック: デフォルトフォント
        return pygame.font.Font(pygame.font.get_default_font(), size)

class SaveManager:
    def __init__(self):
        self.save_dir = "saves"
        self.ensure_save_directory()
        
        # トレーナーデータのファイルパス
        self.trainer_file = os.path.join(self.save_dir, "trainer_data.json")
        
        # 墓地データのファイルパス
        self.graveyard_file = os.path.join(self.save_dir, "graveyard.json")
        
        # 犬のデータディレクトリ
        self.dogs_dir = os.path.join(self.save_dir, "dogs")
        self.ensure_dogs_directory()
        
        # トレーナーデータの初期化
        self.trainer_data = self.load_trainer_data()
        
        # 墓地データの初期化
        self.graveyard = self.load_graveyard()
        
        # 現在飼っている犬のリスト
        self.current_dogs = self.load_all_dogs()
    
    def ensure_save_directory(self):
        """セーブディレクトリが存在することを確認"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def ensure_dogs_directory(self):
        """犬のデータディレクトリが存在することを確認"""
        if not os.path.exists(self.dogs_dir):
            os.makedirs(self.dogs_dir)
    
    def load_trainer_data(self):
        """トレーナーデータをロード"""
        if os.path.exists(self.trainer_file):
            try:
                with open(self.trainer_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # デフォルトのトレーナーデータ
        return {
            "trainer_level": 1,
            "trainer_exp": 0,
            "dogs_raised": {
                "コーギー": 0,
                "ミニチュアダックスフンド": 0,
                "柴犬": 0
            },
            "total_deaths": 0,
            "max_growth_stage": "子犬",  # "子犬", "成犬", "老犬"
            "bonuses": {
                "feed_bonus": 1.0,
                "happiness_bonus": 1.0,
                "discipline_bonus": 1.0,
                "cleanliness_bonus": 1.0,
                "energy_bonus": 1.0
            }
        }
    
    def load_graveyard(self):
        """墓地データをロード"""
        if os.path.exists(self.graveyard_file):
            try:
                with open(self.graveyard_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # デフォルトの墓地データ
        return []
    
    def load_all_dogs(self):
        """すべての犬のデータをロード"""
        dogs_data = []
        
        if os.path.exists(self.dogs_dir):
            for filename in os.listdir(self.dogs_dir):
                if filename.endswith('.json'):
                    dog_file = os.path.join(self.dogs_dir, filename)
                    try:
                        with open(dog_file, 'r', encoding='utf-8') as f:
                            dog_data = json.load(f)
                            # 犬のIDをファイル名から取得
                            dog_id = filename.replace('.json', '')
                            dog_data['id'] = dog_id
                            dogs_data.append(dog_data)
                    except:
                        pass
        
        return dogs_data
    
    def load_dog(self, dog_id):
        """特定の犬のデータをロード"""
        dog_file = os.path.join(self.dogs_dir, f"{dog_id}.json")
        if os.path.exists(dog_file):
            try:
                with open(dog_file, 'r', encoding='utf-8') as f:
                    dog_data = json.load(f)
                    dog_data['id'] = dog_id
                    return dog_data
            except:
                pass
        
        return None
    
    def save_trainer_data(self):
        """トレーナーデータを保存"""
        with open(self.trainer_file, 'w', encoding='utf-8') as f:
            json.dump(self.trainer_data, f, ensure_ascii=False, indent=2)
    
    def save_graveyard(self):
        """墓地データを保存"""
        with open(self.graveyard_file, 'w', encoding='utf-8') as f:
            json.dump(self.graveyard, f, ensure_ascii=False, indent=2)
    
    def save_dog(self, dog_data):
        """犬のデータを保存"""
        # 犬のIDがない場合は新しく生成
        if 'id' not in dog_data:
            dog_id = f"dog_{int(time.time())}"
            dog_data['id'] = dog_id
        else:
            dog_id = dog_data['id']
        
        # IDはファイル名として使用するため、保存データからは削除
        save_data = dog_data.copy()
        if 'id' in save_data:
            del save_data['id']
        
        dog_file = os.path.join(self.dogs_dir, f"{dog_id}.json")
        with open(dog_file, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        # 現在の犬リストを更新
        self.update_dog_in_list(dog_data)
        
        return dog_id
    
    def update_dog_in_list(self, dog_data):
        """犬リストの中の特定の犬を更新"""
        dog_id = dog_data['id']
        
        # 既存の犬を探す
        for i, dog in enumerate(self.current_dogs):
            if dog['id'] == dog_id:
                self.current_dogs[i] = dog_data
                return
        
        # 見つからなければ追加
        self.current_dogs.append(dog_data)
    
    def delete_dog(self, dog_id):
        """犬のデータを削除"""
        dog_file = os.path.join(self.dogs_dir, f"{dog_id}.json")
        if os.path.exists(dog_file):
            os.remove(dog_file)
        
        # 現在の犬リストから削除
        self.current_dogs = [dog for dog in self.current_dogs if dog['id'] != dog_id]
    
    def add_to_graveyard(self, dog):
        """墓地に犬を追加"""
        grave = {
            "name": dog.name,
            "dog_type": dog.dog_type,
            "growth_stage": dog.growth_stage,
            "death_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "lifespan": dog.lifespan_days
        }
        
        self.graveyard.append(grave)
        self.save_graveyard()
        
        # トレーナーデータも更新
        self.trainer_data["total_deaths"] += 1
        self.trainer_data["dogs_raised"][dog.dog_type] += 1
        
        # 成長段階の最大値を更新
        growth_stages = ["子犬", "成犬", "老犬"]
        current_index = growth_stages.index(dog.growth_stage)
        max_index = growth_stages.index(self.trainer_data["max_growth_stage"])
        
        if current_index > max_index:
            self.trainer_data["max_growth_stage"] = dog.growth_stage
        
        # トレーナー経験値を追加
        exp_gain = 10  # 基本経験値
        
        # 成長段階に応じたボーナス
        if dog.growth_stage == "成犬":
            exp_gain += 20
        elif dog.growth_stage == "老犬":
            exp_gain += 50
        
        self.add_trainer_exp(exp_gain)
        
        # 犬のデータを削除
        if hasattr(dog, 'id'):
            self.delete_dog(dog.id)
    
    def add_trainer_exp(self, exp):
        """トレーナー経験値を追加し、レベルアップを処理"""
        self.trainer_data["trainer_exp"] += exp
        
        # レベルアップの処理
        level_threshold = self.trainer_data["trainer_level"] * 100
        
        while self.trainer_data["trainer_exp"] >= level_threshold:
            self.trainer_data["trainer_exp"] -= level_threshold
            self.trainer_data["trainer_level"] += 1
            
            # ボーナスの増加
            for bonus_key in self.trainer_data["bonuses"]:
                self.trainer_data["bonuses"][bonus_key] += 0.05
            
            # 次のレベルの閾値を計算
            level_threshold = self.trainer_data["trainer_level"] * 100
        
        self.save_trainer_data()
    
    def get_trainer_bonuses(self):
        """トレーナーボーナスを取得"""
        return self.trainer_data["bonuses"]
