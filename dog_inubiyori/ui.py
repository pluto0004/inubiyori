import pygame
import os
from utils import Utils
from animation import Animation

class UI:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # フォント初期化
        pygame.font.init()
        
        # フォントの作成
        self.create_fonts()
        
        # 色の定義
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.LIGHT_BLUE = (173, 216, 230)
        self.GREEN = (144, 238, 144)
        self.RED = (255, 99, 71)
        self.YELLOW = (255, 255, 153)
        self.BROWN = (139, 69, 19)
        self.HOVER_COLOR = (255, 220, 180)  # ホバー時の色
        
        # プレースホルダー画像の作成
        self.placeholder_images = self.create_placeholder_images()
        
        # 墓石画像の作成
        self.tombstone_image = self.create_tombstone_image()
        
        # ボタンの位置
        self.action_buttons = []
        self.menu_buttons = []
        
        # アニメーション
        self.animations = {}
        
        # 現在のアニメーション状態
        self.current_animation_state = "idle"
        
        # ホバー状態の追跡
        self.hover_button = None
        
        # ロゴ画像の読み込み
        try:
            self.logo_image = pygame.image.load("./dog_inubiyori/assets/logo.png")
            # 画像のアスペクト比を維持したまま適切なサイズに調整
            logo_width = 200
            aspect_ratio = self.logo_image.get_width() / self.logo_image.get_height()
            logo_height = int(logo_width / aspect_ratio)
            self.logo_image = pygame.transform.scale(self.logo_image, (logo_width, logo_height))
        except:
            self.logo_image = None
    
    def create_fonts(self):
        """フォントを作成"""
        # デフォルトフォント（フォールバック用）
        self.default_title_font = pygame.font.Font(None, 48)
        self.default_normal_font = pygame.font.Font(None, 32)
        self.default_small_font = pygame.font.Font(None, 24)
        
        # 日本語フォント
        self.title_font = Utils.get_japanese_font(48)
        self.normal_font = Utils.get_japanese_font(32)
        self.small_font = Utils.get_japanese_font(24)
        
        # フォントが正しく読み込めなかった場合はデフォルトフォントを使用
        if not self.title_font:
            self.title_font = self.default_title_font
        if not self.normal_font:
            self.normal_font = self.default_normal_font
        if not self.small_font:
            self.small_font = self.default_small_font
    
    def create_placeholder_images(self):
        """プレースホルダー画像を作成"""
        images = {}
        dog_types = ["コーギー", "ミニチュアダックスフンド", "柴犬"]
        colors = [(255, 200, 100), (150, 100, 50), (255, 150, 50)]
        
        for i, dog_type in enumerate(dog_types):
            # 犬の選択画面用の小さい画像
            small_img = pygame.Surface((100, 100))
            small_img.fill(colors[i])
            pygame.draw.ellipse(small_img, (255, 255, 255), (10, 10, 80, 80))
            pygame.draw.ellipse(small_img, colors[i], (15, 15, 70, 70))
            
            # メインゲーム用の大きい画像
            large_img = pygame.Surface((200, 200))
            large_img.fill(colors[i])
            pygame.draw.ellipse(large_img, (255, 255, 255), (20, 20, 160, 160))
            pygame.draw.ellipse(large_img, colors[i], (30, 30, 140, 140))
            
            images[dog_type] = {
                "small": small_img,
                "large": large_img
            }
        
        return images
    
    def create_tombstone_image(self):
        """墓石画像を作成"""
        tombstone = pygame.Surface((100, 120), pygame.SRCALPHA)
        
        # 墓石の形
        pygame.draw.rect(tombstone, self.GRAY, (20, 40, 60, 80))
        pygame.draw.rect(tombstone, self.GRAY, (10, 20, 80, 30))
        pygame.draw.rect(tombstone, self.GRAY, (0, 0, 100, 20))
        
        # 墓石の文字
        rip_text = self.small_font.render("R.I.P.", True, self.BLACK)
        tombstone.blit(rip_text, (50 - rip_text.get_width() // 2, 50))
        
        return tombstone
    
    def get_animation(self, dog_type, growth_stage):
        """アニメーションを取得"""
        key = f"{dog_type}_{growth_stage}"
        if key not in self.animations:
            self.animations[key] = Animation(dog_type, growth_stage)
        
        return self.animations[key]
    
    def draw_dog_selection(self, dog_types):
        """犬の選択画面を描画"""
        # タイトル
        try:
            title = self.title_font.render("あなたの犬を選んでください", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            title = self.default_title_font.render("Choose your dog", True, self.BLACK)
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
        
        # 犬の選択肢
        dog_names = {
            "コーギー": "コーギー",
            "ミニチュアダックスフンド": "ダックス",  # 表示名を短くする
            "柴犬": "柴犬"
        }
        
        # 犬の画像を読み込む
        dog_images = {}
        try:
            # ダックスフンドの画像
            dachshund_img = pygame.image.load("./dog_inubiyori/assets/dogs/dachsuhund.png")
            dachshund_img = pygame.transform.scale(dachshund_img, (150, 150))
            dog_images["ミニチュアダックスフンド"] = dachshund_img
            
            # 柴犬の画像
            shiba_img = pygame.image.load("./dog_inubiyori/assets/dogs/shiba.png")
            shiba_img = pygame.transform.scale(shiba_img, (150, 150))
            dog_images["柴犬"] = shiba_img
            
            # コーギーの画像（ない場合はプレースホルダー）
            try:
                corgi_img = pygame.image.load("./dog_inubiyori/assets/dogs/corgi.png")
                corgi_img = pygame.transform.scale(corgi_img, (150, 150))
                dog_images["コーギー"] = corgi_img
            except:
                dog_images["コーギー"] = self.placeholder_images["コーギー"]["large"]
        except:
            # 画像が読み込めない場合はプレースホルダーを使用
            for dog_type in dog_types:
                dog_images[dog_type] = self.placeholder_images[dog_type]["large"]
        
        # 犬の選択ボタンを描画
        button_width = 200
        button_height = 220
        margin = 50
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        
        for i, dog_type in enumerate(dog_types):
            x = (self.width - (button_width * len(dog_types) + margin * (len(dog_types) - 1))) // 2 + i * (button_width + margin)
            y = self.height // 2 - 100
            
            # ホバー効果の判定
            is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
            
            # ボタンの背景
            button_color = self.HOVER_COLOR if is_hover else (230, 230, 250)  # ホバー時は色を変える
            pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=15)
            pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), 2, border_radius=15)
            
            # 犬の画像
            if dog_type in dog_images:
                dog_img = dog_images[dog_type]
                self.screen.blit(dog_img, (x + button_width // 2 - dog_img.get_width() // 2, y + 20))
            else:
                # 画像がない場合はプレースホルダー
                self.screen.blit(self.placeholder_images[dog_type]["large"], (x + button_width // 2 - 75, y + 20))
            
            # 犬の名前
            display_name = dog_names.get(dog_type, dog_type)
            try:
                name = self.normal_font.render(display_name, True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                name = self.default_normal_font.render(dog_names.get(dog_type, dog_type), True, self.BLACK)
            
            self.screen.blit(name, (x + button_width // 2 - name.get_width() // 2, y + button_height - 40))
        
        # メニューボタン（右上に配置）
        self.draw_menu_buttons(["墓地を見る", "トレーナー情報"])
    
    def check_dog_selection(self, mouse_pos, dog_types):
        """犬の選択をチェック"""
        button_width = 200
        button_height = 220
        margin = 50
        
        for i, dog_type in enumerate(dog_types):
            x = (self.width - (button_width * len(dog_types) + margin * (len(dog_types) - 1))) // 2 + i * (button_width + margin)
            y = self.height // 2 - 100
            
            # ボタンの範囲内かチェック
            if x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height:
                return dog_type
        
        return None
    
    def draw_menu_buttons(self, menu_items):
        """メニューボタンを描画"""
        self.menu_buttons = []
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        
        for i, item in enumerate(menu_items):
            button_width = 160
            button_height = 40
            margin = 15
            
            # 右上に配置、タイトルと重ならないように調整
            x = self.width - button_width - 20
            y = 100 + i * (button_height + margin)
            
            # ホバー効果の判定
            is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
            
            # ボタンの背景
            button_color = self.HOVER_COLOR if is_hover else self.YELLOW
            pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=10)
            pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), 2, border_radius=10)
            
            # ボタンのテキスト
            try:
                item_text = self.small_font.render(item, True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                menu_names = {"墓地を見る": "Graveyard", "トレーナー情報": "Trainer Info"}
                item_text = self.default_small_font.render(menu_names.get(item, item), True, self.BLACK)
            
            self.screen.blit(item_text, (x + button_width // 2 - item_text.get_width() // 2, 
                                        y + button_height // 2 - item_text.get_height() // 2))
            
            # ボタンの位置を保存
            self.menu_buttons.append((x, y, button_width, button_height, item))
    
    def check_menu_selection(self, mouse_pos):
        """メニューの選択をチェック"""
        for x, y, width, height, item in self.menu_buttons:
            if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
                return item
        
        return None
    
    def draw_loading_screen(self, progress=0):
        """ローディング画面を描画"""
        # 背景を塗りつぶす
        self.screen.fill(self.WHITE)
        
        # ロゴ画像を表示
        if self.logo_image:
            logo_y = 50
            self.screen.blit(self.logo_image, (self.width // 2 - self.logo_image.get_width() // 2, logo_y))
            title_y = logo_y + self.logo_image.get_height() + 20
        else:
            title_y = self.height // 3
        
        # タイトル
        try:
            title = self.title_font.render("犬のたまごっち", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            title = self.default_title_font.render("Dog Tamagotchi", True, self.BLACK)
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, title_y))
        
        # ローディングバー
        bar_width = 400
        bar_height = 30
        x = (self.width - bar_width) // 2
        y = self.height // 2 + 50  # ロゴの下に配置
        
        # バーの背景
        pygame.draw.rect(self.screen, self.GRAY, (x, y, bar_width, bar_height))
        
        # バーの進捗
        progress_width = int(bar_width * progress)
        pygame.draw.rect(self.screen, self.GREEN, (x, y, progress_width, bar_height))
        
        # バーの枠
        pygame.draw.rect(self.screen, self.BLACK, (x, y, bar_width, bar_height), 2)
        
        # ローディングテキスト
        try:
            loading_text = self.normal_font.render("ロード中...", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            loading_text = self.default_normal_font.render("Loading...", True, self.BLACK)
        
        self.screen.blit(loading_text, (self.width // 2 - loading_text.get_width() // 2, y + bar_height + 20))
        
        # 犬のアイコン（ローディングアニメーション）
        dog_icon_size = 50
        dog_x = x + progress_width - dog_icon_size // 2
        dog_y = y - dog_icon_size - 10
        
        # 進捗に応じて犬のアイコンを表示
        if progress > 0:
            pygame.draw.circle(self.screen, self.YELLOW, (dog_x, dog_y), dog_icon_size // 2)
            
            # 目
            pygame.draw.circle(self.screen, self.BLACK, (dog_x - 10, dog_y - 5), 5)
            pygame.draw.circle(self.screen, self.BLACK, (dog_x + 10, dog_y - 5), 5)
            
            # 鼻
            pygame.draw.circle(self.screen, self.BLACK, (dog_x, dog_y + 5), 3)
            
            # 口（笑顔）
            pygame.draw.arc(self.screen, self.BLACK, (dog_x - 15, dog_y, 30, 20), 0, 3.14, 2)
        
        # 進捗率テキスト
        progress_text = self.default_small_font.render(f"{int(progress * 100)}%", True, self.BLACK)
        self.screen.blit(progress_text, (x + bar_width + 10, y + bar_height // 2 - progress_text.get_height() // 2))
        
        # 画面を更新
        pygame.display.flip()
    
    def draw_main_game(self, dog, game_state):
        """メインゲーム画面を描画"""
        # 犬の名前と種類
        display_name = "ダックス" if dog.dog_type == "ミニチュアダックスフンド" else dog.dog_type
        try:
            name_text = self.title_font.render(f"{dog.name} ({display_name})", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            dog_names = {"コーギー": "Corgi", "ミニチュアダックスフンド": "Dachshund", "柴犬": "Shiba"}
            name_text = self.default_title_font.render(f"{dog.name} ({dog_names.get(dog.dog_type, dog.dog_type)})", True, self.BLACK)
        
        self.screen.blit(name_text, (self.width // 2 - name_text.get_width() // 2, 20))
        
        # 成長段階
        try:
            growth_text = self.normal_font.render(f"成長段階: {dog.growth_stage}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            growth_names = {"子犬": "Puppy", "成犬": "Adult", "老犬": "Senior"}
            growth_text = self.default_normal_font.render(f"Growth: {growth_names.get(dog.growth_stage, dog.growth_stage)}", True, self.BLACK)
        
        self.screen.blit(growth_text, (self.width // 2 - growth_text.get_width() // 2, 70))
        
        # 生存日数
        try:
            days_text = self.small_font.render(f"生存日数: {int(dog.lifespan_days)}日", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            days_text = self.default_small_font.render(f"Days: {int(dog.lifespan_days)}", True, self.BLACK)
        
        self.screen.blit(days_text, (self.width // 2 - days_text.get_width() // 2, 110))
        
        # 犬のアニメーション
        if dog.is_alive:
            animation = self.get_animation(dog.dog_type, dog.growth_stage)
            animation_state = dog.get_animation_state()
            
            # アニメーション状態を更新
            if self.current_animation_state != animation_state:
                animation.set_animation(animation_state)
                self.current_animation_state = animation_state
            
            # アニメーションを更新
            animation.update(pygame.time.get_ticks())
            
            # アニメーションを描画
            dog_img = animation.get_current_frame()
            self.screen.blit(dog_img, (self.width // 2 - dog_img.get_width() // 2, 140))
        else:
            # 死亡時は墓石を表示
            self.screen.blit(self.tombstone_image, (self.width // 2 - 50, 140))
        
        # 犬のステータス
        self.draw_status_bars(dog, 350)  # Y座標を調整
        
        # メッセージ表示用の背景（読みやすくするため）
        message_y = 480  # メッセージ位置を上に移動
        message_height = 60
        pygame.draw.rect(self.screen, (240, 240, 240), (0, message_y - 10, self.width, message_height), border_radius=5)
        
        # メッセージ
        try:
            message = self.normal_font.render(game_state.message, True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            message_map = {
                "犬を選んでください": "Please select a dog",
                "もういない": "is gone",
                "永遠の眠りについた": "has passed away",
                "ご飯を美味しそうに食べた": "ate the food happily",
                "楽しく散歩した": "enjoyed the walk",
                "しつけを頑張った": "trained well",
                "トイレをきれいに片付けた": "toilet is clean now",
                "おもちゃで楽しく遊んだ": "played with toys happily",
                "疲れていて散歩に行きたがらない": "is too tired to walk",
                "疲れていてしつけに集中できない": "is too tired to train",
                "疲れていて遊びたがらない": "is too tired to play",
                "とても幸せ": "very happy",
                "幸せ": "happy",
                "普通": "normal",
                "不満": "unsatisfied",
                "不機嫌": "grumpy",
                "病気": "sick"
            }
            
            # メッセージを英語に変換
            eng_message = game_state.message
            for jp, eng in message_map.items():
                if jp in eng_message:
                    eng_message = eng_message.replace(jp, eng)
            
            message = self.default_normal_font.render(eng_message, True, self.BLACK)
        
        # メッセージ表示位置を調整
        self.screen.blit(message, (self.width // 2 - message.get_width() // 2, message_y))
        
        # デモ用ショートカットボタン（右下に配置）
        if dog.is_alive:
            self.draw_demo_buttons(dog)
        
        # アクションボタンは不要（ステータスバーの横に配置済み）
        
        # 再スタートボタン（死亡時のみ）
        if not dog.is_alive:
            self.draw_restart_button()
        
        # メニューボタン
        self.draw_menu_buttons(["墓地を見る", "トレーナー情報"])
    
    def draw_status_bars(self, dog, start_y=80):
        """ステータスバーを描画"""
        status_items = [
            ("満腹度", "Hunger", dog.hunger, self.GREEN, "ご飯をあげる"),
            ("幸福度", "Happiness", dog.happiness, self.YELLOW, "おもちゃで遊ぶ"),
            ("しつけ度", "Discipline", dog.discipline, self.LIGHT_BLUE, "しつけをする"),
            ("清潔度", "Cleanliness", dog.cleanliness, self.WHITE, "トイレを片付ける"),
            ("元気度", "Energy", dog.energy, self.RED, "散歩にいく"),
            ("健康度", "Health", dog.health, self.GREEN, None)
        ]
        
        # ステータスバーの背景
        status_bg_height = len(status_items) * 30 + 20
        pygame.draw.rect(self.screen, (245, 245, 245), (10, start_y - 10, 450, status_bg_height), border_radius=10)
        
        self.action_buttons = []  # ボタンリストをクリア
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (jp_name, en_name, value, color, action) in enumerate(status_items):
            x = 20
            y = start_y + i * 30
            
            # ステータス名
            try:
                status_name = self.small_font.render(jp_name, True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                status_name = self.default_small_font.render(en_name, True, self.BLACK)
            
            self.screen.blit(status_name, (x, y))
            
            # ステータスバーの背景
            pygame.draw.rect(self.screen, self.GRAY, (x + 100, y, 150, 20))
            
            # ステータスバーの値
            pygame.draw.rect(self.screen, color, (x + 100, y, value * 1.5, 20))
            
            # ステータス値
            value_text = self.default_small_font.render(f"{int(value)}", True, self.BLACK)
            self.screen.blit(value_text, (x + 260, y))
            
            # アクションボタン（対応するアクションがある場合）
            if action and dog.is_alive:
                button_width = 120
                button_height = 25
                button_x = x + 300
                button_y = y - 2
                
                # ホバー効果の判定
                is_hover = button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height
                
                # ボタンの背景
                button_color = self.HOVER_COLOR if is_hover else self.LIGHT_BLUE
                pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height), border_radius=5)
                pygame.draw.rect(self.screen, self.BLACK, (button_x, button_y, button_width, button_height), 1, border_radius=5)
                
                # ボタンのテキスト
                try:
                    action_text = self.small_font.render(action, True, self.BLACK)
                except:
                    # フォールバック: 英語で表示
                    action_names = {
                        "ご飯をあげる": "Feed",
                        "散歩にいく": "Walk",
                        "しつけをする": "Train",
                        "トイレを片付ける": "Clean",
                        "おもちゃで遊ぶ": "Play"
                    }
                    action_text = self.default_small_font.render(action_names.get(action, action), True, self.BLACK)
                
                # テキストが長すぎる場合はフォントサイズを調整
                if action_text.get_width() > button_width - 10:
                    try:
                        smaller_font = Utils.get_japanese_font(18)  # 小さいフォント
                        action_text = smaller_font.render(action, True, self.BLACK)
                    except:
                        smaller_font = pygame.font.Font(None, 18)
                        action_text = smaller_font.render(action_names.get(action, action), True, self.BLACK)
                
                # テキストを中央に配置
                self.screen.blit(action_text, (button_x + button_width // 2 - action_text.get_width() // 2, 
                                            button_y + button_height // 2 - action_text.get_height() // 2))
                
                # ボタンの位置を保存
                self.action_buttons.append((button_x, button_y, button_width, button_height, action))
    
    def draw_action_buttons(self, actions):
        """アクションボタンを描画"""
        self.action_buttons = []
        
        # ボタンの配置を調整
        button_width = 150  # ボタン幅を広げる
        button_height = 50  # ボタン高さを高くする
        margin = 20  # マージンを広げる
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        
        # 画面サイズに応じてボタンを配置
        if self.width < 600:  # モバイルサイズ対応
            # 縦に並べる（1列）
            for i, action in enumerate(actions):
                x = (self.width - button_width) // 2
                y = self.height - 300 + i * (button_height + margin)
                
                # ホバー効果の判定
                is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
                
                # ボタンの背景
                button_color = self.HOVER_COLOR if is_hover else self.LIGHT_BLUE
                pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=10)
                pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), 2, border_radius=10)
                
                # ボタンのテキスト
                try:
                    action_text = self.small_font.render(action, True, self.BLACK)
                except:
                    # フォールバック: 英語で表示
                    action_names = {
                        "ご飯をあげる": "Feed",
                        "散歩にいく": "Walk",
                        "しつけをする": "Train",
                        "トイレを片付ける": "Clean",
                        "おもちゃで遊ぶ": "Play"
                    }
                    action_text = self.default_small_font.render(action_names.get(action, action), True, self.BLACK)
                
                # テキストが長すぎる場合はフォントサイズを調整
                if action_text.get_width() > button_width - 20:
                    try:
                        smaller_font = Utils.get_japanese_font(20)  # 小さいフォント
                        action_text = smaller_font.render(action, True, self.BLACK)
                    except:
                        smaller_font = pygame.font.Font(None, 20)
                        action_text = smaller_font.render(action_names.get(action, action), True, self.BLACK)
                
                # テキストを中央に配置
                self.screen.blit(action_text, (x + button_width // 2 - action_text.get_width() // 2, 
                                            y + button_height // 2 - action_text.get_height() // 2))
                
                # ボタンの位置を保存
                self.action_buttons.append((x, y, button_width, button_height, action))
        else:
            # 画面幅に収まらない場合は2行に分ける
            if len(actions) > 3:
                buttons_per_row = 3
                rows = (len(actions) + buttons_per_row - 1) // buttons_per_row
                
                for i, action in enumerate(actions):
                    row = i // buttons_per_row
                    col = i % buttons_per_row
                    
                    row_buttons = min(buttons_per_row, len(actions) - row * buttons_per_row)
                    row_width = button_width * row_buttons + margin * (row_buttons - 1)
                    
                    x = (self.width - row_width) // 2 + col * (button_width + margin)
                    y = self.height - 150 + row * (button_height + margin)
                    
                    # ホバー効果の判定
                    is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
                    
                    # ボタンの背景
                    button_color = self.HOVER_COLOR if is_hover else self.LIGHT_BLUE
                    pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=10)
                    pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), 2, border_radius=10)
                    
                    # ボタンのテキスト
                    try:
                        action_text = self.small_font.render(action, True, self.BLACK)
                    except:
                        # フォールバック: 英語で表示
                        action_names = {
                            "ご飯をあげる": "Feed",
                            "散歩にいく": "Walk",
                            "しつけをする": "Train",
                            "トイレを片付ける": "Clean",
                            "おもちゃで遊ぶ": "Play"
                        }
                        action_text = self.default_small_font.render(action_names.get(action, action), True, self.BLACK)
                    
                    # テキストが長すぎる場合はフォントサイズを調整
                    if action_text.get_width() > button_width - 20:
                        try:
                            smaller_font = Utils.get_japanese_font(20)  # 小さいフォント
                            action_text = smaller_font.render(action, True, self.BLACK)
                        except:
                            smaller_font = pygame.font.Font(None, 20)
                            action_text = smaller_font.render(action_names.get(action, action), True, self.BLACK)
                    
                    # テキストを中央に配置
                    self.screen.blit(action_text, (x + button_width // 2 - action_text.get_width() // 2, 
                                                y + button_height // 2 - action_text.get_height() // 2))
                    
                    # ボタンの位置を保存
                    self.action_buttons.append((x, y, button_width, button_height, action))
            else:
                # 1行に収まる場合
                total_width = button_width * len(actions) + margin * (len(actions) - 1)
                
                for i, action in enumerate(actions):
                    x = (self.width - total_width) // 2 + i * (button_width + margin)
                    y = self.height - 100
                    
                    # ホバー効果の判定
                    is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
                    
                    # ボタンの背景
                    button_color = self.HOVER_COLOR if is_hover else self.LIGHT_BLUE
                    pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=10)
                    pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), 2, border_radius=10)
                    
                    # ボタンのテキスト
                    try:
                        action_text = self.small_font.render(action, True, self.BLACK)
                    except:
                        # フォールバック: 英語で表示
                        action_names = {
                            "ご飯をあげる": "Feed",
                            "散歩にいく": "Walk",
                            "しつけをする": "Train",
                            "トイレを片付ける": "Clean",
                            "おもちゃで遊ぶ": "Play"
                        }
                        action_text = self.default_small_font.render(action_names.get(action, action), True, self.BLACK)
                    
                    # テキストが長すぎる場合はフォントサイズを調整
                    if action_text.get_width() > button_width - 20:
                        try:
                            smaller_font = Utils.get_japanese_font(20)  # 小さいフォント
                            action_text = smaller_font.render(action, True, self.BLACK)
                        except:
                            smaller_font = pygame.font.Font(None, 20)
                            action_text = smaller_font.render(action_names.get(action, action), True, self.BLACK)
                    
                    # テキストを中央に配置
                    self.screen.blit(action_text, (x + button_width // 2 - action_text.get_width() // 2, 
                                                y + button_height // 2 - action_text.get_height() // 2))
                    
                    # ボタンの位置を保存
                    self.action_buttons.append((x, y, button_width, button_height, action))
    
    def draw_restart_button(self):
        """再スタートボタンを描画"""
        self.action_buttons = []
        
        button_width = 220
        button_height = 60
        x = self.width // 2 - button_width // 2
        y = self.height - 100
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
        
        # ボタンの背景
        button_color = self.HOVER_COLOR if is_hover else self.GREEN
        pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=15)
        pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), 2, border_radius=15)
        
        # ボタンのテキスト
        try:
            restart_text = self.normal_font.render("新しい犬を選ぶ", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            restart_text = self.default_normal_font.render("Choose a new dog", True, self.BLACK)
        
        self.screen.blit(restart_text, (x + button_width // 2 - restart_text.get_width() // 2, 
                                      y + button_height // 2 - restart_text.get_height() // 2))
        
        # ボタンの位置を保存
        self.action_buttons.append((x, y, button_width, button_height, "restart"))
    
    def draw_back_button(self):
        """戻るボタンを描画"""
        self.action_buttons = []
        
        button_width = 120
        button_height = 50
        x = 20
        y = 20
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
        
        # ボタンの背景
        button_color = self.HOVER_COLOR if is_hover else self.LIGHT_BLUE
        pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), 2, border_radius=10)
        
        # ボタンのテキスト
        try:
            back_text = self.normal_font.render("戻る", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            back_text = self.default_normal_font.render("Back", True, self.BLACK)
        
        self.screen.blit(back_text, (x + button_width // 2 - back_text.get_width() // 2, 
                                    y + button_height // 2 - back_text.get_height() // 2))
        
        # ボタンの位置を保存
        self.action_buttons.append((x, y, button_width, button_height, "back"))
    
    def check_action_selection(self, mouse_pos):
        """アクションの選択をチェック"""
        for x, y, width, height, action in self.action_buttons:
            if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
                return action
        
        return None
    
    def draw_graveyard(self, graveyard):
        """墓地画面を描画"""
        # タイトル
        try:
            title = self.title_font.render("犬の墓地", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            title = self.default_title_font.render("Dog Graveyard", True, self.BLACK)
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))
        
        if not graveyard:
            # 墓地が空の場合
            try:
                message = self.normal_font.render("まだ墓地はありません", True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                message = self.default_normal_font.render("No graves yet", True, self.BLACK)
            
            self.screen.blit(message, (self.width // 2 - message.get_width() // 2, self.height // 2))
        else:
            # 墓石を描画
            max_per_row = 3
            for i, grave in enumerate(graveyard):
                row = i // max_per_row
                col = i % max_per_row
                
                x = self.width // 4 * (col + 1) - 50
                y = 100 + row * 180  # 間隔を狭める
                
                # 墓石
                self.screen.blit(self.tombstone_image, (x, y))
                
                # 犬の名前
                try:
                    name = self.small_font.render(grave["name"], True, self.BLACK)
                except:
                    # フォールバック: 英語で表示
                    name = self.default_small_font.render(grave["name"], True, self.BLACK)
                
                self.screen.blit(name, (x + 50 - name.get_width() // 2, y + 130))
                
                # 犬種と成長段階を1行にまとめる
                display_type = "ダックス" if grave["dog_type"] == "ミニチュアダックスフンド" else grave["dog_type"]
                try:
                    dog_info = self.small_font.render(f"{display_type} ({grave['growth_stage']})", True, self.BLACK)
                except:
                    # フォールバック: 英語で表示
                    dog_names = {"コーギー": "Corgi", "ミニチュアダックスフンド": "Dachshund", "柴犬": "Shiba"}
                    growth_names = {"子犬": "Puppy", "成犬": "Adult", "老犬": "Senior"}
                    dog_info = self.default_small_font.render(
                        f"{dog_names.get(grave['dog_type'], grave['dog_type'])} ({growth_names.get(grave['growth_stage'], grave['growth_stage'])})", 
                        True, self.BLACK
                    )
                
                self.screen.blit(dog_info, (x + 50 - dog_info.get_width() // 2, y + 150))
                
                # 生存日数
                try:
                    lifespan = self.small_font.render(f"{int(grave['lifespan'])}日", True, self.BLACK)
                except:
                    # フォールバック: 英語で表示
                    lifespan = self.default_small_font.render(f"{int(grave['lifespan'])} days", True, self.BLACK)
                
                self.screen.blit(lifespan, (x + 50 - lifespan.get_width() // 2, y + 170))
        
        # 戻るボタン
        self.draw_back_button()
    
    def draw_trainer_info(self, trainer_data):
        """トレーナー情報画面を描画"""
        # タイトル
        try:
            title = self.title_font.render("トレーナー情報", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            title = self.default_title_font.render("Trainer Info", True, self.BLACK)
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))
        
        # トレーナーレベル
        try:
            level_text = self.normal_font.render(f"トレーナーレベル: {trainer_data['trainer_level']}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            level_text = self.default_normal_font.render(f"Trainer Level: {trainer_data['trainer_level']}", True, self.BLACK)
        
        self.screen.blit(level_text, (self.width // 2 - level_text.get_width() // 2, 80))
        
        # 経験値
        try:
            exp_text = self.normal_font.render(f"経験値: {trainer_data['trainer_exp']} / {trainer_data['trainer_level'] * 100}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            exp_text = self.default_normal_font.render(f"EXP: {trainer_data['trainer_exp']} / {trainer_data['trainer_level'] * 100}", True, self.BLACK)
        
        self.screen.blit(exp_text, (self.width // 2 - exp_text.get_width() // 2, 120))
        
        # 育てた犬の数
        dogs_raised = trainer_data["dogs_raised"]
        total_dogs = sum(dogs_raised.values())
        
        try:
            dogs_text = self.normal_font.render(f"育てた犬の総数: {total_dogs}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            dogs_text = self.default_normal_font.render(f"Total Dogs Raised: {total_dogs}", True, self.BLACK)
        
        self.screen.blit(dogs_text, (self.width // 2 - dogs_text.get_width() // 2, 160))
        
        # 犬種ごとの育成数
        y = 200
        for dog_type, count in dogs_raised.items():
            display_type = "ダックス" if dog_type == "ミニチュアダックスフンド" else dog_type
            try:
                dog_text = self.small_font.render(f"{display_type}: {count}匹", True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                dog_names = {"コーギー": "Corgi", "ミニチュアダックスフンド": "Dachshund", "柴犬": "Shiba"}
                dog_text = self.default_small_font.render(f"{dog_names.get(dog_type, dog_type)}: {count}", True, self.BLACK)
            
            self.screen.blit(dog_text, (self.width // 2 - dog_text.get_width() // 2, y))
            y += 30
        
        # 死亡回数
        try:
            deaths_text = self.normal_font.render(f"死亡回数: {trainer_data['total_deaths']}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            deaths_text = self.default_normal_font.render(f"Total Deaths: {trainer_data['total_deaths']}", True, self.BLACK)
        
        self.screen.blit(deaths_text, (self.width // 2 - deaths_text.get_width() // 2, y + 20))
        
        # 最大成長段階
        try:
            max_growth_text = self.normal_font.render(f"最大成長段階: {trainer_data['max_growth_stage']}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            growth_names = {"子犬": "Puppy", "成犬": "Adult", "老犬": "Senior"}
            max_growth_text = self.default_normal_font.render(f"Max Growth Stage: {growth_names.get(trainer_data['max_growth_stage'], trainer_data['max_growth_stage'])}", True, self.BLACK)
        
        self.screen.blit(max_growth_text, (self.width // 2 - max_growth_text.get_width() // 2, y + 60))
        
        # トレーナーボーナス
        bonuses = trainer_data["bonuses"]
        
        try:
            bonus_text = self.normal_font.render("トレーナーボーナス:", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            bonus_text = self.default_normal_font.render("Trainer Bonuses:", True, self.BLACK)
        
        self.screen.blit(bonus_text, (self.width // 2 - bonus_text.get_width() // 2, y + 100))
        
        # ボーナス情報を2列に分けて表示
        bonus_items = list(bonuses.items())
        col1_items = bonus_items[:3]  # 最初の3項目
        col2_items = bonus_items[3:]  # 残りの項目
        
        name_map = {
            "feed_bonus": ("ご飯効果", "Feed Effect"),
            "happiness_bonus": ("幸福度効果", "Happiness Effect"),
            "discipline_bonus": ("しつけ効果", "Discipline Effect"),
            "cleanliness_bonus": ("清潔度効果", "Cleanliness Effect"),
            "energy_bonus": ("元気度効果", "Energy Effect")
        }
        
        # 1列目
        bonus_y = y + 140
        for bonus_name, bonus_value in col1_items:
            jp_name, en_name = name_map.get(bonus_name, (bonus_name, bonus_name))
            
            try:
                bonus_item_text = self.small_font.render(f"{jp_name}: x{bonus_value:.2f}", True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                bonus_item_text = self.default_small_font.render(f"{en_name}: x{bonus_value:.2f}", True, self.BLACK)
            
            self.screen.blit(bonus_item_text, (self.width // 4 - bonus_item_text.get_width() // 2, bonus_y))
            bonus_y += 30
        
        # 2列目
        bonus_y = y + 140
        for bonus_name, bonus_value in col2_items:
            jp_name, en_name = name_map.get(bonus_name, (bonus_name, bonus_name))
            
            try:
                bonus_item_text = self.small_font.render(f"{jp_name}: x{bonus_value:.2f}", True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                bonus_item_text = self.default_small_font.render(f"{en_name}: x{bonus_value:.2f}", True, self.BLACK)
            
            self.screen.blit(bonus_item_text, (self.width * 3 // 4 - bonus_item_text.get_width() // 2, bonus_y))
            bonus_y += 30
        
        # 戻るボタン
        self.draw_back_button()
    def draw_demo_buttons(self, dog):
        """デモ用ショートカットボタンを描画"""
        # ボタンの設定
        buttons = [
            ("成長させる", "grow"),
            ("病気にする", "make_sick"),
            ("死亡させる", "kill")
        ]
        
        button_width = 120
        button_height = 30
        margin = 10
        start_x = self.width - (button_width + margin) * len(buttons)
        y = self.height - 40
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (label, action) in enumerate(buttons):
            x = start_x + i * (button_width + margin)
            
            # ホバー効果の判定
            is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
            
            # ボタンの背景
            button_color = self.HOVER_COLOR if is_hover else (200, 100, 100)  # 赤っぽい色
            pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=5)
            pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), 1, border_radius=5)
            
            # ボタンのテキスト
            try:
                button_text = self.small_font.render(label, True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                english_labels = {"成長させる": "Grow", "病気にする": "Make Sick", "死亡させる": "Kill"}
                button_text = self.default_small_font.render(english_labels.get(label, label), True, self.BLACK)
            
            # テキストを中央に配置
            self.screen.blit(button_text, (x + button_width // 2 - button_text.get_width() // 2, 
                                        y + button_height // 2 - button_text.get_height() // 2))
            
            # ボタンの位置を保存
            self.action_buttons.append((x, y, button_width, button_height, f"demo_{action}"))
