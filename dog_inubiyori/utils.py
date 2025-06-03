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
        
        # 現在のゲームデータのファイルパス
        self.current_game_file = os.path.join(self.save_dir, "current_game.json")
        
        # トレーナーデータの初期化
        self.trainer_data = self.load_trainer_data()
        
        # 墓地データの初期化
        self.graveyard = self.load_graveyard()
    
    def ensure_save_directory(self):
        """セーブディレクトリが存在することを確認"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
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
    
    def load_current_game(self):
        """現在のゲームデータをロード"""
        if os.path.exists(self.current_game_file):
            try:
                with open(self.current_game_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
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
    
    def save_current_game(self, dog_data):
        """現在のゲームデータを保存"""
        with open(self.current_game_file, 'w', encoding='utf-8') as f:
            json.dump(dog_data, f, ensure_ascii=False, indent=2)
    
    def delete_current_game(self):
        """現在のゲームデータを削除"""
        if os.path.exists(self.current_game_file):
            os.remove(self.current_game_file)
    
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
