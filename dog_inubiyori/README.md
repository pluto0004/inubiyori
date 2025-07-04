犬の育成ゲームです。

## 機能
- 3 種類の犬（コーギー、ミニチュアダックスフンド、柴犬）から選択可能
- 5 つのお世話アクション：
  - ご飯をあげる
  - 散歩にいく
  - しつけをする
  - トイレを片付ける
  - おもちゃで遊ぶ
- 犬のステータス管理（満腹度、幸福度、しつけ度、清潔度、元気度、健康度）
- 犬の成長システム（子犬 → 成犬 → 老犬）
- 犬の死亡システム（健康度が 0 になるか、病気の日数が 5 日を超えると死亡）
- 墓地システム（死亡した犬の記録）
- トレーナーレベルシステム（経験値を獲得してレベルアップ）
- トレーナーボーナス（レベルアップによるお世話効果の向上）
- 日本語フォント対応（Windows/macOS）
- 可愛らしい犬のアニメーション（瞬き、尻尾を振る、歩くなど）
- ローカルセーブ機能

## 必要条件

- Python 3.x
- Pygame

## インストール方法

1. Python をインストールします（まだの場合）
2. Pygame をインストールします：
   ```
   pip install pygame
   ```
3. このリポジトリをクローンまたはダウンロードします

## 実行方法

```
python main.py
```

## プロジェクト構造

- `main.py` - メインゲームループとアプリケーションの起動点
- `dog.py` - 犬のクラスと関連機能
- `game_state.py` - ゲームの状態管理
- `ui.py` - ユーザーインターフェース関連の機能
- `animation.py` - 犬のアニメーション管理
- `utils.py` - ユーティリティ関数とセーブデータ管理
- `assets/` - 画像などのアセットを格納するディレクトリ
- `saves/` - セーブデータを格納するディレクトリ

## ゲームの流れ

1. 3 種類の犬から 1 匹を選択
2. 犬のお世話をする（ご飯をあげる、散歩にいく、しつけをする、トイレを片付ける、おもちゃで遊ぶ）
3. 犬のステータスを管理し、健康を維持する
4. 適切にお世話を続けると、犬は成長する（子犬 → 成犬 → 老犬）
5. お世話を怠ると、犬は病気になり、最終的に死亡する
6. 犬が死亡すると、墓地に記録され、新しい犬を選べるようになる
7. 犬の育成を通じてトレーナー経験値を獲得し、レベルアップする
8. レベルアップによりお世話の効果が向上する

## 拡張の可能性

- 実際の犬の画像の追加
- より多くの犬種の追加
- ミニゲームの追加
- 犬の名前変更機能
- より複雑な成長システム
- 犬の病気や特殊イベントの追加
- マルチプレイヤー機能

## ライセンス

このプロジェクトはオープンソースです。
