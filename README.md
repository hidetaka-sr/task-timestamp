# タスクタイムスタンプ記録アプリ

シンプルなクリック操作でタスクの開始/終了時間を記録するデスクトップアプリです。

## 特徴

- ✅ 常に最前面に表示されるコンパクトなウィンドウ
- ✅ クリックだけで開始/終了を記録
- ✅ CSV形式で月別に自動保存（Excel対応）
- ✅ 複数ユーザのデータ集計に対応
- ✅ アプリ内から設定変更可能
- ✅ Excelからタスクインポート可能

## スクリーンショット

（準備中）

## インストール

### 配布版（exe）
1. Releasesから`TaskTimestamp_v2.0.zip`をダウンロード
2. 任意のフォルダに解凍
3. `TaskTimestamp.exe`を実行

### 開発環境
```bash
git clone https://github.com/hidetaka-sr/task-timestamp.git
cd task-timestamp
python src/main.py
```

## 使い方

1. **メインタスク選択**: プロジェクト/案件を選択
2. **サブタスク選択**: 作業内容を選択
3. **開始ボタン**: 作業開始時刻を記録
4. **終了ボタン**: 作業終了時刻を記録 → CSVに保存

## 設定

設定ファイル: `Documents\TaskTimestamp\config.json`

```json
{
  "output_folder": "C:\\Users\\<ユーザ名>\\Documents\\TaskTimestamp",
  "subtasks": ["図面チェック", "成果品策定", "電話対応", ...],
  "font_size": 10
}
```

## CSV出力形式

| ユーザ名 | メインタスク | サブタスク | 開始日時 | 終了日時 | 作業時間(分) |
|---------|------------|----------|---------|---------|------------|
| yamada | プロジェクトA | 図面チェック | 2026/01/14 10:30:00 | 2026/01/14 11:15:00 | 45 |

## ビルド

```bash
pip install pyinstaller
python -m PyInstaller build_onefile.spec
```

## ライセンス

MIT License
