import pygame
import sys
import os
import platform
import time
from game_state import GameState
from dog import Dog
from ui import UI
from utils import Utils, SaveManager

class DogTamagotchi:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("犬びより")
        
        # UI管理（ローディング画面用）
        self.ui = UI(self.screen, self.width, self.height)
        
        # ローディング画面を表示
        self.show_loading_screen()
        
        # 日本語フォントの初期化
        self.setup_japanese_font()
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # ゲームの状態管理
        self.game_state = GameState()
        
        # 犬の種類
        self.dog_types = ["コーギー", "ミニチュアダックスフンド", "柴犬"]
        self.dog = None
        
        # セーブマネージャー
        self.save_manager = SaveManager()
        
        # ゲームの状態
        self.state = self.game_state.state  # "select_dog", "main_game", "graveyard", "trainer_info"
        
        # 最後の更新時間
        self.last_update_time = time.time()
        
        # 更新間隔（秒）
        self.update_interval = 1.0  # 1秒ごとに更新
    
    def show_loading_screen(self):
        """ローディング画面を表示"""
        # ローディングの進捗
        progress = 0.0
        
        while progress < 1.0:
            # ローディング画面を描画
            self.ui.draw_loading_screen(progress)
            
            # 進捗を更新
            progress += 0.01
            
            # 少し待機
            pygame.time.delay(20)
            
            # イベント処理（ウィンドウを閉じる操作など）
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
        # 最終的なローディング画面を表示
        self.ui.draw_loading_screen(1.0)
        pygame.time.delay(500)  # 0.5秒待機
    
    def setup_japanese_font(self):
        """日本語フォントの初期化"""
        system = platform.system()
        
        if system == "Windows":
            # Windowsの場合
            font_paths = [
                "C:\\Windows\\Fonts\\msgothic.ttc",
                "C:\\Windows\\Fonts\\meiryo.ttc",
                "C:\\Windows\\Fonts\\YuGothM.ttc"
            ]
            
            for path in font_paths:
                if os.path.exists(path):
                    pygame.font.Font(path, 24)  # フォントを事前に読み込む
                    break
                    
        elif system == "Darwin":  # macOS
            # macOSの場合
            font_paths = [
                "/System/Library/Fonts/Hiragino Sans GB.ttc",
                "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
                "/System/Library/Fonts/AppleGothic.ttf",
                "/Library/Fonts/Osaka.ttf"
            ]
            
            for path in font_paths:
                if os.path.exists(path):
                    pygame.font.Font(path, 24)  # フォントを事前に読み込む
                    break
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                
                if self.state == "select_dog":
                    self.handle_dog_selection(event)
                elif self.state == "main_game":
                    self.handle_main_game(event)
                elif self.state == "graveyard":
                    self.handle_graveyard(event)
                elif self.state == "trainer_info":
                    self.handle_trainer_info(event)
            
            # ゲーム状態の同期
            self.state = self.game_state.state
            
            # 定期的に更新
            current_time = time.time()
            if current_time - self.last_update_time >= self.update_interval:
                self.update()
                self.last_update_time = current_time
            
            self.render()
            pygame.display.flip()  # 毎フレーム画面を更新
            self.clock.tick(self.fps)
    
    def handle_dog_selection(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            selected_dog = self.ui.check_dog_selection(mouse_pos, self.dog_types)
            
            if selected_dog is not None:
                # 犬を選択した場合の処理
                self.dog = Dog(selected_dog)
                # 状態を先に更新
                self.state = "main_game"
                # ゲーム状態を更新
                self.game_state.start_game(self.dog)
                # ゲーム状態の同期を確実に行う
                self.game_state.state = "main_game"
                return  # 他の処理を行わずに関数を抜ける
            
            # メニューボタンのチェック
            menu_item = self.ui.check_menu_selection(mouse_pos)
            if menu_item == "墓地を見る":
                self.game_state.show_graveyard()
                # 状態を更新してから即座に画面を描画
                self.state = self.game_state.state
                self.render()
                pygame.display.flip()  # 画面を強制的に更新
            elif menu_item == "トレーナー情報":
                self.game_state.show_trainer_info()
                # 状態を更新してから即座に画面を描画
                self.state = self.game_state.state
                self.render()
                pygame.display.flip()  # 画面を強制的に更新
    
    def handle_main_game(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            action = self.ui.check_action_selection(mouse_pos)
            
            if action is not None:
                if action == "restart":
                    self.game_state.restart_game()
                    # 状態を更新
                    self.state = self.game_state.state
                else:
                    self.game_state.perform_action(action)
            
            # メニューボタンのチェック
            menu_item = self.ui.check_menu_selection(mouse_pos)
            if menu_item == "墓地を見る":
                self.game_state.show_graveyard()
                # 状態を更新
                self.state = self.game_state.state
            elif menu_item == "トレーナー情報":
                self.game_state.show_trainer_info()
                # 状態を更新
                self.state = self.game_state.state
    
    def handle_graveyard(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            action = self.ui.check_action_selection(mouse_pos)
            
            if action == "back":
                self.game_state.back_to_main()
                # 状態を更新
                self.state = self.game_state.state
    
    def handle_trainer_info(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            action = self.ui.check_action_selection(mouse_pos)
            
            if action == "back":
                self.game_state.back_to_main()
                # 状態を更新
                self.state = self.game_state.state
    
    def update(self):
        if self.state == "main_game":
            self.game_state.update()
    
    def render(self):
        self.screen.fill((255, 255, 255))
        
        if self.state == "select_dog":
            self.ui.draw_dog_selection(self.dog_types)
        elif self.state == "main_game":
            self.ui.draw_main_game(self.game_state.dog, self.game_state)
        elif self.state == "graveyard":
            self.ui.draw_graveyard(self.save_manager.graveyard)
        elif self.state == "trainer_info":
            self.ui.draw_trainer_info(self.save_manager.trainer_data)
        
        pygame.display.flip()
    
    def quit_game(self):
        # ゲームデータを保存
        if self.game_state.dog and self.game_state.dog.is_alive:
            self.game_state.save_current_game()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # セーブディレクトリの作成
    save_dir = "saves"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    game = DogTamagotchi()
    game.run()
