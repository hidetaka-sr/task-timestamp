"""サブタスク選択画面"""
import tkinter as tk
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from config.settings import Settings


class SubtaskWindow(tk.Frame):
    """サブタスク選択を表示するフレーム"""

    def __init__(self, parent: tk.Widget, settings: "Settings",
                 main_task: str,
                 on_subtask_select: Callable[[str], None],
                 on_back: Callable[[], None]):
        super().__init__(parent)
        self.settings = settings
        self.main_task = main_task
        self.on_subtask_select = on_subtask_select
        self.on_back = on_back
        self.configure(bg=settings.COLORS["bg_primary"])
        self._create_widgets()

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
            command=self.on_back
        )
        back_btn.pack(side=tk.LEFT, padx=5)

        # メインタスク名（短縮表示）
        display_name = self.main_task[:10] + "..." if len(self.main_task) > 10 else self.main_task
        task_label = tk.Label(
            header,
            text=f"📌 {display_name}",
            font=self.settings.FONT_SMALL,
            bg=colors["bg_secondary"],
            fg=colors["accent"]
        )
        task_label.pack(side=tk.LEFT, padx=3)

        subtitle = tk.Label(
            self,
            text="何をする？",
            font=self.settings.FONT_MEDIUM,
            bg=colors["bg_primary"],
            fg=colors["text_primary"]
        )
        subtitle.pack(pady=(10, 5))

        container = tk.Frame(self, bg=colors["bg_primary"])
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        button_colors = [
            "#e94560", "#4ecca3", "#4A90D9",
            "#FFB347", "#9B59B6", "#3498DB", "#95A5A6"
        ]

        # configから読み込んだサブタスクを表示
        for i, subtask in enumerate(self.settings.subtasks):
            btn_color = button_colors[i % len(button_colors)]
            btn = tk.Button(
                container,
                text=subtask,
                font=self.settings.FONT_SMALL,
                bg=btn_color,
                fg=colors["text_primary"],
                activebackground=colors["accent_hover"],
                activeforeground=colors["text_primary"],
                relief=tk.FLAT,
                cursor="hand2",
                height=1,
                command=lambda s=subtask: self.on_subtask_select(s)
            )
            btn.pack(fill=tk.X, pady=2)
