"""タスクタイムスタンプ記録アプリ - メインエントリーポイント"""
import sys
from pathlib import Path

# srcディレクトリをパスに追加（exe化時の対応）
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
    DATA_DIR = Path(sys.executable).parent / "data"
else:
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR.parent / "data"

import tkinter as tk

from config.settings import settings, Settings
from services.task_manager import TaskManager
from services.csv_writer import CSVWriter
from ui.main_window import MainWindow
from ui.subtask_window import SubtaskWindow
from ui.timer_window import TimerWindow
from ui.settings_window import SettingsWindow


class TaskTimestampApp:
    """メインアプリケーションクラス"""

    def __init__(self):
        self.root = tk.Tk()
        self.settings = settings
        self._setup_window()
        self._init_services()
        self._show_main_window()

        self._drag_start_x = 0
        self._drag_start_y = 0

        self.root.bind('<Button-1>', self._on_drag_start)
        self.root.bind('<B1-Motion>', self._on_drag_motion)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_window(self):
        """ウィンドウの初期設定"""
        self.root.title(Settings.WINDOW_TITLE)
        self.root.geometry(f"{Settings.WINDOW_WIDTH}x{Settings.WINDOW_HEIGHT}")
        self.root.configure(bg=Settings.COLORS["bg_primary"])
        self.root.attributes('-topmost', True)

        if self.settings.window_x is not None:
            self.root.geometry(
                f"+{self.settings.window_x}+{self.settings.window_y}"
            )

        self.root.minsize(150, 350)

    def _init_services(self):
        """サービスの初期化"""
        json_path = DATA_DIR / "main_tasks.json"
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        self.task_manager = TaskManager(json_path)
        self.csv_writer = CSVWriter(self.settings.output_folder)

        self.current_main_task = None
        self.current_sub_task = None
        self.current_frame = None

    def _clear_frame(self):
        """現在のフレームをクリア"""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def _show_main_window(self):
        """メインタスク一覧画面を表示"""
        self._clear_frame()
        self.current_main_task = None
        self.current_sub_task = None

        self.current_frame = MainWindow(
            self.root,
            self.task_manager,
            self.settings,
            on_task_select=self._on_main_task_select,
            on_settings=self._show_settings_window
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def _on_main_task_select(self, task_name: str):
        """メインタスク選択時の処理"""
        self.current_main_task = task_name
        self._show_subtask_window()

    def _show_subtask_window(self):
        """サブタスク選択画面を表示"""
        self._clear_frame()

        self.current_frame = SubtaskWindow(
            self.root,
            self.settings,
            self.current_main_task,
            on_subtask_select=self._on_subtask_select,
            on_back=self._show_main_window
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def _on_subtask_select(self, subtask_name: str):
        """サブタスク選択時の処理"""
        self.current_sub_task = subtask_name
        self._show_timer_window()

    def _show_timer_window(self):
        """タイマー画面を表示"""
        self._clear_frame()

        self.current_frame = TimerWindow(
            self.root,
            self.settings,
            self.csv_writer,
            self.current_main_task,
            self.current_sub_task,
            on_complete=self._show_main_window,
            on_back=self._show_subtask_window
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_settings_window(self):
        """設定画面を表示"""
        self._clear_frame()

        self.current_frame = SettingsWindow(
            self.root,
            self.settings,
            self.task_manager,
            on_back=self._show_main_window,
            on_save=self._on_settings_saved
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def _on_settings_saved(self):
        """設定保存後の処理"""
        # CSVWriterの出力先を更新
        self.csv_writer = CSVWriter(self.settings.output_folder)
        self._show_main_window()

    def _on_drag_start(self, event):
        """ドラッグ開始"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def _on_drag_motion(self, event):
        """ドラッグ中"""
        x = self.root.winfo_x() + event.x - self._drag_start_x
        y = self.root.winfo_y() + event.y - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")

    def _on_close(self):
        """終了時の処理"""
        self.settings.set_window_position(
            self.root.winfo_x(),
            self.root.winfo_y()
        )
        self.root.destroy()

    def run(self):
        """アプリケーションを実行"""
        self.root.mainloop()


def main():
    """エントリーポイント"""
    app = TaskTimestampApp()
    app.run()


if __name__ == "__main__":
    main()
