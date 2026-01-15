"""タイマー画面（開始/終了）"""
import tkinter as tk
from datetime import datetime
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from config.settings import Settings
    from services.csv_writer import CSVWriter


class TimerWindow(tk.Frame):
    """タイマー画面を表示するフレーム"""

    def __init__(self, parent: tk.Widget, settings: "Settings",
                 csv_writer: "CSVWriter",
                 main_task: str, sub_task: str,
                 on_complete: Callable[[], None],
                 on_back: Callable[[], None]):
        super().__init__(parent)
        self.settings = settings
        self.csv_writer = csv_writer
        self.main_task = main_task
        self.sub_task = sub_task
        self.on_complete = on_complete
        self.on_back = on_back

        self.start_time = None
        self.is_running = False
        self.timer_id = None

        self.configure(bg=settings.COLORS["bg_primary"])
        self._create_widgets()
        self._update_clock()

    def _create_widgets(self):
        """ウィジェットを作成する"""
        colors = self.settings.COLORS

        # ヘッダー
        header = tk.Frame(self, bg=colors["bg_secondary"], pady=5)
        header.pack(fill=tk.X)

        # 戻るボタン（わかりやすく改善）
        back_btn = tk.Button(
            header,
            text="◀ 戻る",
            font=self.settings.FONT_SMALL,
            bg=colors["accent"],
            fg=colors["text_primary"],
            activebackground=colors["accent_hover"],
            activeforeground=colors["text_primary"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._handle_back
        )
        back_btn.pack(side=tk.LEFT, padx=5)

        # タスク情報
        info_frame = tk.Frame(self, bg=colors["bg_primary"])
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        display_name = self.main_task[:12] + "..." if len(self.main_task) > 12 else self.main_task
        tk.Label(
            info_frame,
            text=f"📌 {display_name}",
            font=self.settings.FONT_SMALL,
            bg=colors["bg_primary"],
            fg=colors["accent"]
        ).pack(anchor=tk.W)

        tk.Label(
            info_frame,
            text=f"🔹 {self.sub_task}",
            font=self.settings.FONT_MEDIUM,
            bg=colors["bg_primary"],
            fg=colors["text_primary"]
        ).pack(anchor=tk.W)

        # 現在時刻表示
        self.clock_label = tk.Label(
            self,
            text="",
            font=self.settings.FONT_CLOCK,
            bg=colors["bg_primary"],
            fg=colors["text_primary"]
        )
        self.clock_label.pack(pady=10)

        # 開始時間表示
        self.start_label = tk.Label(
            self,
            text="",
            font=self.settings.FONT_SMALL,
            bg=colors["bg_primary"],
            fg=colors["success"]
        )
        self.start_label.pack()

        # 経過時間表示
        self.elapsed_label = tk.Label(
            self,
            text="",
            font=self.settings.FONT_MEDIUM,
            bg=colors["bg_primary"],
            fg=colors["warning"]
        )
        self.elapsed_label.pack(pady=5)

        # メインボタン
        self.main_button = tk.Button(
            self,
            text="▶ 開始",
            font=self.settings.FONT_BUTTON,
            bg=colors["success"],
            fg=colors["text_primary"],
            activebackground=colors["accent_hover"],
            activeforeground=colors["text_primary"],
            relief=tk.FLAT,
            cursor="hand2",
            width=10,
            height=2,
            command=self._toggle_timer
        )
        self.main_button.pack(pady=15)

    def _update_clock(self):
        """時計を更新する"""
        now = datetime.now()
        self.clock_label.config(text=now.strftime("%H:%M:%S"))

        if self.is_running and self.start_time:
            elapsed = now - self.start_time
            minutes = int(elapsed.total_seconds() // 60)
            seconds = int(elapsed.total_seconds() % 60)
            self.elapsed_label.config(text=f"経過: {minutes:02d}:{seconds:02d}")

        self.timer_id = self.after(1000, self._update_clock)

    def _toggle_timer(self):
        """タイマーの開始/終了を切り替える"""
        colors = self.settings.COLORS

        if not self.is_running:
            self.start_time = datetime.now()
            self.is_running = True
            self.start_label.config(
                text=f"開始: {self.start_time.strftime('%H:%M:%S')}"
            )
            self.main_button.config(
                text="⏹ 終了",
                bg=colors["accent"]
            )
        else:
            self._finish_recording()

    def _finish_recording(self):
        """記録を完了し、CSVに書き込む"""
        from models.task import TimeRecord

        end_time = datetime.now()
        record = TimeRecord(
            main_task=self.main_task,
            sub_task=self.sub_task,
            start_time=self.start_time,
            username=self.settings.get_username(),
            end_time=end_time
        )

        self.csv_writer.write_record(record)

        if self.timer_id:
            self.after_cancel(self.timer_id)

        self.on_complete()

    def _handle_back(self):
        """戻るボタン処理"""
        if self.is_running:
            from tkinter import messagebox
            if not messagebox.askyesno("確認", "記録中です。キャンセルしますか？"):
                return

        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.on_back()

    def destroy(self):
        """ウィジェット破棄時にタイマーをキャンセル"""
        if self.timer_id:
            self.after_cancel(self.timer_id)
        super().destroy()
