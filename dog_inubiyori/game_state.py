import time
from utils import SaveManager

class GameState:
    def __init__(self):
        self.dog = None
        self.game_started = False
        self.last_update_time = 0
        self.message = "犬を選んでください"
        self.actions = ["ご飯をあげる", "散歩にいく", "しつけをする", "トイレを片付ける", "おもちゃで遊ぶ"]
        self.message_timeout = 0
        
        # セーブマネージャーの初期化
        self.save_manager = SaveManager()
        
        # トレーナーデータの読み込み
        self.trainer_data = self.save_manager.trainer_data
        
        # 現在のゲームデータの読み込み
        self.load_current_game()
        
        # ゲームの状態
        self.state = "select_dog"  # "select_dog", "main_game", "graveyard", "trainer_info"
    
    def load_current_game(self):
        """現在のゲームデータをロード"""
        saved_game = self.save_manager.load_current_game()
        if saved_game:
            from dog import Dog
            self.dog = Dog(saved_game["dog_type"], saved_game["name"], saved_game)
            self.game_started = True
            self.last_update_time = time.time()
            self.message = f"{self.dog.name}が戻ってきた！"
            self.message_timeout = time.time() + 3
            self.state = "main_game"
    
    def start_game(self, dog):
        """ゲームを開始する"""
        self.dog = dog
        self.game_started = True
        self.last_update_time = time.time()
        self.message = f"{dog.dog_type}を選びました！名前は{dog.name}です。"
        self.message_timeout = time.time() + 3  # メッセージを3秒間表示
        self.state = "main_game"  # 状態を明示的に設定
        
        # ゲームデータを保存
        self.save_current_game()
    
    def update(self):
        """ゲームの状態を更新する"""
        if not self.game_started or self.dog is None:
            return
        
        current_time = time.time()
        
        # 犬のステータスを更新
        self.dog.update_status()
        self.last_update_time = current_time
        
        # 犬が死亡した場合
        if not self.dog.is_alive:
            self.handle_dog_death()
        
        # メッセージのタイムアウトをチェック
        if self.message_timeout > 0 and current_time > self.message_timeout:
            if self.dog.is_alive:
                self.message = f"{self.dog.name}は{self.dog.get_mood()}な様子..."
            else:
                self.message = f"{self.dog.name}はもういない..."
            self.message_timeout = 0
        
        # ゲームデータを保存
        self.save_current_game()
    
    def perform_action(self, action):
        """アクションを実行する"""
        if not self.game_started or self.dog is None:
            return
        
        # トレーナーボーナスを取得
        trainer_bonuses = self.save_manager.get_trainer_bonuses()
        
        # デモ用アクションの処理
        if action.startswith("demo_"):
            demo_action = action.replace("demo_", "")
            if demo_action == "grow":
                self.message = self.dog.demo_grow()
            elif demo_action == "make_sick":
                self.message = self.dog.demo_make_sick()
            elif demo_action == "kill":
                self.message = self.dog.demo_kill()
                # 死亡処理
                self.handle_dog_death()
            return
        
        # 通常のアクション処理
        if action == "ご飯をあげる":
            self.message = self.dog.feed(trainer_bonuses)
        elif action == "散歩にいく":
            self.message = self.dog.walk(trainer_bonuses)
        elif action == "しつけをする":
            self.message = self.dog.train(trainer_bonuses)
        elif action == "トイレを片付ける":
            self.message = self.dog.clean(trainer_bonuses)
        elif action == "おもちゃで遊ぶ":
            self.message = self.dog.play(trainer_bonuses)
        
        self.message_timeout = time.time() + 3  # メッセージを3秒間表示
        
        # ゲームデータを保存
        self.save_current_game()
    
    def handle_dog_death(self):
        """犬の死亡を処理する"""
        if hasattr(self, "death_handled") and self.death_handled:
            return
        
        # 墓地に追加
        self.save_manager.add_to_graveyard(self.dog)
        
        # 現在のゲームデータを削除
        self.save_manager.delete_current_game()
        
        # メッセージを設定
        self.message = f"{self.dog.name}は永遠の眠りについた..."
        self.message_timeout = time.time() + 5
        
        # 死亡処理済みフラグを設定
        self.death_handled = True
    
    def save_current_game(self):
        """現在のゲームデータを保存"""
        if self.dog and self.dog.is_alive:
            self.save_manager.save_current_game(self.dog.to_dict())
    
    def restart_game(self):
        """ゲームを再スタート"""
        self.dog = None
        self.game_started = False
        self.message = "犬を選んでください"
        self.state = "select_dog"
        self.death_handled = False
    
    def show_graveyard(self):
        """墓地を表示"""
        self.state = "graveyard"
    
    def show_trainer_info(self):
        """トレーナー情報を表示"""
        self.state = "trainer_info"
    
    def back_to_main(self):
        """メイン画面に戻る"""
        if self.dog and self.dog.is_alive:
            self.state = "main_game"
        else:
            self.state = "select_dog"
