"""タスクデータモデル"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MainTask:
    """メインタスクを表すデータクラス"""
    id: int
    name: str
    color: str = "#4A90D9"


@dataclass
class TimeRecord:
    """時間記録を表すデータクラス"""
    main_task: str
    sub_task: str
    start_time: datetime
    username: str = ""
    end_time: Optional[datetime] = None

    @property
    def duration_minutes(self) -> Optional[int]:
        """作業時間（分）を計算する"""
        if self.end_time is None:
            return None
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)

    def _to_excel_datetime(self, dt: datetime) -> str:
        """Excel形式の日時文字列を生成する（YYYY/MM/DD HH:MM:SS）"""
        return dt.strftime("%Y/%m/%d %H:%M:%S")

    def to_csv_row(self) -> list:
        """CSV用の行データを生成する（Excel形式）"""
        start_str = self._to_excel_datetime(self.start_time)
        end_str = self._to_excel_datetime(self.end_time) if self.end_time else ""
        duration = self.duration_minutes or 0
        return [
            self.username,
            self.main_task,
            self.sub_task,
            start_str,
            end_str,
            str(duration)
        ]
