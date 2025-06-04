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
        
        # 色の定義（洗練されたパステル調に変更）
        self.BLACK = (40, 40, 40)
        self.WHITE = (250, 250, 250)
        self.GRAY = (220, 220, 220)
        self.LIGHT_BLUE = (173, 216, 250)  # 明るいパステルブルー
        self.GREEN = (170, 220, 170)       # 柔らかいグリーン
        self.RED = (255, 120, 120)         # 柔らかいレッド
        self.YELLOW = (255, 245, 180)      # パステルイエロー
        self.BROWN = (180, 140, 100)       # 柔らかいブラウン
        self.HOVER_COLOR = (255, 235, 200) # ホバー時の淡いオレンジ
        self.BUTTON_COLOR = (230, 230, 250)  # 通常ボタンの色
        self.ACTION_BUTTON_COLOR = (200, 230, 255)  # アクションボタンの色
        self.BACKGROUND_COLOR = (250, 250, 255)  # 背景色
        
        # UI要素のサイズ設定
        self.BUTTON_RADIUS = 10  # ボタンの角丸半径
        self.STATUS_BAR_HEIGHT = 20  # ステータスバーの高さ
        
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
        
        # 音量設定
        self.volume = 0.5  # デフォルト音量
        
        # ロゴ画像の読み込み
        try:
            self.logo_image = pygame.image.load("./dog_inubiyori/assets/logo.png")
            # 画像のアスペクト比を維持したまま適切なサイズに調整
            logo_width = 240  # サイズを少し大きく
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
        self.default_tiny_font = pygame.font.Font(None, 18)  # 小さいテキスト用
        
        # 日本語フォント
        self.title_font = Utils.get_japanese_font(48)
        self.normal_font = Utils.get_japanese_font(32)
        self.small_font = Utils.get_japanese_font(24)
        self.tiny_font = Utils.get_japanese_font(18)  # 小さいテキスト用
        
        # フォントが正しく読み込めなかった場合はデフォルトフォントを使用
        if not self.title_font:
            self.title_font = self.default_title_font
        if not self.normal_font:
            self.normal_font = self.default_normal_font
        if not self.small_font:
            self.small_font = self.default_small_font
        if not self.tiny_font:
            self.tiny_font = self.default_tiny_font
    
    def create_placeholder_images(self):
        """プレースホルダー画像を作成"""
        images = {}
        dog_types = ["コーギー", "ミニチュアダックスフンド", "柴犬"]
        colors = [(255, 200, 100), (150, 100, 50), (255, 150, 50)]
        
        for i, dog_type in enumerate(dog_types):
            # 犬の選択画面用の小さい画像
            small_img = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.ellipse(small_img, colors[i], (10, 10, 80, 80))
            pygame.draw.ellipse(small_img, (255, 255, 255), (15, 15, 70, 70), 2)
            
            # 目と鼻を追加してより犬らしく
            pygame.draw.circle(small_img, (0, 0, 0), (35, 40), 5)  # 左目
            pygame.draw.circle(small_img, (0, 0, 0), (65, 40), 5)  # 右目
            pygame.draw.ellipse(small_img, (0, 0, 0), (45, 55, 10, 8))  # 鼻
            
            # メインゲーム用の大きい画像
            large_img = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.ellipse(large_img, colors[i], (20, 20, 160, 160))
            pygame.draw.ellipse(large_img, (255, 255, 255), (25, 25, 150, 150), 3)
            
            # 目と鼻を追加
            pygame.draw.circle(large_img, (0, 0, 0), (70, 80), 10)  # 左目
            pygame.draw.circle(large_img, (0, 0, 0), (130, 80), 10)  # 右目
            pygame.draw.ellipse(large_img, (0, 0, 0), (95, 110, 20, 15))  # 鼻
            
            images[dog_type] = {
                "small": small_img,
                "large": large_img
            }
        
        return images
    
    def create_tombstone_image(self):
        """墓石画像を作成"""
        tombstone = pygame.Surface((100, 120), pygame.SRCALPHA)
        
        # 墓石の形 - より立体的に
        # 墓石の本体
        pygame.draw.rect(tombstone, (180, 180, 180), (20, 40, 60, 80), border_radius=5)
        # 墓石の上部
        pygame.draw.rect(tombstone, (190, 190, 190), (10, 20, 80, 30), border_radius=3)
        pygame.draw.rect(tombstone, (200, 200, 200), (0, 0, 100, 20), border_radius=2)
        
        # 墓石に影をつける
        pygame.draw.line(tombstone, (160, 160, 160), (20, 40), (20, 120), 2)
        pygame.draw.line(tombstone, (160, 160, 160), (10, 20), (10, 50), 2)
        
        # 墓石の文字
        rip_text = self.small_font.render("R.I.P.", True, self.BLACK)
        tombstone.blit(rip_text, (50 - rip_text.get_width() // 2, 50))
        
        # 十字架を追加
        pygame.draw.rect(tombstone, (100, 100, 100), (45, 75, 10, 30), border_radius=2)
        pygame.draw.rect(tombstone, (100, 100, 100), (35, 85, 30, 10), border_radius=2)
        
        return tombstone
    
    def get_animation(self, dog_type, growth_stage):
        """アニメーションを取得"""
        key = f"{dog_type}_{growth_stage}"
        if key not in self.animations:
            self.animations[key] = Animation(dog_type, growth_stage)
        
        return self.animations[key]
    
    def draw_dog_selection(self, dog_types):
        """犬の選択画面を描画"""
        # 背景色を設定
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # タイトル
        try:
            title = self.title_font.render("あなたの犬を選んでください", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            title = self.default_title_font.render("Choose your dog", True, self.BLACK)
        
        # タイトル背景
        title_bg_rect = pygame.Rect(0, 30, self.width, 60)
        pygame.draw.rect(self.screen, (240, 240, 255), title_bg_rect)
        pygame.draw.line(self.screen, (220, 220, 240), (0, title_bg_rect.bottom), (self.width, title_bg_rect.bottom), 2)
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 40))
        
        # 音量調整ボタンを右上に配置
        self.draw_volume_controls()
        
        # 犬の選択肢
        dog_names = {
            "コーギー": "コーギー",
            "ミニチュアダックスフンド": "ダックス",  # 表示名を短くする
            "柴犬": "柴犬"
        }
        
        # 犬の画像を読み込む
        dog_images = {}
        try:
            # コーギーの画像
            corgi_img = pygame.image.load("./dog_inubiyori/assets/dogs/corgi.png")
            corgi_img = pygame.transform.scale(corgi_img, (150, 150))
            dog_images["コーギー"] = corgi_img
            
            # ダックスフンドの画像
            dachshund_img = pygame.image.load("./dog_inubiyori/assets/dogs/dachsuhund.png")
            dachshund_img = pygame.transform.scale(dachshund_img, (150, 150))
            dog_images["ミニチュアダックスフンド"] = dachshund_img
            
            # 柴犬の画像
            shiba_img = pygame.image.load("./dog_inubiyori/assets/dogs/shiba.png")
            shiba_img = pygame.transform.scale(shiba_img, (150, 150))
            dog_images["柴犬"] = shiba_img
        except Exception as e:
            print(f"画像読み込みエラー: {e}")
            # 画像が読み込めない場合はプレースホルダーを使用
            for dog_type in dog_types:
                dog_images[dog_type] = self.placeholder_images[dog_type]["large"]
        
        # 犬の選択ボタンを描画
        button_width = 220
        button_height = 250
        margin = 40
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        
        for i, dog_type in enumerate(dog_types):
            x = (self.width - (button_width * len(dog_types) + margin * (len(dog_types) - 1))) // 2 + i * (button_width + margin)
            y = self.height // 2 - 100
            
            # ホバー効果の判定
            is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
            
            # ボタンの背景
            button_color = self.HOVER_COLOR if is_hover else self.BUTTON_COLOR
            pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=15)
            
            # ボタンの枠線 - ホバー時は太く
            border_width = 3 if is_hover else 2
            pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), border_width, border_radius=15)
            
            # 犬の画像
            if dog_type in dog_images:
                dog_img = dog_images[dog_type]
                self.screen.blit(dog_img, (x + button_width // 2 - dog_img.get_width() // 2, y + 30))
            else:
                # 画像がない場合はプレースホルダー
                self.screen.blit(self.placeholder_images[dog_type]["large"], (x + button_width // 2 - 75, y + 30))
            
            # 犬の名前
            display_name = dog_names.get(dog_type, dog_type)
            try:
                name = self.normal_font.render(display_name, True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                name = self.default_normal_font.render(dog_names.get(dog_type, dog_type), True, self.BLACK)
            
            # 名前の背景
            name_bg_rect = pygame.Rect(x + 10, y + button_height - 60, button_width - 20, 40)
            pygame.draw.rect(self.screen, (255, 255, 255, 180), name_bg_rect, border_radius=8)
            
            self.screen.blit(name, (x + button_width // 2 - name.get_width() // 2, y + button_height - 50))
        
        # メニューボタン（右上に配置）
        self.draw_menu_buttons(["墓地を見る", "トレーナー"])
    
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
        
        icon_size = 40
        margin = 15
        # 右端からではなく、少し左に寄せる（例: +30px）
        offset = 30
        start_x = self.width - (icon_size + margin) * len(menu_items) - offset
        y = self.height - icon_size - 10  # 画面右下に配置
        
        for i, item in enumerate(menu_items):
            x = start_x + i * (icon_size + margin)
            
            # ホバー効果の判定
            is_hover = x <= mouse_pos[0] <= x + icon_size and y <= mouse_pos[1] <= y + icon_size
            
            # アイコンの背景（円形）
            button_color = self.HOVER_COLOR if is_hover else self.YELLOW
            pygame.draw.circle(self.screen, button_color, (x + icon_size // 2, y + icon_size // 2), icon_size // 2)
            
            # アイコンの枠線 - ホバー時は太く
            border_width = 2 if is_hover else 1
            pygame.draw.circle(self.screen, self.BLACK, (x + icon_size // 2, y + icon_size // 2), icon_size // 2, border_width)
            
            # アイコンの描画
            if item == "墓地を見る":
                # 墓石アイコン
                pygame.draw.rect(self.screen, (150, 150, 150), (x + icon_size // 2 - 8, y + 10, 16, 20), border_radius=2)
                pygame.draw.rect(self.screen, (130, 130, 130), (x + icon_size // 2 - 10, y + 5, 20, 8), border_radius=1)
                pygame.draw.line(self.screen, self.BLACK, (x + icon_size // 2, y + 15), (x + icon_size // 2, y + 25), 2)
                pygame.draw.line(self.screen, self.BLACK, (x + icon_size // 2 - 5, y + 20), (x + icon_size // 2 + 5, y + 20), 2)
            elif item == "トレーナー":
                # 人物アイコン
                pygame.draw.circle(self.screen, (100, 100, 200), (x + icon_size // 2, y + 15), 8)  # 頭
                pygame.draw.rect(self.screen, (100, 100, 200), (x + icon_size // 2 - 8, y + 23, 16, 12))  # 体
                
            # ツールチップ（ホバー時）
            if is_hover:
                try:
                    tooltip = self.tiny_font.render(item, True, self.BLACK)
                except:
                    # フォールバック: 英語で表示
                    menu_names = {"墓地を見る": "Graveyard", "トレーナー": "Trainer Info"}
                    tooltip = self.default_tiny_font.render(menu_names.get(item, item), True, self.BLACK)
                
                # ツールチップの背景
                tooltip_padding = 5
                tooltip_bg = pygame.Rect(
                    x + icon_size // 2 - tooltip.get_width() // 2 - tooltip_padding,
                    y - tooltip.get_height() - 10,
                    tooltip.get_width() + tooltip_padding * 2,
                    tooltip.get_height() + tooltip_padding * 2
                )
                pygame.draw.rect(self.screen, (255, 255, 220), tooltip_bg, border_radius=5)
                pygame.draw.rect(self.screen, self.BLACK, tooltip_bg, 1, border_radius=5)
                
                # ツールチップのテキスト
                self.screen.blit(tooltip, (x + icon_size // 2 - tooltip.get_width() // 2, y - tooltip.get_height() - 5))
            
            # ボタンの位置を保存
            self.menu_buttons.append((x, y, icon_size, icon_size, item))
            
            # アイコンの描画
            if item == "墓地を見る":
                # 墓石アイコン
                pygame.draw.rect(self.screen, (150, 150, 150), (x + icon_size // 2 - 10, y + 12, 20, 25), border_radius=2)
                pygame.draw.rect(self.screen, (130, 130, 130), (x + icon_size // 2 - 12, y + 7, 24, 10), border_radius=1)
                pygame.draw.line(self.screen, self.BLACK, (x + icon_size // 2, y + 18), (x + icon_size // 2, y + 32), 2)
                pygame.draw.line(self.screen, self.BLACK, (x + icon_size // 2 - 6, y + 25), (x + icon_size // 2 + 6, y + 25), 2)
            elif item == "トレーナー":
                # 人物アイコン
                pygame.draw.circle(self.screen, (100, 100, 200), (x + icon_size // 2, y + 18), 10)  # 頭
                pygame.draw.rect(self.screen, (100, 100, 200), (x + icon_size // 2 - 10, y + 28, 20, 15))  # 体
                
            # ツールチップ（ホバー時）
            if is_hover:
                try:
                    tooltip = self.tiny_font.render(item, True, self.BLACK)
                except:
                    # フォールバック: 英語で表示
                    menu_names = {"墓地を見る": "Graveyard", "トレーナー": "Trainer Info"}
                    tooltip = self.default_tiny_font.render(menu_names.get(item, item), True, self.BLACK)
                
                # ツールチップの背景
                tooltip_padding = 5
                tooltip_bg = pygame.Rect(
                    x + icon_size // 2 - tooltip.get_width() // 2 - tooltip_padding,
                    y - tooltip.get_height() - 10,
                    tooltip.get_width() + tooltip_padding * 2,
                    tooltip.get_height() + tooltip_padding * 2
                )
                pygame.draw.rect(self.screen, (255, 255, 220), tooltip_bg, border_radius=5)
                pygame.draw.rect(self.screen, self.BLACK, tooltip_bg, 1, border_radius=5)
                
                # ツールチップのテキスト
                self.screen.blit(tooltip, (x + icon_size // 2 - tooltip.get_width() // 2, y - tooltip.get_height() - 5))
            
            # ボタンの位置を保存
            self.menu_buttons.append((x, y, icon_size, icon_size, item))
    
    def check_menu_selection(self, mouse_pos):
        """メニューの選択をチェック"""
        for x, y, width, height, item in self.menu_buttons:
            if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
                return item
        
        return None
    
    def draw_loading_screen(self, progress=0):
        """ローディング画面を描画"""
        # 背景を塗りつぶす
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # ロゴ画像を表示
        if self.logo_image:
            logo_y = 50
            self.screen.blit(self.logo_image, (self.width // 2 - self.logo_image.get_width() // 2, logo_y))
            title_y = logo_y + self.logo_image.get_height() + 20
        else:
            title_y = self.height // 3
        
        # ローディングバー
        bar_width = 400
        bar_height = 30
        x = (self.width - bar_width) // 2
        y = self.height // 2 + 50  # ロゴの下に配置
        
        # バーの背景
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, bar_width, bar_height), border_radius=8)
        
        # バーの進捗
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            pygame.draw.rect(self.screen, self.GREEN, (x, y, progress_width, bar_height), border_radius=8)
        
        # バーの枠
        pygame.draw.rect(self.screen, self.BLACK, (x, y, bar_width, bar_height), 2, border_radius=8)
        
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
            # 犬の顔
            pygame.draw.circle(self.screen, self.YELLOW, (dog_x, dog_y), dog_icon_size // 2)
            
            # 目
            pygame.draw.circle(self.screen, self.BLACK, (dog_x - 10, dog_y - 5), 5)
            pygame.draw.circle(self.screen, self.BLACK, (dog_x + 10, dog_y - 5), 5)
            pygame.draw.circle(self.screen, self.WHITE, (dog_x - 8, dog_y - 7), 2)  # 目の光
            pygame.draw.circle(self.screen, self.WHITE, (dog_x + 12, dog_y - 7), 2)  # 目の光
            
            # 鼻
            pygame.draw.circle(self.screen, self.BLACK, (dog_x, dog_y + 5), 3)
            
            # 口（笑顔）
            pygame.draw.arc(self.screen, self.BLACK, (dog_x - 15, dog_y, 30, 20), 0, 3.14, 2)
            
            # 耳
            pygame.draw.ellipse(self.screen, self.BROWN, (dog_x - 25, dog_y - 25, 15, 25))
            pygame.draw.ellipse(self.screen, self.BROWN, (dog_x + 10, dog_y - 25, 15, 25))
        
        # 進捗率テキスト
        progress_text = self.default_small_font.render(f"{int(progress * 100)}%", True, self.BLACK)
        self.screen.blit(progress_text, (x + bar_width + 10, y + bar_height // 2 - progress_text.get_height() // 2))
        
        # 画面を更新
        pygame.display.flip()
    
    def draw_main_game(self, dog, game_state):
        """メインゲーム画面を描画"""
        # 背景を塗りつぶす
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # 上部のヘッダー背景
        pygame.draw.rect(self.screen, (240, 240, 255), (0, 0, self.width, 120))
        pygame.draw.line(self.screen, (220, 220, 240), (0, 120), (self.width, 120), 2)
        
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
        
        self.screen.blit(days_text, (self.width // 2 - days_text.get_width() // 2, 100))
        
        # 音量調整ボタンを右上に配置
        self.draw_volume_controls()
        
        # 犬のアニメーション表示エリア
        animation_area_height = 200
        pygame.draw.rect(self.screen, (250, 250, 255), (0, 130, self.width, animation_area_height))
        
        # 犬のアニメーション
        if dog.is_alive:
            # 犬の画像を表示（アニメーションがない場合）
            try:
                if dog.dog_type == "コーギー":
                    dog_img = pygame.image.load(os.path.join("dog_inubiyori", "assets", "dogs", "corgi.png"))
                elif dog.dog_type == "ミニチュアダックスフンド":
                    dog_img = pygame.image.load(os.path.join("dog_inubiyori", "assets", "dogs", "dachsuhund.png"))
                elif dog.dog_type == "柴犬":
                    dog_img = pygame.image.load(os.path.join("dog_inubiyori", "assets", "dogs", "shiba.png"))
                else:
                    # 未知の犬種の場合はプレースホルダーを使用
                    dog_img = self.placeholder_images[dog.dog_type]["large"]
                
                # 画像サイズを調整
                dog_img = pygame.transform.scale(dog_img, (180, 180))
                
                # アニメーションがある場合はそちらを優先
                animation = self.get_animation(dog.dog_type, dog.growth_stage)
                animation_state = dog.get_animation_state()
                
                # アニメーション状態を更新
                if self.current_animation_state != animation_state:
                    animation.set_animation(animation_state)
                    self.current_animation_state = animation_state
                
                # アニメーションを更新
                animation.update(pygame.time.get_ticks())
                
                # アニメーションフレームを取得
                animation_frame = animation.get_current_frame()
                
                # アニメーションがある場合はそれを表示、なければ静止画を表示
                if animation_frame:
                    self.screen.blit(animation_frame, (self.width // 2 - animation_frame.get_width() // 2, 140))
                else:
                    self.screen.blit(dog_img, (self.width // 2 - dog_img.get_width() // 2, 140))
            except Exception as e:
                print(f"画像読み込みエラー: {e}")
                # エラーが発生した場合はプレースホルダーを使用
                self.screen.blit(self.placeholder_images[dog.dog_type]["large"], (self.width // 2 - 100, 140))
        else:
            # 死亡時は墓石を表示
            self.screen.blit(self.tombstone_image, (self.width // 2 - 50, 170))
        
        # 犬のステータス
        self.draw_status_bars(dog, 350)  # Y座標を調整
        
        # メッセージ表示用の背景
        message_y = 480
        message_height = 60
        message_bg_rect = pygame.Rect(20, message_y - 10, self.width - 40, message_height)
        pygame.draw.rect(self.screen, (240, 240, 255), message_bg_rect, border_radius=10)
        pygame.draw.rect(self.screen, (220, 220, 240), message_bg_rect, 2, border_radius=10)
        
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
        # メッセージが長すぎる場合は小さいフォントで表示
        if message.get_width() > message_bg_rect.width - 20:
            try:
                message = self.small_font.render(game_state.message, True, self.BLACK)
            except:
                message = self.default_small_font.render(eng_message, True, self.BLACK)
        
        # メッセージ表示位置を調整
        self.screen.blit(message, (self.width // 2 - message.get_width() // 2, message_y + 10))
        
        # デモ用ショートカットボタン（右下に配置）
        if dog.is_alive:
            self.draw_demo_buttons(dog)
        
        # 再スタートボタン（死亡時のみ）
        if not dog.is_alive:
            self.draw_restart_button()
        
        # メニューボタン
        self.draw_menu_buttons(["墓地を見る", "トレーナー"])
        
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
        pygame.draw.rect(self.screen, (245, 245, 255), (10, start_y - 10, self.width - 20, status_bg_height), border_radius=10)
        pygame.draw.rect(self.screen, (220, 220, 240), (10, start_y - 10, self.width - 20, status_bg_height), 2, border_radius=10)
        
        self.action_buttons = []  # ボタンリストをクリア
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        
        # ステータスを2列に分けて表示
        items_per_column = 3
        column_width = 220
        
        for i, (jp_name, en_name, value, color, action) in enumerate(status_items):
            # 列と行を計算
            column = i // items_per_column
            row = i % items_per_column
            
            x = 30 + column * column_width
            y = start_y + row * 30
            
            # ステータス名
            try:
                status_name = self.small_font.render(jp_name, True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                status_name = self.default_small_font.render(en_name, True, self.BLACK)
            
            # ステータス名のフォントサイズを小さく
            if status_name.get_height() > 18:
                try:
                    smaller_font = Utils.get_japanese_font(16)
                    status_name = smaller_font.render(jp_name, True, self.BLACK)
                except:
                    smaller_font = pygame.font.Font(None, 16)
                    status_name = smaller_font.render(en_name, True, self.BLACK)
            
            self.screen.blit(status_name, (x, y + 2))  # 垂直位置を微調整
            
            # ステータスバーの背景
            bar_width = 100
            bar_x = x + 70
            bar_y = y + 2  # 垂直位置を微調整
            
            pygame.draw.rect(self.screen, self.YELLOW, (bar_x, bar_y, bar_width, self.STATUS_BAR_HEIGHT), border_radius=5)
            
            # ステータスバーの値
            value_width = min(value * bar_width / 100, bar_width)  # 値に応じた幅
            if value_width > 0:  # 値が0より大きい場合のみ描画
                pygame.draw.rect(self.screen, color, (bar_x, bar_y, value_width, self.STATUS_BAR_HEIGHT), border_radius=5)
            
            # ステータスバーの枠
            pygame.draw.rect(self.screen, self.BLACK, (bar_x, bar_y, bar_width, self.STATUS_BAR_HEIGHT), 1, border_radius=5)
            
            # ステータス値
            value_text = self.default_small_font.render(f"{int(value)}", True, self.BLACK)
            # ステータス値のフォントサイズを小さく
            if value_text.get_height() > 18:
                value_text = pygame.font.Font(None, 16).render(f"{int(value)}", True, self.BLACK)
            
            self.screen.blit(value_text, (bar_x + bar_width + 5, bar_y))
            
            # アクションボタン（対応するアクションがある場合）
            if action and dog.is_alive:
                button_width = 140
                button_height = 28
                button_x = self.width - button_width - 30
                button_y = y
                
                # ホバー効果の判定
                is_hover = button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height
                
                # ボタンの背景
                button_color = self.HOVER_COLOR if is_hover else self.ACTION_BUTTON_COLOR
                pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height), border_radius=7)
                
                # ボタンの枠線 - ホバー時は太く
                border_width = 2 if is_hover else 1
                pygame.draw.rect(self.screen, self.BLACK, (button_x, button_y, button_width, button_height), border_width, border_radius=7)
                
                # ボタンのテキスト
                try:
                    action_text = self.small_font.render(action, True, self.BLACK)
                except:
                    action_name_map = {
                        "ご飯をあげる": "Feed",
                        "散歩にいく": "Walk",
                        "しつけをする": "Train",
                        "トイレを片付ける": "Clean",
                        "おもちゃで遊ぶ": "Play"
                    }
                    action_text = self.default_small_font.render(action_name_map.get(action, action), True, self.BLACK)
                
                # テキストが長すぎる場合はさらに小さいフォントに
                if action_text.get_width() > button_width - 10:
                    try:
                        smaller_font = Utils.get_japanese_font(14)
                        action_text = smaller_font.render(action, True, self.BLACK)
                    except:
                        smaller_font = pygame.font.Font(None, 14)
                        action_name_map = {
                            "ご飯をあげる": "Feed",
                            "散歩にいく": "Walk",
                            "しつけをする": "Train",
                            "トイレを片付ける": "Clean",
                            "おもちゃで遊ぶ": "Play"
                        }
                        action_text = smaller_font.render(action_name_map.get(action, action), True, self.BLACK)
                
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
                    action_name_map = {
                        "ご飯をあげる": "Feed",
                        "散歩にいく": "Walk",
                        "しつけをする": "Train",
                        "トイレを片付ける": "Clean",
                        "おもちゃで遊ぶ": "Play"
                    }
                    action_text = self.default_small_font.render(action_name_map.get(action, action), True, self.BLACK)
                
                # テキストが長すぎる場合はフォントサイズを調整
                if action_text.get_width() > button_width - 20:
                    try:
                        smaller_font = Utils.get_japanese_font(20)  # 小さいフォント
                        action_text = smaller_font.render(action, True, self.BLACK)
                    except:
                        smaller_font = pygame.font.Font(None, 20)
                        action_text = smaller_font.render(action_name_map.get(action, action), True, self.BLACK)
                
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
                        action_name_map = {
                            "ご飯をあげる": "Feed",
                            "散歩にいく": "Walk",
                            "しつけをする": "Train",
                            "トイレを片付ける": "Clean",
                            "おもちゃで遊ぶ": "Play"
                        }
                        action_text = self.default_small_font.render(action_name_map.get(action, action), True, self.BLACK)
                    
                    # テキストが長すぎる場合はフォントサイズを調整
                    if action_text.get_width() > button_width - 20:
                        try:
                            smaller_font = Utils.get_japanese_font(20)  # 小さいフォント
                            action_text = smaller_font.render(action, True, self.BLACK)
                        except:
                            smaller_font = pygame.font.Font(None, 20)
                            action_text = smaller_font.render(action_name_map.get(action, action), True, self.BLACK)
                    
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
                        action_name_map = {
                            "ご飯をあげる": "Feed",
                            "散歩にいく": "Walk",
                            "しつけをする": "Train",
                            "トイレを片付ける": "Clean",
                            "おもちゃで遊ぶ": "Play"
                        }
                        action_text = self.default_small_font.render(action_name_map.get(action, action), True, self.BLACK)
                    
                    # テキストが長すぎる場合はフォントサイズを調整
                    if action_text.get_width() > button_width - 20:
                        try:
                            smaller_font = Utils.get_japanese_font(20)  # 小さいフォント
                            action_text = smaller_font.render(action, True, self.BLACK)
                        except:
                            smaller_font = pygame.font.Font(None, 20)
                            action_text = smaller_font.render(action_name_map.get(action, action), True, self.BLACK)
                    
                    # テキストを中央に配置
                    self.screen.blit(action_text, (x + button_width // 2 - action_text.get_width() // 2, 
                                                y + button_height // 2 - action_text.get_height() // 2))
                    
                    # ボタンの位置を保存
                    self.action_buttons.append((x, y, button_width, button_height, action))
    
    def draw_restart_button(self):
        """再スタートボタンを描画"""
        self.action_buttons = []
        
        button_width = 240
        button_height = 60
        x = self.width // 2 - button_width // 2
        y = self.height - 100
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
        
        # ボタンの背景
        button_color = self.HOVER_COLOR if is_hover else self.GREEN
        pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=15)
        
        # ボタンの枠線 - ホバー時は太く
        border_width = 3 if is_hover else 2
        pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), border_width, border_radius=15)
        
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
        button_color = self.HOVER_COLOR if is_hover else self.ACTION_BUTTON_COLOR
        pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=self.BUTTON_RADIUS)
        
        # ボタンの枠線 - ホバー時は太く
        border_width = 2 if is_hover else 1
        pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), border_width, border_radius=self.BUTTON_RADIUS)
        
        # 戻る矢印を描画
        arrow_points = [(x + 20, y + button_height // 2), 
                        (x + 35, y + button_height // 2 - 10),
                        (x + 35, y + button_height // 2 + 10)]
        pygame.draw.polygon(self.screen, self.BLACK, arrow_points)
        
        # ボタンのテキスト
        try:
            back_text = self.normal_font.render("戻る", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            back_text = self.default_normal_font.render("Back", True, self.BLACK)
        
        self.screen.blit(back_text, (x + 45, y + button_height // 2 - back_text.get_height() // 2))
        
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
        # 背景を塗りつぶす
        self.screen.fill((240, 240, 245))  # 墓地用の薄暗い背景色
        
        # タイトル背景
        pygame.draw.rect(self.screen, (220, 220, 230), (0, 0, self.width, 80))
        pygame.draw.line(self.screen, (200, 200, 210), (0, 80), (self.width, 80), 2)
        
        # タイトル
        try:
            title = self.title_font.render("犬の墓地", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            title = self.default_title_font.render("Dog Graveyard", True, self.BLACK)
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))
        
        # 音量調整ボタンを右上に配置
        self.draw_volume_controls()
        
        if not graveyard:
            # 墓地が空の場合
            try:
                message = self.normal_font.render("まだ墓地はありません", True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                message = self.default_normal_font.render("No graves yet", True, self.BLACK)
            
            # メッセージの背景
            message_width = message.get_width() + 40
            message_height = message.get_height() + 20
            message_x = self.width // 2 - message_width // 2
            message_y = self.height // 2 - message_height // 2
            
            pygame.draw.rect(self.screen, (255, 255, 255), 
                            (message_x, message_y, message_width, message_height), 
                            border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 210), 
                            (message_x, message_y, message_width, message_height), 
                            2, border_radius=10)
            
            self.screen.blit(message, (self.width // 2 - message.get_width() // 2, self.height // 2 - message.get_height() // 2))
        else:
            # 墓石を描画
            max_per_row = 3
            for i, grave in enumerate(graveyard):
                row = i // max_per_row
                col = i % max_per_row
                
                x = self.width // 4 * (col + 1) - 50
                y = 100 + row * 180  # 間隔を狭める
                
                # 墓石の背景
                grave_bg_width = 120
                grave_bg_height = 160
                grave_bg_x = x - 10
                grave_bg_y = y - 10
                
                pygame.draw.rect(self.screen, (230, 230, 235), 
                                (grave_bg_x, grave_bg_y, grave_bg_width, grave_bg_height), 
                                border_radius=8)
                pygame.draw.rect(self.screen, (210, 210, 220), 
                                (grave_bg_x, grave_bg_y, grave_bg_width, grave_bg_height), 
                                2, border_radius=8)
                
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
                
                # テキストが長すぎる場合は小さいフォントで表示
                if dog_info.get_width() > grave_bg_width - 10:
                    try:
                        dog_info = self.tiny_font.render(f"{display_type} ({grave['growth_stage']})", True, self.BLACK)
                    except:
                        dog_info = self.default_tiny_font.render(
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
        """トレーナー画面を描画"""
        # 背景を塗りつぶす
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # タイトル背景
        pygame.draw.rect(self.screen, (240, 240, 255), (0, 0, self.width, 80))
        pygame.draw.line(self.screen, (220, 220, 240), (0, 80), (self.width, 80), 2)
        
        # タイトル
        try:
            title = self.title_font.render("トレーナー", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            title = self.default_title_font.render("Trainer Info", True, self.BLACK)
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))
        
        # 音量調整ボタンを右上に配置
        self.draw_volume_controls()
        
        # トレーナーの背景
        info_bg_width = self.width - 40
        info_bg_height = self.height - 150
        info_bg_x = 20
        info_bg_y = 100
        
        pygame.draw.rect(self.screen, (250, 250, 255), 
                        (info_bg_x, info_bg_y, info_bg_width, info_bg_height), 
                        border_radius=15)
        pygame.draw.rect(self.screen, (230, 230, 245), 
                        (info_bg_x, info_bg_y, info_bg_width, info_bg_height), 
                        2, border_radius=15)
        
        # トレーナーレベル
        try:
            level_text = self.normal_font.render(f"トレーナーレベル: {trainer_data['trainer_level']}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            level_text = self.default_normal_font.render(f"Trainer Level: {trainer_data['trainer_level']}", True, self.BLACK)
        
        self.screen.blit(level_text, (self.width // 2 - level_text.get_width() // 2, 120))
        
        # 経験値バー
        exp_bar_width = 300
        exp_bar_height = 20
        exp_bar_x = self.width // 2 - exp_bar_width // 2
        exp_bar_y = 160
        
        # 経験値の計算
        current_exp = trainer_data['trainer_exp']
        max_exp = trainer_data['trainer_level'] * 100
        exp_ratio = min(1.0, current_exp / max_exp if max_exp > 0 else 0)
        
        # 経験値バーの背景
        pygame.draw.rect(self.screen, self.GRAY, 
                        (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height), 
                        border_radius=5)
        
        # 経験値バーの進捗
        if exp_ratio > 0:
            pygame.draw.rect(self.screen, (100, 200, 255), 
                            (exp_bar_x, exp_bar_y, int(exp_bar_width * exp_ratio), exp_bar_height), 
                            border_radius=5)
        
        # 経験値バーの枠
        pygame.draw.rect(self.screen, self.BLACK, 
                        (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height), 
                        1, border_radius=5)
        
        # 経験値テキスト
        try:
            exp_text = self.small_font.render(f"経験値: {current_exp} / {max_exp}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            exp_text = self.default_small_font.render(f"EXP: {current_exp} / {max_exp}", True, self.BLACK)
        
        self.screen.blit(exp_text, (self.width // 2 - exp_text.get_width() // 2, exp_bar_y + exp_bar_height + 10))
        
        # 育てた犬の数
        dogs_raised = trainer_data["dogs_raised"]
        total_dogs = sum(dogs_raised.values())
        
        # 犬の総数の背景
        dogs_bg_width = 300
        dogs_bg_height = 40
        dogs_bg_x = self.width // 2 - dogs_bg_width // 2
        dogs_bg_y = 220
        
        pygame.draw.rect(self.screen, (245, 245, 255), 
                        (dogs_bg_x, dogs_bg_y, dogs_bg_width, dogs_bg_height), 
                        border_radius=8)
        pygame.draw.rect(self.screen, (230, 230, 245), 
                        (dogs_bg_x, dogs_bg_y, dogs_bg_width, dogs_bg_height), 
                        1, border_radius=8)
        
        try:
            dogs_text = self.normal_font.render(f"育てた犬の総数: {total_dogs}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            dogs_text = self.default_normal_font.render(f"Total Dogs Raised: {total_dogs}", True, self.BLACK)
        
        self.screen.blit(dogs_text, (self.width // 2 - dogs_text.get_width() // 2, dogs_bg_y + 5))
        
        # 犬種ごとの育成数
        y = 280
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
        
        # 死亡回数と最大成長段階の背景
        stats_bg_width = 400
        stats_bg_height = 80
        stats_bg_x = self.width // 2 - stats_bg_width // 2
        stats_bg_y = y + 10
        
        pygame.draw.rect(self.screen, (245, 245, 255), 
                        (stats_bg_x, stats_bg_y, stats_bg_width, stats_bg_height), 
                        border_radius=8)
        pygame.draw.rect(self.screen, (230, 230, 245), 
                        (stats_bg_x, stats_bg_y, stats_bg_width, stats_bg_height), 
                        1, border_radius=8)
        
        # 死亡回数
        try:
            deaths_text = self.normal_font.render(f"死亡回数: {trainer_data['total_deaths']}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            deaths_text = self.default_normal_font.render(f"Total Deaths: {trainer_data['total_deaths']}", True, self.BLACK)
        
        self.screen.blit(deaths_text, (self.width // 2 - deaths_text.get_width() // 2, stats_bg_y + 10))
        
        # 最大成長段階
        try:
            max_growth_text = self.normal_font.render(f"最大成長段階: {trainer_data['max_growth_stage']}", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            growth_names = {"子犬": "Puppy", "成犬": "Adult", "老犬": "Senior"}
            max_growth_text = self.default_normal_font.render(f"Max Growth Stage: {growth_names.get(trainer_data['max_growth_stage'], trainer_data['max_growth_stage'])}", True, self.BLACK)
        
        self.screen.blit(max_growth_text, (self.width // 2 - max_growth_text.get_width() // 2, stats_bg_y + 45))
        
        # トレーナーボーナス
        bonuses = trainer_data["bonuses"]
        
        # ボーナスのタイトル背景
        bonus_title_bg_width = 300
        bonus_title_bg_height = 40
        bonus_title_bg_x = self.width // 2 - bonus_title_bg_width // 2
        bonus_title_bg_y = stats_bg_y + stats_bg_height + 20
        
        pygame.draw.rect(self.screen, (240, 240, 255), 
                        (bonus_title_bg_x, bonus_title_bg_y, bonus_title_bg_width, bonus_title_bg_height), 
                        border_radius=8)
        pygame.draw.rect(self.screen, (220, 220, 240), 
                        (bonus_title_bg_x, bonus_title_bg_y, bonus_title_bg_width, bonus_title_bg_height), 
                        2, border_radius=8)
        
        try:
            bonus_text = self.normal_font.render("トレーナーボーナス", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            bonus_text = self.default_normal_font.render("Trainer Bonuses", True, self.BLACK)
        
        self.screen.blit(bonus_text, (self.width // 2 - bonus_text.get_width() // 2, bonus_title_bg_y + 5))
        
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
        
        # ボーナス項目の背景
        bonus_bg_width = self.width - 80
        bonus_bg_height = 120
        bonus_bg_x = 40
        bonus_bg_y = bonus_title_bg_y + bonus_title_bg_height + 10
        
        pygame.draw.rect(self.screen, (250, 250, 255), 
                        (bonus_bg_x, bonus_bg_y, bonus_bg_width, bonus_bg_height), 
                        border_radius=8)
        pygame.draw.rect(self.screen, (230, 230, 245), 
                        (bonus_bg_x, bonus_bg_y, bonus_bg_width, bonus_bg_height), 
                        1, border_radius=8)
        
        # 1列目
        bonus_y = bonus_bg_y + 20
        col1_x = self.width // 4
        for bonus_name, bonus_value in col1_items:
            jp_name, en_name = name_map.get(bonus_name, (bonus_name, bonus_name))
            try:
                bonus_item_text = self.small_font.render(f"{jp_name}: x{bonus_value:.2f}", True, self.BLACK)
            except:
                bonus_item_text = self.default_small_font.render(f"{en_name}: x{bonus_value:.2f}", True, self.BLACK)
            
            self.screen.blit(bonus_item_text, (col1_x - bonus_item_text.get_width() // 2, bonus_y))
            bonus_y += 30
        
        # 2列目
        bonus_y = bonus_bg_y + 20
        col2_x = self.width * 3 // 4
        for bonus_name, bonus_value in col2_items:
            jp_name, en_name = name_map.get(bonus_name, (bonus_name, bonus_name))
            try:
                bonus_item_text = self.small_font.render(f"{jp_name}: x{bonus_value:.2f}", True, self.BLACK)
            except:
                bonus_item_text = self.default_small_font.render(f"{en_name}: x{bonus_value:.2f}", True, self.BLACK)
            
            self.screen.blit(bonus_item_text, (col2_x - bonus_item_text.get_width() // 2, bonus_y))
            bonus_y += 30
        
        # 戻るボタン
        self.draw_back_button()
    def handle_key_event(self, event, dog):
        """キーボードイベント処理: dキーで犬を死亡させる"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                dog.is_alive = False
    
    def draw_demo_buttons(self, dog):
        pass
    
    def draw_volume_controls(self):
        """音量調整ボタンを描画"""
        # 音量調整ボタンを右上に配置
        button_width = 160
        button_height = 40
        x = self.width - button_width - 20
        y = 20
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        
        # ボタンの背景
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, (x, y, button_width, button_height), border_radius=self.BUTTON_RADIUS)
        pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), 1, border_radius=self.BUTTON_RADIUS)
        
        # 音量ラベル
        try:
            volume_text = self.small_font.render("音量:", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            volume_text = self.default_small_font.render("Volume:", True, self.BLACK)
        
        self.screen.blit(volume_text, (x + 10, y + button_height // 2 - volume_text.get_height() // 2))
        
        # 音量バー
        bar_width = 70
        bar_height = 10
        bar_x = x + 60
        bar_y = y + button_height // 2 - bar_height // 2
        
       
        
        # バーの背景
        pygame.draw.rect(self.screen, self.GRAY, (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        
        # 現在の音量を表示
        volume_width = int(bar_width * self.volume)
        pygame.draw.rect(self.screen, self.GREEN, (bar_x, bar_y, volume_width, bar_height), border_radius=5)
        
        # バーの枠
        pygame.draw.rect(self.screen, self.BLACK, (bar_x, bar_y, bar_width, bar_height), 1, border_radius=5)
        
        # 音量調整ボタン（- と +）
        minus_x = bar_x - 20
        minus_y = bar_y - 5
        plus_x = bar_x + bar_width + 5
        plus_y = bar_y - 5
        button_size = 20
        
        # マイナスボタン
        is_minus_hover = minus_x <= mouse_pos[0] <= minus_x + button_size and minus_y <= mouse_pos[1] <= minus_y + button_size
        minus_color = self.HOVER_COLOR if is_minus_hover else self.YELLOW
        pygame.draw.rect(self.screen, minus_color, (minus_x, minus_y, button_size, button_size), border_radius=5)
        pygame.draw.rect(self.screen, self.BLACK, (minus_x, minus_y, button_size, button_size), 1, border_radius=5)
        pygame.draw.line(self.screen, self.BLACK, (minus_x + 5, minus_y + button_size // 2), (minus_x + button_size - 5, minus_y + button_size // 2), 2)
        
        # プラスボタン
        is_plus_hover = plus_x <= mouse_pos[0] <= plus_x + button_size and plus_y <= mouse_pos[1] <= plus_y + button_size
        plus_color = self.HOVER_COLOR if is_plus_hover else self.YELLOW
        pygame.draw.rect(self.screen, plus_color, (plus_x, plus_y, button_size, button_size), border_radius=5)
        pygame.draw.rect(self.screen, self.BLACK, (plus_x, plus_y, button_size, button_size), 1, border_radius=5)
        pygame.draw.line(self.screen, self.BLACK, (plus_x + 5, plus_y + button_size // 2), (plus_x + button_size - 5, plus_y + button_size // 2), 2)
        pygame.draw.line(self.screen, self.BLACK, (plus_x + button_size // 2, plus_y + 5), (plus_x + button_size // 2, plus_y + button_size - 5), 2)
        
        # ボタンの位置を保存
        self.action_buttons.append((minus_x, minus_y, button_size, button_size, "volume_down"))
        self.action_buttons.append((plus_x, plus_y, button_size, button_size, "volume_up"))
    
    def update_volume(self, change):
        """音量を更新"""
        self.volume = max(0.0, min(1.0, self.volume + change))
        return self.volume
    def draw_dog_management(self, dogs):
        """犬管理画面を描画"""
        # 背景を塗りつぶす
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # タイトル背景
        pygame.draw.rect(self.screen, (240, 240, 255), (0, 0, self.width, 80))
        pygame.draw.line(self.screen, (220, 220, 240), (0, 80), (self.width, 80), 2)
        
        # タイトル
        try:
            title = self.title_font.render("飼っている犬", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            title = self.default_title_font.render("Your Dogs", True, self.BLACK)
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))
        
        # 音量調整ボタンを右上に配置
        self.draw_volume_controls()
        
        if not dogs:
            # 犬がいない場合
            try:
                message = self.normal_font.render("まだ犬を飼っていません", True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                message = self.default_normal_font.render("You don't have any dogs yet", True, self.BLACK)
            
            # メッセージの背景
            message_width = message.get_width() + 40
            message_height = message.get_height() + 20
            message_x = self.width // 2 - message_width // 2
            message_y = self.height // 2 - message_height // 2
            
            pygame.draw.rect(self.screen, (255, 255, 255), 
                            (message_x, message_y, message_width, message_height), 
                            border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 210), 
                            (message_x, message_y, message_width, message_height), 
                            2, border_radius=10)
            
            self.screen.blit(message, (self.width // 2 - message.get_width() // 2, self.height // 2 - message.get_height() // 2))
        else:
            # 犬のリストを表示
            self.draw_dog_list(dogs)
        
        # 新しい犬を追加するボタン
        self.draw_add_dog_button()
        
        # メニューボタン
        self.draw_menu_buttons(["墓地を見る", "トレーナー"])
    
    def draw_dog_list(self, dogs):
        """犬のリストを描画"""
        self.dog_buttons = []  # 犬ボタンのリストをクリア
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        
        # 犬カードのサイズと配置
        card_width = 220
        card_height = 180
        margin_x = 30
        margin_y = 20
        cards_per_row = 3
        
        # スクロール可能な領域を作成
        list_area_y = 100
        list_area_height = self.height - list_area_y - 80  # 下部のボタン用にスペースを確保
        
        for i, dog in enumerate(dogs):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = margin_x + col * (card_width + margin_x)
            y = list_area_y + row * (card_height + margin_y)
            
            # ホバー効果の判定
            is_hover = x <= mouse_pos[0] <= x + card_width and y <= mouse_pos[1] <= y + card_height
            
            # カードの背景
            card_color = self.HOVER_COLOR if is_hover else self.BUTTON_COLOR
            pygame.draw.rect(self.screen, card_color, (x, y, card_width, card_height), border_radius=10)
            
            # カードの枠線 - ホバー時は太く
            border_width = 3 if is_hover else 2
            border_color = (100, 200, 100) if dog.is_alive else (200, 100, 100)
            pygame.draw.rect(self.screen, border_color, (x, y, card_width, card_height), border_width, border_radius=10)
            
            # 犬の画像
            try:
                if dog.dog_type == "コーギー":
                    dog_img = pygame.image.load(os.path.join("dog_inubiyori", "assets", "dogs", "corgi.png"))
                elif dog.dog_type == "ミニチュアダックスフンド":
                    dog_img = pygame.image.load(os.path.join("dog_inubiyori", "assets", "dogs", "dachsuhund.png"))
                elif dog.dog_type == "柴犬":
                    dog_img = pygame.image.load(os.path.join("dog_inubiyori", "assets", "dogs", "shiba.png"))
                else:
                    # 未知の犬種の場合はプレースホルダーを使用
                    dog_img = self.placeholder_images[dog.dog_type]["small"]
                
                # 画像サイズを調整
                dog_img = pygame.transform.scale(dog_img, (80, 80))
                self.screen.blit(dog_img, (x + 20, y + 20))
            except Exception as e:
                # エラーが発生した場合はプレースホルダーを使用
                self.screen.blit(self.placeholder_images[dog.dog_type]["small"], (x + 20, y + 20))
            
            # 犬の名前
            try:
                name = self.normal_font.render(dog.name, True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                name = self.default_normal_font.render(dog.name, True, self.BLACK)
            
            # 名前が長すぎる場合は小さいフォントで表示
            if name.get_width() > card_width - 120:
                try:
                    name = self.small_font.render(dog.name, True, self.BLACK)
                except:
                    name = self.default_small_font.render(dog.name, True, self.BLACK)
            
            self.screen.blit(name, (x + 120, y + 30))
            
            # 犬種
            display_type = "ダックス" if dog.dog_type == "ミニチュアダックスフンド" else dog.dog_type
            try:
                dog_type = self.small_font.render(display_type, True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                dog_names = {"コーギー": "Corgi", "ミニチュアダックスフンド": "Dachshund", "柴犬": "Shiba"}
                dog_type = self.default_small_font.render(dog_names.get(dog.dog_type, dog.dog_type), True, self.BLACK)
            
            self.screen.blit(dog_type, (x + 120, y + 60))
            
            # 成長段階
            try:
                growth = self.small_font.render(f"成長: {dog.growth_stage}", True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                growth_names = {"子犬": "Puppy", "成犬": "Adult", "老犬": "Senior"}
                growth = self.default_small_font.render(f"Growth: {growth_names.get(dog.growth_stage, dog.growth_stage)}", True, self.BLACK)
            
            self.screen.blit(growth, (x + 120, y + 90))
            
            # 生存日数
            try:
                days = self.small_font.render(f"{int(dog.lifespan_days)}日", True, self.BLACK)
            except:
                # フォールバック: 英語で表示
                days = self.default_small_font.render(f"{int(dog.lifespan_days)} days", True, self.BLACK)
            
            self.screen.blit(days, (x + 120, y + 120))
            
            # 状態表示
            status_color = (100, 200, 100) if dog.is_alive else (200, 100, 100)
            status_text = dog.get_mood() if dog.is_alive else "死亡"
            try:
                status = self.small_font.render(status_text, True, status_color)
            except:
                # フォールバック: 英語で表示
                status_names = {
                    "とても幸せ": "Very Happy", 
                    "幸せ": "Happy", 
                    "普通": "Normal", 
                    "不満": "Unsatisfied", 
                    "不機嫌": "Grumpy", 
                    "病気": "Sick",
                    "死亡": "Dead"
                }
                status = self.default_small_font.render(status_names.get(status_text, status_text), True, status_color)
            
            # 状態の背景
            status_bg_width = status.get_width() + 10
            status_bg_height = status.get_height() + 6
            status_bg_x = x + card_width - status_bg_width - 10
            status_bg_y = y + 10
            
            pygame.draw.rect(self.screen, (255, 255, 255, 180), 
                            (status_bg_x, status_bg_y, status_bg_width, status_bg_height), 
                            border_radius=5)
            pygame.draw.rect(self.screen, status_color, 
                            (status_bg_x, status_bg_y, status_bg_width, status_bg_height), 
                            1, border_radius=5)
            
            self.screen.blit(status, (status_bg_x + 5, status_bg_y + 3))
            
            # ボタンの位置を保存
            self.dog_buttons.append((x, y, card_width, card_height, dog.id))
    
    def draw_add_dog_button(self):
        """新しい犬を追加するボタンを描画"""
        button_width = 300
        button_height = 50
        x = self.width // 2 - button_width // 2
        y = self.height - button_height - 20
        
        # マウス位置を取得してホバー効果を適用
        mouse_pos = pygame.mouse.get_pos()
        is_hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
        
        # ボタンの背景
        button_color = self.HOVER_COLOR if is_hover else self.GREEN
        pygame.draw.rect(self.screen, button_color, (x, y, button_width, button_height), border_radius=10)
        
        # ボタンの枠線 - ホバー時は太く
        border_width = 3 if is_hover else 2
        pygame.draw.rect(self.screen, self.BLACK, (x, y, button_width, button_height), border_width, border_radius=10)
        
        # ボタンのテキスト
        try:
            button_text = self.normal_font.render("新しい犬を追加", True, self.BLACK)
        except:
            # フォールバック: 英語で表示
            button_text = self.default_normal_font.render("Add New Dog", True, self.BLACK)
        
        self.screen.blit(button_text, (x + button_width // 2 - button_text.get_width() // 2, 
                                      y + button_height // 2 - button_text.get_height() // 2))
        
        # ボタンの位置を保存
        self.action_buttons.append((x, y, button_width, button_height, "add_dog"))
    
    def check_dog_selection_from_list(self, mouse_pos):
        """犬リストからの選択をチェック"""
        for x, y, width, height, dog_id in self.dog_buttons:
            if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
                return dog_id
        
        return None
