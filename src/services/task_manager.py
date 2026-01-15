"""タスク管理サービス"""
import json
from pathlib import Path
from typing import List
import sys
import os

# srcディレクトリをパスに追加
src_dir = Path(__file__).parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from models.task import MainTask


class TaskManager:
    """メインタスクの管理を担当するクラス"""
    
    def __init__(self, data_file: Path):
        self.data_file = data_file
        self.tasks: List[MainTask] = []
        self._load()
    
    def _load(self):
        """タスクをファイルから読み込む"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [MainTask(**item) for item in data]
            except (json.JSONDecodeError, IOError):
                self.tasks = []
    
    def _save(self):
        """タスクをファイルに保存する"""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        data = [{"id": t.id, "name": t.name, "color": t.color} for t in self.tasks]
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all(self) -> List[MainTask]:
        """全タスクを取得する"""
        return self.tasks
    
    def add(self, name: str, color: str = "#4A90D9") -> MainTask:
        """新しいタスクを追加する"""
        new_id = max((t.id for t in self.tasks), default=0) + 1
        task = MainTask(id=new_id, name=name, color=color)
        self.tasks.append(task)
        self._save()
        return task
    
    def remove(self, task_id: int) -> bool:
        """タスクを削除する"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self._save()
                return True
        return False
