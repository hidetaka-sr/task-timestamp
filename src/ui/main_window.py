"""メインタスク一覧画面"""
import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from services.task_manager import TaskManager
    from config.settings import Settings


class MainWindow(tk.Frame):
    """メインタスク一覧を表示するフレーム"""

    def __init__(self, parent: tk.Widget, task_manager: "TaskManager",
                 settings: "Settings",
                 on_task_select: Callable[[str], None],
                 on_settings: Callable[[], None] = None):
        super().__init__(parent)
        self.task_manager = task_manager
        self.settings = settings
        self.on_task_select = on_task_select
        self.on_settings = on_settings
        self.configure(bg=settings.COLORS["bg_primary"])
        self._create_widgets()

    def _create_widgets(self):
        """ウィジェットを作成する"""
        colors = self.settings.COLORS

        # ヘッダー
        header = tk.Frame(self, bg=colors["bg_secondary"], pady=5)
        header.pack(fill=tk.X)

        # 設定ボタン
        if self.on_settings:
            settings_btn = tk.Button(
                header,
                text="⚙",
                font=self.settings.FONT_MEDIUM,
                bg=colors["bg_tertiary"],
                fg=colors["text_secondary"],
                activebackground=colors["accent"],
                activeforeground=colors["text_primary"],
                relief=tk.FLAT,
                cursor="hand2",
                width=2,
                command=self.on_settings
            )
            settings_btn.pack(side=tk.RIGHT, padx=3)

        title = tk.Label(
            header,
            text="📋 タスク",
            font=self.settings.FONT_LARGE,
            bg=colors["bg_secondary"],
            fg=colors["text_primary"]
        )
        title.pack(side=tk.LEFT, padx=5)

        # タスクリストコンテナ
        self.task_container = tk.Frame(self, bg=colors["bg_primary"])
        self.task_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._refresh_task_list()

        # フッター（追加ボタン）
        footer = tk.Frame(self, bg=colors["bg_primary"], pady=5)
        footer.pack(fill=tk.X)

        add_btn = tk.Button(
            footer,
            text="＋ 追加",
            font=self.settings.FONT_SMALL,
            bg=colors["bg_tertiary"],
            fg=colors["text_primary"],
            activebackground=colors["accent"],
            activeforeground=colors["text_primary"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._add_task
        )
        add_btn.pack(pady=3)

    def _refresh_task_list(self):
        """タスクリストを更新する"""
        for widget in self.task_container.winfo_children():
            widget.destroy()

        colors = self.settings.COLORS
        tasks = self.task_manager.get_all()

        if not tasks:
            empty_label = tk.Label(
                self.task_container,
                text="タスクなし\n＋ 追加",
                font=self.settings.FONT_SMALL,
                bg=colors["bg_primary"],
                fg=colors["text_secondary"],
                justify=tk.CENTER
            )
            empty_label.pack(pady=20)
            return

        for task in tasks:
            self._create_task_button(task)

    def _create_task_button(self, task):
        """タスクボタンを作成する"""
        colors = self.settings.COLORS

        btn_frame = tk.Frame(self.task_container, bg=colors["bg_primary"])
        btn_frame.pack(fill=tk.X, pady=2)

        btn = tk.Button(
            btn_frame,
            text=task.name,
            font=self.settings.FONT_SMALL,
            bg=task.color,
            fg=colors["text_primary"],
            activebackground=colors["accent_hover"],
            activeforeground=colors["text_primary"],
            relief=tk.FLAT,
            cursor="hand2",
            height=1,
            command=lambda t=task: self.on_task_select(t.name)
        )
        btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        del_btn = tk.Button(
            btn_frame,
            text="×",
            font=self.settings.FONT_SMALL,
            bg=colors["bg_tertiary"],
            fg=colors["text_secondary"],
            activebackground=colors["accent"],
            activeforeground=colors["text_primary"],
            relief=tk.FLAT,
            cursor="hand2",
            width=2,
            command=lambda t=task: self._delete_task(t.id)
        )
        del_btn.pack(side=tk.RIGHT)

    def _add_task(self):
        """タスクを追加する"""
        name = simpledialog.askstring("追加", "タスク名:")
        if name and name.strip():
            self.task_manager.add(name.strip())
            self._refresh_task_list()

    def _delete_task(self, task_id: int):
        """タスクを削除する"""
        if messagebox.askyesno("確認", "削除しますか？"):
            self.task_manager.remove(task_id)
            self._refresh_task_list()

    def refresh(self):
        """画面をリフレッシュする"""
        self._refresh_task_list()
