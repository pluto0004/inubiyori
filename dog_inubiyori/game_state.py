import time
from utils import SaveManager
from dog import Dog

class GameState:
    def __init__(self):
        self.dog = None  # 現在選択されている犬
        self.game_started = False
        self.last_update_time = 0
        self.message = "犬を選んでください"
        self.actions = ["ご飯をあげる", "散歩にいく", "しつけをする", "トイレを片付ける", "おもちゃで遊ぶ"]
        self.message_timeout = 0
        
        # セーブマネージャーの初期化
        self.save_manager = SaveManager()
        
        # トレーナーデータの読み込み
        self.trainer_data = self.save_manager.trainer_data
        
        # 現在飼っている犬のリスト
        self.dogs = []
        self.load_all_dogs()
        
        # ゲームの状態
        if len(self.dogs) > 0:
            self.state = "dog_management"  # 犬がいる場合は犬管理画面から開始
        else:
            self.state = "select_dog"  # 犬がいない場合は犬選択画面から開始
    
    def load_all_dogs(self):
        """すべての犬をロード"""
        self.dogs = []
        for dog_data in self.save_manager.current_dogs:
            dog = Dog(dog_data["dog_type"], dog_data["name"], dog_data)
            self.dogs.append(dog)
    
    def start_game(self, dog):
        """ゲームを開始する（新しい犬を追加）"""
        # 犬を保存して一意のIDを取得
        dog_id = self.save_manager.save_dog(dog.to_dict())
        dog.id = dog_id
        
        # 犬リストに追加
        self.dogs.append(dog)
        
        # 現在の犬として設定
        self.dog = dog
        self.game_started = True
        self.last_update_time = time.time()
        self.message = f"{dog.dog_type}を選びました！名前は{dog.name}です。"
        self.message_timeout = time.time() + 3  # メッセージを3秒間表示
        self.state = "main_game"  # 状態を明示的に設定
    
    def select_dog(self, dog_id):
        """既存の犬を選択"""
        for dog in self.dogs:
            if dog.id == dog_id:
                self.dog = dog
                self.game_started = True
                self.last_update_time = time.time()
                self.message = f"{dog.name}のお世話を始めます！"
                self.message_timeout = time.time() + 3
                self.state = "main_game"
                break
    
    def update(self):
        """ゲームの状態を更新する"""
        # すべての犬を更新
        for dog in self.dogs:
            if dog.is_alive:
                dog.update_status()
                
                # 犬が死亡した場合
                if not dog.is_alive:
                    self.handle_dog_death(dog)
                else:
                    # 生きている犬は保存
                    self.save_manager.save_dog(dog.to_dict())
        
        current_time = time.time()
        
        # 現在選択中の犬がいる場合
        if self.dog:
            # メッセージのタイムアウトをチェック
            if self.message_timeout > 0 and current_time > self.message_timeout:
                if self.dog.is_alive:
                    self.message = f"{self.dog.name}は{self.dog.get_mood()}な様子..."
                else:
                    self.message = f"{self.dog.name}はもういない..."
                self.message_timeout = 0
    
    def perform_action(self, action):
        """アクションを実行する"""
        if not self.game_started or self.dog is None or not self.dog.is_alive:
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
                self.handle_dog_death(self.dog)
            
            # 犬のデータを保存
            if self.dog.is_alive:
                self.save_manager.save_dog(self.dog.to_dict())
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
        
        # 犬のデータを保存
        self.save_manager.save_dog(self.dog.to_dict())
    
    def handle_dog_death(self, dog):
        """犬の死亡を処理する"""
        # 墓地に追加
        self.save_manager.add_to_graveyard(dog)
        
        # 犬リストから削除
        self.dogs = [d for d in self.dogs if d.id != dog.id]
        
        # 現在選択中の犬が死亡した場合
        if self.dog and self.dog.id == dog.id:
            # メッセージを設定
            self.message = f"{dog.name}は永遠の眠りについた..."
            self.message_timeout = time.time() + 5
    
    def add_new_dog(self):
        """新しい犬を追加するモードに移行"""
        self.state = "select_dog"
    
    def show_dog_management(self):
        """犬管理画面を表示"""
        self.state = "dog_management"
    
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
            if len(self.dogs) > 0:
                self.state = "dog_management"
            else:
                self.state = "select_dog"
