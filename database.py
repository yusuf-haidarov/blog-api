import sqlite3

def init_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bio TEXT
        )
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        views INTEGER DEFAULT 0,
        FOREIGN KEY (author_id) REFERENCES authors(id)
    )
""")
    
    conn.commit()
    conn.close()
    print('Databases were made')


def seed_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()

    authors = [
        ("blogger1", 'aaaaaaa'),
        ("blogger2", 'bbbbbbb'),
        ("blogger3", 'cccc123123ccc')
    ]
    cursor.executemany(
        "INSERT INTO authors (name, bio) VALUES (?, ?)",
        authors
    )

    posts = [
        ('hello', 'qwertyuiop', 1, 5),
        ('hi', 'aaazzxxdff', 2, 1000),
        ('addaddadadadada', 'xxxxmxmmxxmx', 3, 200),
        ('abcd', '12345678', 3, 500)
    ]
    cursor.executemany(
            "INSERT INTO posts (title, content, author_id, views) VALUES (?, ?, ?, ?)",
            posts
        )

    
    conn.commit()
    conn.close()
    print(f"{len(authors)} authors were added")
    print(f'{len(posts)} posts were added')

if __name__ == "__main__":
    init_db()
    seed_db()