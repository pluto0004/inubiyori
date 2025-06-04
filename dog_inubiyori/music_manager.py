import pygame
import os
import pathlib

class MusicManager:
    def __init__(self):
        """音楽マネージャーの初期化"""
        # 音楽の初期化 - 明示的なパラメータを使用
        self.audio_initialized = False
        try:
            # 一般的なサンプルレート、ビット深度、チャンネル数を明示的に指定
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
            # 初期化が成功したかどうか確認
            if pygame.mixer.get_init() is not None:
                self.audio_initialized = True
                print("Pygame audio system successfully initialized")
                print(f"Pygame version: {pygame.version.ver}")
                print(f"SDL version: {pygame.version.SDL}")
                print(f"Audio driver: {pygame.mixer.get_init()}")
                print(f"Available audio drivers: {pygame.mixer.get_sdl_mixer_version()}")
            else:
                print("WARNING: Pygame audio system failed to initialize")
        except Exception as e:
            print(f"ERROR: Failed to initialize audio system: {e}")
        
        # 音楽ファイルのパス
        # スクリプトの場所を基準に絶対パスを設定
        # dog_inubiyori/assets/music ディレクトリを参照
        script_dir = pathlib.Path(__file__).parent.absolute()
        self.music_dir = os.path.join(script_dir, "assets", "music")
        
        # ディレクトリの存在チェック
        if os.path.exists(self.music_dir):
            print(f"Music directory found: {self.music_dir}")
            
            # ディレクトリアクセス権限チェック
            if os.access(self.music_dir, os.R_OK):
                print(f"Music directory is readable")
            else:
                print(f"WARNING: No read permission for music directory {self.music_dir}")
        else:
            print(f"ERROR: Music directory does not exist: {self.music_dir}")
            print(f"Current working directory: {os.getcwd()}")
        
        # 音楽ファイル名（MP3とWAVの両方をサポート、WAVを優先）
        self.music_files = {
            "opening": ["opening.wav", "opening.mp3"],
            "game": ["game.wav", "game.mp3"],
            "funeral": ["funeral.wav", "funeral.mp3"]
        }
        
        # デバッグ情報を表示：音楽ディレクトリパスの確認
        print(f"Music directory path: {self.music_dir}")
        for music_type, filenames in self.music_files.items():
            for filename in filenames:
                full_path = os.path.join(self.music_dir, filename)
                exists = os.path.exists(full_path)
                readable = os.access(full_path, os.R_OK) if exists else False
                size = os.path.getsize(full_path) if exists else 0
                print(f"Checking {music_type} file: {full_path}")
                print(f"  - Exists: {exists}")
                print(f"  - Readable: {readable}")
                print(f"  - Size: {size} bytes")
        
        # 現在再生中の音楽
        self.current_music = None
        
        # 音量設定
        self.volume = 0.5  # 0.0 ~ 1.0
        if self.audio_initialized:
            pygame.mixer.music.set_volume(self.volume)
    
    def play_music(self, music_type):
        """指定された種類の音楽を再生"""
        # オーディオシステムが初期化されていない場合は何もしない
        if not self.audio_initialized:
            print("Cannot play music: Audio system not initialized")
            return False
            
        if music_type not in self.music_files:
            print(f"Unknown music type: {music_type}")
            return False
        
        # 同じ音楽が既に再生中なら何もしない
        if self.current_music == music_type:
            return True
        
        # 音楽ファイルのパスを試す（MP3とWAVの両方）
        music_loaded = False
        
        # デバッグ情報: 音楽ディレクトリのファイル一覧を表示
        if os.path.exists(self.music_dir):
            print(f"Files in music directory {self.music_dir}:")
            try:
                for f in os.listdir(self.music_dir):
                    file_path = os.path.join(self.music_dir, f)
                    size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                    readable = os.access(file_path, os.R_OK)
                    print(f"  - {f} (Size: {size} bytes, Readable: {readable})")
            except Exception as e:
                print(f"Error listing directory: {e}")
        else:
            print(f"Music directory does not exist: {self.music_dir}")
            print(f"Attempting to create directory: {self.music_dir}")
            try:
                os.makedirs(self.music_dir, exist_ok=True)
                print(f"Directory created: {self.music_dir}")
            except Exception as e:
                print(f"Failed to create directory: {e}")
            
        for file_name in self.music_files[music_type]:
            music_path = os.path.join(self.music_dir, file_name)
            
            # ファイルが存在するか確認
            print(f"Trying to load music: {music_path}")
            if os.path.exists(music_path):
                try:
                    # 現在の音楽を停止
                    pygame.mixer.music.stop()
                    
                    # 新しい音楽をロード
                    print(f"Loading music file: {music_path}")
                    pygame.mixer.music.load(music_path)
                    
                    # 音楽を再生（ループ再生）
                    pygame.mixer.music.play(-1)
                    
                    # 現在の音楽を更新
                    self.current_music = music_type
                    
                    music_loaded = True
                    print(f"Playing music: {music_path}")
                    break
                except Exception as e:
                    print(f"Error loading music {music_path}: {e}")
                    if os.path.exists(music_path):
                        print(f"File size: {os.path.getsize(music_path)} bytes")
                        print(f"File permissions: {oct(os.stat(music_path).st_mode)}")
                        print(f"File readable: {os.access(music_path, os.R_OK)}")
                    else:
                        print(f"File does not exist: {music_path}")
        
        if not music_loaded:
            print(f"No valid music file found for {music_type}")
            return False
        
        return True
    
    def stop_music(self):
        """音楽を停止"""
        if self.audio_initialized:
            pygame.mixer.music.stop()
        self.current_music = None
    
    def set_volume(self, volume):
        """音量を設定（0.0 ~ 1.0）"""
        self.volume = max(0.0, min(1.0, volume))
        if self.audio_initialized:
            pygame.mixer.music.set_volume(self.volume)
    
    def get_volume(self):
        """現在の音量を取得"""
        return self.volume
