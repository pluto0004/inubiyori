import pygame
import sys
import os
import platform
import time
from game_state import GameState
from dog import Dog
from ui import UI
from utils import Utils, SaveManager
from music_manager import MusicManager

class DogTamagotchi:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("犬びより")
        
        # 音楽マネージャーの初期化
        self.music_manager = MusicManager()
        
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
        
        # ゲームの状態
        self.state = self.game_state.state  # "dog_management", "select_dog", "main_game", "graveyard", "trainer_info"
        
        # 最後の更新時間
        self.last_update_time = time.time()
        
        # 更新間隔（秒）
        self.update_interval = 1.0  # 1秒ごとに更新
        
        # オープニング音楽を再生
        try:
            self.music_manager.play_music("opening")
        except Exception as e:
            print(f"音楽の再生に失敗しました: {e}")
    
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
                
                # --- キーボードイベントのハンドリング ---
                if self.state == "main_game" and self.game_state.dog:
                    self.ui.handle_key_event(event, self.game_state.dog)
                
                if self.state == "dog_management":
                    self.handle_dog_management(event)
                elif self.state == "select_dog":
                    self.handle_dog_selection(event)
                elif self.state == "main_game":
                    self.handle_main_game(event)
                elif self.state == "graveyard":
                    self.handle_graveyard(event)
                elif self.state == "trainer_info":
                    self.handle_trainer_info(event)
            
            # ゲーム状態の同期
            self.state = self.game_state.state
            
            # 音楽の更新
            self.update_music()
            
            # 定期的に更新
            current_time = time.time()
            if current_time - self.last_update_time >= self.update_interval:
                self.update()
                self.last_update_time = current_time
            
            self.render()
            pygame.display.flip()  # 毎フレーム画面を更新
            self.clock.tick(self.fps)
    
    def update_music(self):
        """状態に応じて音楽を更新"""
        if self.state == "select_dog" or self.state == "dog_management":
            # タイトル画面や犬管理画面では opening 音楽
            self.music_manager.play_music("opening")
        elif self.state == "main_game":
            if self.game_state.dog and not self.game_state.dog.is_alive:
                # 犬が死亡している場合は funeral 音楽
                self.music_manager.play_music("funeral")
            else:
                # 通常のゲーム画面では game 音楽
                self.music_manager.play_music("game")
    
    def handle_dog_management(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # 犬の選択をチェック
            selected_dog_id = self.ui.check_dog_selection_from_list(mouse_pos)
            if selected_dog_id is not None:
                self.game_state.select_dog(selected_dog_id)
                return
            
            # アクションボタンのチェック
            action = self.ui.check_action_selection(mouse_pos)
            if action == "add_dog":
                self.game_state.add_new_dog()
                return
            elif action == "volume_up":
                # 音量を上げる
                new_volume = self.ui.update_volume(0.1)
                self.music_manager.set_volume(new_volume)
            elif action == "volume_down":
                # 音量を下げる
                new_volume = self.ui.update_volume(-0.1)
                self.music_manager.set_volume(new_volume)
            
            # メニューボタンのチェック
            menu_item = self.ui.check_menu_selection(mouse_pos)
            if menu_item == "墓地を見る":
                self.game_state.show_graveyard()
            elif menu_item == "トレーナー情報":
                self.game_state.show_trainer_info()
    
    def handle_dog_selection(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            selected_dog = self.ui.check_dog_selection(mouse_pos, self.dog_types)
            
            if selected_dog is not None:
                # 犬を選択した場合、名前入力を促す
                dog_name = self.get_dog_name(selected_dog)
                
                # 犬を作成して名前を設定
                dog = Dog(selected_dog, name=dog_name)
                
                # 犬を追加
                self.game_state.start_game(dog)
                return  # 他の処理を行わずに関数を抜ける
            
            # メニューボタンのチェック
            menu_item = self.ui.check_menu_selection(mouse_pos)
            if menu_item == "墓地を見る":
                self.game_state.show_graveyard()
            elif menu_item == "トレーナー情報":
                self.game_state.show_trainer_info()
            
            # 音量調整ボタンのチェック
            action = self.ui.check_action_selection(mouse_pos)
            if action == "volume_up":
                # 音量を上げる
                new_volume = self.ui.update_volume(0.1)
                self.music_manager.set_volume(new_volume)
            elif action == "volume_down":
                # 音量を下げる
                new_volume = self.ui.update_volume(-0.1)
                self.music_manager.set_volume(new_volume)
    
    def get_dog_name(self, dog_type):
        """犬の名前を入力するダイアログを表示"""
        # デフォルト名は犬種
        default_name = dog_type
        
        # 入力用の変数
        input_name = ""
        input_active = True
        
        # 入力ループ
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Enterキーで確定
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        # バックスペースで1文字削除
                        input_name = input_name[:-1]
                    else:
                        # 文字入力（10文字まで）
                        if len(input_name) < 10:
                            # 入力された文字を追加
                            char = event.unicode
                            if char:  # 空でない場合のみ追加
                                input_name += char
            
            # 画面を描画
            self.screen.fill(self.ui.BACKGROUND_COLOR)
            
            # タイトル背景
            pygame.draw.rect(self.screen, (240, 240, 255), (0, 0, self.width, 80))
            pygame.draw.line(self.screen, (220, 220, 240), (0, 80), (self.width, 80), 2)
            
            # タイトル
            try:
                title = self.ui.title_font.render("犬の名前を入力してください", True, self.ui.BLACK)
            except:
                # フォールバック: 英語で表示
                title = self.ui.default_title_font.render("Enter dog name", True, self.ui.BLACK)
            
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))
            
            # 犬の種類表示
            try:
                dog_type_text = self.ui.normal_font.render(f"犬種: {dog_type}", True, self.ui.BLACK)
            except:
                # フォールバック: 英語で表示
                dog_names = {"コーギー": "Corgi", "ミニチュアダックスフンド": "Dachshund", "柴犬": "Shiba"}
                dog_type_text = self.ui.default_normal_font.render(f"Dog type: {dog_names.get(dog_type, dog_type)}", True, self.ui.BLACK)
            
            self.screen.blit(dog_type_text, (self.width // 2 - dog_type_text.get_width() // 2, 100))
            
            # 入力フィールドの背景
            input_bg_width = 300
            input_bg_height = 50
            input_bg_x = self.width // 2 - input_bg_width // 2
            input_bg_y = 150
            
            pygame.draw.rect(self.screen, self.ui.WHITE, 
                            (input_bg_x, input_bg_y, input_bg_width, input_bg_height), 
                            border_radius=8)
            pygame.draw.rect(self.screen, self.ui.BLACK, 
                            (input_bg_x, input_bg_y, input_bg_width, input_bg_height), 
                            2, border_radius=8)
            
            # 入力テキスト
            if input_name:
                try:
                    name_text = self.ui.normal_font.render(input_name, True, self.ui.BLACK)
                except:
                    name_text = self.ui.default_normal_font.render(input_name, True, self.ui.BLACK)
            else:
                # プレースホルダー
                try:
                    name_text = self.ui.normal_font.render(default_name, True, (150, 150, 150))
                except:
                    name_text = self.ui.default_normal_font.render(default_name, True, (150, 150, 150))
            
            self.screen.blit(name_text, (input_bg_x + 10, input_bg_y + input_bg_height // 2 - name_text.get_height() // 2))
            
            # カーソル表示（点滅）
            if pygame.time.get_ticks() % 1000 < 500:  # 0.5秒ごとに点滅
                cursor_x = input_bg_x + 10 + name_text.get_width()
                cursor_y = input_bg_y + 10
                pygame.draw.line(self.screen, self.ui.BLACK, 
                                (cursor_x, cursor_y), 
                                (cursor_x, cursor_y + input_bg_height - 20), 
                                2)
            
            # 説明テキスト
            try:
                info_text = self.ui.small_font.render("Enterキーで確定 (最大10文字)", True, self.ui.BLACK)
            except:
                info_text = self.ui.default_small_font.render("Press Enter to confirm (max 10 chars)", True, self.ui.BLACK)
            
            self.screen.blit(info_text, (self.width // 2 - info_text.get_width() // 2, input_bg_y + input_bg_height + 10))
            
            # 犬の画像表示
            try:
                if dog_type == "コーギー":
                    dog_img = pygame.image.load("./dog_inubiyori/assets/dogs/corgi.png")
                elif dog_type == "ミニチュアダックスフンド":
                    dog_img = pygame.image.load("./dog_inubiyori/assets/dogs/dachsuhund.png")
                elif dog_type == "柴犬":
                    dog_img = pygame.image.load("./dog_inubiyori/assets/dogs/shiba.png")
                else:
                    # 未知の犬種の場合はプレースホルダーを使用
                    dog_img = self.ui.placeholder_images[dog_type]["large"]
                
                # 画像サイズを調整
                dog_img = pygame.transform.scale(dog_img, (200, 200))
                self.screen.blit(dog_img, (self.width // 2 - dog_img.get_width() // 2, 220))
            except Exception as e:
                print(f"画像読み込みエラー: {e}")
                # エラーが発生した場合はプレースホルダーを使用
                self.screen.blit(self.ui.placeholder_images[dog_type]["large"], (self.width // 2 - 100, 220))
            
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        # 入力が空の場合はデフォルト名を使用
        if not input_name:
            input_name = default_name
        
        return input_name
    
    def handle_main_game(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            action = self.ui.check_action_selection(mouse_pos)
            
            if action is not None:
                if action == "restart":
                    self.game_state.show_dog_management()
                elif action.startswith("demo_"):
                    # デモアクションの場合
                    self.game_state.perform_action(action)
                    # 犬が死亡した場合は音楽を変更
                    if action == "demo_kill":
                        self.music_manager.play_music("funeral")
                elif action == "volume_up":
                    # 音量を上げる
                    new_volume = self.ui.update_volume(0.1)
                    self.music_manager.set_volume(new_volume)
                elif action == "volume_down":
                    # 音量を下げる
                    new_volume = self.ui.update_volume(-0.1)
                    self.music_manager.set_volume(new_volume)
                else:
                    self.game_state.perform_action(action)
            
            # メニューボタンのチェック
            menu_item = self.ui.check_menu_selection(mouse_pos)
            if menu_item == "墓地を見る":
                self.game_state.show_graveyard()
            elif menu_item == "トレーナー情報":
                self.game_state.show_trainer_info()
    
    def handle_graveyard(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            action = self.ui.check_action_selection(mouse_pos)
            
            if action == "back":
                self.game_state.back_to_main()
            elif action == "trainer_info":
                self.game_state.show_trainer_info()
            elif action == "volume_up":
                # 音量を上げる
                new_volume = self.ui.update_volume(0.1)
                self.music_manager.set_volume(new_volume)
            elif action == "volume_down":
                # 音量を下げる
                new_volume = self.ui.update_volume(-0.1)
                self.music_manager.set_volume(new_volume)
    
    def handle_trainer_info(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            action = self.ui.check_action_selection(mouse_pos)
            
            if action == "back":
                self.game_state.back_to_main()
            elif action == "volume_up":
                # 音量を上げる
                new_volume = self.ui.update_volume(0.1)
                self.music_manager.set_volume(new_volume)
            elif action == "volume_down":
                # 音量を下げる
                new_volume = self.ui.update_volume(-0.1)
                self.music_manager.set_volume(new_volume)
    
    def update(self):
        self.game_state.update()
    
    def render(self):
        self.screen.fill((255, 255, 255))
        
        if self.state == "dog_management":
            self.ui.draw_dog_management(self.game_state.dogs)
        elif self.state == "select_dog":
            self.ui.draw_dog_selection(self.dog_types)
        elif self.state == "main_game":
            self.ui.draw_main_game(self.game_state.dog, self.game_state)
        elif self.state == "graveyard":
            self.ui.draw_graveyard(self.game_state.save_manager.graveyard)
        elif self.state == "trainer_info":
            self.ui.draw_trainer_info(self.game_state.save_manager.trainer_data)
    
    def quit_game(self):
        # ゲームデータを保存
        for dog in self.game_state.dogs:
            if dog.is_alive:
                self.game_state.save_manager.save_dog(dog.to_dict())
        
        # 音楽を停止
        self.music_manager.stop_music()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # セーブディレクトリの作成
    save_dir = "saves"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    game = DogTamagotchi()
    game.run()
