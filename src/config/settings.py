"""設定管理モジュール"""
import json
import os
from pathlib import Path


class Settings:
    """アプリケーション設定を管理するクラス"""

    # デフォルトサブタスク一覧
    DEFAULT_SUBTASKS = [
        "図面チェック",
        "成果品策定",
        "電話対応",
        "メール対応",
        "打ち合わせ",
        "資料作成",
        "その他"
    ]

    # デフォルトフォントサイズ
    DEFAULT_FONT_SIZE = 10

    # ウィンドウ設定
    WINDOW_WIDTH = 180
    WINDOW_HEIGHT = 420
    WINDOW_TITLE = "タスク記録"

    # カラー設定（ダークモード）
    COLORS = {
        "bg_primary": "#1a1a2e",
        "bg_secondary": "#16213e",
        "bg_tertiary": "#0f3460",
        "accent": "#e94560",
        "accent_hover": "#ff6b6b",
        "text_primary": "#ffffff",
        "text_secondary": "#a0a0a0",
        "success": "#4ecca3",
        "warning": "#ffc107"
    }

    def __init__(self):
        self.config_dir = Path.home() / "Documents" / "TaskTimestamp"
        self.config_file = self.config_dir / "config.json"
        self.output_folder = self.config_dir
        self.subtasks = self.DEFAULT_SUBTASKS.copy()
        self.font_size = self.DEFAULT_FONT_SIZE
        self.window_x = None
        self.window_y = None
        self._load()
        self._create_default_config_if_not_exists()

    def _load(self):
        """設定をファイルから読み込む"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.output_folder = Path(data.get(
                        'output_folder', str(self.config_dir)))
                    self.subtasks = data.get('subtasks', self.DEFAULT_SUBTASKS)
                    self.font_size = data.get('font_size', self.DEFAULT_FONT_SIZE)
                    self.window_x = data.get('window_x')
                    self.window_y = data.get('window_y')
            except (json.JSONDecodeError, IOError):
                pass

    def _create_default_config_if_not_exists(self):
        """デフォルト設定ファイルを作成"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        if not self.config_file.exists():
            self.save()

    def reload(self):
        """設定を再読み込み"""
        self._load()

    def save(self):
        """設定をファイルに保存する"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        data = {
            'output_folder': str(self.output_folder),
            'subtasks': self.subtasks,
            'font_size': self.font_size,
            'window_x': self.window_x,
            'window_y': self.window_y
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # フォントプロパティ（font_sizeに基づいて動的生成）
    @property
    def FONT_LARGE(self):
        return ("Yu Gothic UI", self.font_size, "bold")

    @property
    def FONT_MEDIUM(self):
        return ("Yu Gothic UI", max(self.font_size - 2, 7))

    @property
    def FONT_SMALL(self):
        return ("Yu Gothic UI", max(self.font_size - 3, 6))

    @property
    def FONT_CLOCK(self):
        return ("Yu Gothic UI", self.font_size + 4, "bold")

    @property
    def FONT_BUTTON(self):
        return ("Yu Gothic UI", max(self.font_size - 2, 7), "bold")

    def get_username(self) -> str:
        """環境変数からユーザ名を取得"""
        return os.environ.get('USERNAME', os.environ.get('USER', 'unknown'))

    def set_output_folder(self, path: str):
        """出力フォルダを設定する"""
        self.output_folder = Path(path)
        self.save()

    def set_font_size(self, size: int):
        """フォントサイズを設定する"""
        self.font_size = max(6, min(20, size))
        self.save()

    def set_window_position(self, x: int, y: int):
        """ウィンドウ位置を記憶する"""
        self.window_x = x
        self.window_y = y
        self.save()


# シングルトンインスタンス
settings = Settings()
