"""CSV書き込みサービス"""
import csv
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.task import TimeRecord


class CSVWriter:
    """CSV書き込みを担当するクラス"""

    # ヘッダー（ユーザ名を追加、Excel形式の日時）
    CSV_HEADER = [
        "ユーザ名",
        "メインタスク",
        "サブタスク",
        "開始日時",
        "終了日時",
        "作業時間(分)"
    ]

    def __init__(self, output_folder: Path):
        self.output_folder = output_folder

    def _get_filename(self) -> str:
        """月別のファイル名を生成する"""
        return f"timestamp_{datetime.now().strftime('%Y%m')}.csv"

    def _get_filepath(self) -> Path:
        """出力ファイルパスを取得する"""
        self.output_folder.mkdir(parents=True, exist_ok=True)
        return self.output_folder / self._get_filename()

    def write_record(self, record: "TimeRecord") -> str:
        """時間記録をCSVに書き込む"""
        filepath = self._get_filepath()
        file_exists = filepath.exists()

        with open(filepath, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(self.CSV_HEADER)
            writer.writerow(record.to_csv_row())

        return str(filepath)
