import sqlite3

class Repository:
    def __init__(self, table):
        self.table = table
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
        """Insert a new record.
        Expects a dictionary with keys: 'title', 'artist', 'filename', 'data'.

        Returns:
            int: the ID of the newly inserted row.
        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {self.table} (title, artist, filename, data) VALUES (?, ?, ?, ?)",
                (js["title"], js["artist"], js["filename"], js["data"])
            )
            connection.commit()
            # Return the auto-incremented id
            return cursor.lastrowid

    def update(self, js)->int:
        """Update an existing record by 'id'.
        Expects a dictionary with keys: 'id', 'title', 'artist', 'filename', 'data'.

        Returns:
            int: the number of rows affected (should be 1 if successful).
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
        """Retrieve a row by its ID.

        Returns:
            Dictionary: a dictionary with 'id', 'title', 'artist', 'filename', 'data',
            None: if not found.
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
                    "data": row[4]
                }
            else:
                return None
            
    def remove(self, item_id: int) -> int:
        """Deletes a single row from the table by record_id.

        Args:
            item_id (int): ID of item to be deleted

        Returns:
            int: number of items deleted
        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {self.table} WHERE id=?", (item_id,))
            connection.commit()
            return cursor.rowcount
        
    def get_id(self, title: str):
        """Returns the id of a givern track.

        Args:
            title (str): Name of the song to return
        
        Returns:
            int: the id of the track that matches the input song title
            None: if the id can't be found
        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT id FROM {self.table} WHERE title=?", (title,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
            
    def get_track_titles(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT title FROM {self.table}")
            rows = cursor.fetchall()
            titles = []
            for title in rows:
                titles.append(title)
            return titles

            


