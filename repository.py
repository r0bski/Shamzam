import sqlite3

class Repository:
    def __init__(self, table):
        self.table = table
        # Database file name will be e.g. "audio_files.db" if table="audio_files"
        self.database = self.table + ".db"
        self.make()

    def make(self):
        """
        Create the table if it doesn't already exist.
        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    data TEXT NOT NULL
                )"""
            )
            connection.commit()

    def clear(self):
        """
        Delete all rows from the table.
        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {self.table}")
            connection.commit()

    def insert(self, js):
        """
        Insert a new record.
        Expects a dictionary with keys: 'title', 'artist', 'filename', 'data'.
        Returns the ID of the newly inserted row.
        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {self.table} (title, artist, filename, data) VALUES (?, ?, ?, ?)",
                (js["title"], js["artist"], js["filename"], js["data"])
            )
            connection.commit()
            return cursor.lastrowid  # Return the auto-incremented id

    def update(self, js):
        """
        Update an existing record by 'id'.
        Expects a dictionary with keys: 'id', 'title', 'artist', 'filename', 'data'.
        Returns the number of rows affected (should be 1 if successful).
        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE {self.table} "
                f"SET title=?, artist=?, filename=?, data=? "
                f"WHERE id=?",
                (js["title"], js["artist"], js["filename"], js["data"], js["id"])
            )
            connection.commit()
            return cursor.rowcount

    def lookup(self, record_id):
        """
        Retrieve a row by its 'id'.
        Returns a dictionary with 'id', 'title', 'artist', 'filename', 'data',
        or None if not found.
        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT id, title, artist, filename, data "
                f"FROM {self.table} WHERE id=?",
                (record_id,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "title": row[1],
                    "artist": row[2],
                    "filename": row[3],
                    "data": row[1]
                }
            else:
                return None
            


