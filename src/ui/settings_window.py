"""設定画面"""
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from config.settings import Settings
    from services.task_manager import TaskManager


class SettingsWindow(tk.Frame):
    """設定画面を表示するフレーム"""

    def __init__(self, parent: tk.Widget, settings: "Settings",
                 task_manager: "TaskManager",
                 on_back: Callable[[], None],
                 on_save: Callable[[], None]):
        super().__init__(parent)
        self.settings = settings
        self.task_manager = task_manager
        self.on_back = on_back
        self.on_save = on_save
        self.configure(bg=settings.COLORS["bg_primary"])
        self._create_widgets()

    def _create_widgets(self):
        """ウィジェットを作成する"""
        colors = self.settings.COLORS

        # ヘッダー
        header = tk.Frame(self, bg=colors["bg_secondary"], pady=5)
        header.pack(fill=tk.X)

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

        title = tk.Label(
            header,
            text="⚙ 設定",
            font=self.settings.FONT_LARGE,
            bg=colors["bg_secondary"],
            fg=colors["text_primary"]
        )
        title.pack(side=tk.LEFT, padx=5)

        # スクロール可能なコンテナ
        container = tk.Frame(self, bg=colors["bg_primary"])
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # フォントサイズ設定
        font_frame = tk.Frame(container, bg=colors["bg_primary"])
        font_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            font_frame,
            text="文字サイズ:",
            font=self.settings.FONT_SMALL,
            bg=colors["bg_primary"],
            fg=colors["text_primary"]
        ).pack(side=tk.LEFT)

        self.font_size_var = tk.StringVar(value=str(self.settings.font_size))
        font_spin = tk.Spinbox(
            font_frame,
            from_=6,
            to=20,
            width=4,
            textvariable=self.font_size_var,
            font=self.settings.FONT_SMALL
        )
        font_spin.pack(side=tk.LEFT, padx=5)

        # 出力フォルダ設定
        folder_frame = tk.Frame(container, bg=colors["bg_primary"])
        folder_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            folder_frame,
            text="出力先:",
            font=self.settings.FONT_SMALL,
            bg=colors["bg_primary"],
            fg=colors["text_primary"]
        ).pack(anchor=tk.W)

        folder_btn_frame = tk.Frame(folder_frame, bg=colors["bg_primary"])
        folder_btn_frame.pack(fill=tk.X)

        self.folder_var = tk.StringVar(value=str(self.settings.output_folder))
        folder_entry = tk.Entry(
            folder_btn_frame,
            textvariable=self.folder_var,
            font=self.settings.FONT_SMALL,
            width=15
        )
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_btn = tk.Button(
            folder_btn_frame,
            text="...",
            font=self.settings.FONT_SMALL,
            bg=colors["bg_tertiary"],
            fg=colors["text_primary"],
            relief=tk.FLAT,
            command=self._browse_folder
        )
        browse_btn.pack(side=tk.LEFT, padx=2)

        # Excelインポート
        import_frame = tk.Frame(container, bg=colors["bg_primary"])
        import_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            import_frame,
            text="タスクインポート:",
            font=self.settings.FONT_SMALL,
            bg=colors["bg_primary"],
            fg=colors["text_primary"]
        ).pack(anchor=tk.W)

        import_btn = tk.Button(
            import_frame,
            text="📥 Excelから読込",
            font=self.settings.FONT_SMALL,
            bg=colors["bg_tertiary"],
            fg=colors["text_primary"],
            activebackground=colors["accent"],
            activeforeground=colors["text_primary"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._import_from_excel
        )
        import_btn.pack(fill=tk.X, pady=3)

        # 保存ボタン
        save_btn = tk.Button(
            container,
            text="💾 保存して戻る",
            font=self.settings.FONT_BUTTON,
            bg=colors["success"],
            fg=colors["text_primary"],
            activebackground=colors["accent_hover"],
            activeforeground=colors["text_primary"],
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            command=self._save_settings
        )
        save_btn.pack(fill=tk.X, pady=10)

    def _browse_folder(self):
        """フォルダ選択ダイアログ"""
        folder = filedialog.askdirectory(
            initialdir=str(self.settings.output_folder)
        )
        if folder:
            self.folder_var.set(folder)

    def _import_from_excel(self):
        """Excelファイルからタスクをインポート"""
        filetypes = [
            ("Excel files", "*.xlsx *.xls"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if not filepath:
            return

        try:
            tasks = self._read_tasks_from_file(filepath)
            if tasks:
                for task_name in tasks:
                    if task_name.strip():
                        self.task_manager.add(task_name.strip())
                messagebox.showinfo(
                    "完了",
                    f"{len(tasks)}件のタスクをインポートしました"
                )
        except Exception as e:
            messagebox.showerror("エラー", f"読み込み失敗:\n{e}")

    def _read_tasks_from_file(self, filepath: str) -> list:
        """ファイルからタスク一覧を読み込む（1行目はヘッダとしてスキップ）"""
        import csv

        tasks = []
        if filepath.endswith('.csv'):
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader, None)  # ヘッダ行をスキップ
                for row in reader:
                    if row and row[0] and row[0].strip():
                        tasks.append(row[0].strip())
        elif filepath.endswith('.xlsx'):
            # .xlsx形式（openpyxlを使用）
            try:
                import openpyxl
                wb = openpyxl.load_workbook(filepath, read_only=True)
                ws = wb.active
                first_row = True
                for row in ws.iter_rows(values_only=True):
                    if first_row:
                        first_row = False
                        continue  # ヘッダ行をスキップ
                    if row and row[0]:
                        tasks.append(str(row[0]).strip())
                wb.close()
            except ImportError:
                messagebox.showwarning(
                    "注意",
                    "Excelファイル(.xlsx)を読むにはopenpyxlが必要です。\n"
                    "CSVファイルに変換してご利用ください。\n\n"
                    "Excelで「名前を付けて保存」→\n"
                    "ファイル形式「CSV UTF-8」を選択"
                )
                return []
        elif filepath.endswith('.xls'):
            # .xls形式（xlrdを使用）
            try:
                import xlrd
                wb = xlrd.open_workbook(filepath)
                ws = wb.sheet_by_index(0)
                for i in range(1, ws.nrows):  # 1行目スキップ
                    val = ws.cell_value(i, 0)
                    if val:
                        tasks.append(str(val).strip())
            except ImportError:
                messagebox.showwarning(
                    "注意",
                    "Excelファイル(.xls)を読むにはxlrdが必要です。\n"
                    "CSVファイルに変換してご利用ください。"
                )
                return []
        else:
            messagebox.showwarning(
                "注意",
                "対応形式: .xlsx, .xls, .csv\n"
                "CSVファイルをご利用ください。"
            )
            return []
        return tasks

    def _save_settings(self):
        """設定を保存"""
        try:
            font_size = int(self.font_size_var.get())
            self.settings.set_font_size(font_size)
        except ValueError:
            pass

        folder = self.folder_var.get()
        if folder:
            self.settings.set_output_folder(folder)

        self.on_save()
