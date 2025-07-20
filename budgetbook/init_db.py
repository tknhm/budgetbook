import os
import sqlite3
from budgetbook.app import app


def init_db():
    db_path = app.config["DB_PATH"]

    # DBファイルのディレクトリを確実に作る
    db_dir = os.path.dirname(db_path)
    if db_dir:  # ルート直下のときは空文字になるのでチェック
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ✅ テスト時は古いデータを削除する
    if app.config.get("TESTING", False):
        cursor.executescript(
            """
            DROP TABLE IF EXISTS income;
            DROP TABLE IF EXISTS expense;
        """
        )

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            shop TEXT,
            category TEXT NOT NULL,
            amount INTEGER NOT NULL,
            payment TEXT
        );
        """
    )

    conn.commit()
    conn.close()
    print(f"✅ Initialized DB at {db_path}")


if __name__ == "__main__":
    init_db()
