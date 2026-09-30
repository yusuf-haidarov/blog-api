import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("blog.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/authors", methods=["GET"])
def get_authors():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM authors")
    rows = cursor.fetchall()

    conn.close()

    authors = []
    for row in rows:
        authors.append({
            "id": row["id"],
            "name": row["name"],
            "bio": row['bio']
        })

    return jsonify(authors)


@app.route("/posts", methods=["GET"])
def get_posts():
    conn = get_db_connection()
    cursor = conn.cursor()


    author_id = request.args.get("author_id")
    if author_id:
        cursor.execute("SELECT * FROM posts WHERE author_id = ?", (author_id,))
    else:
        cursor.execute("SELECT * FROM posts")

    rows = cursor.fetchall()

    conn.close()
    
    posts = []
    for row in rows:
        posts.append({
            "id" : row['id'],
            "title": row["title"],
            "content": row["content"],
            "author_id": row['author_id'],
            'views': row['views']
        })

    return jsonify(posts)


@app.route("/posts/<int:id>", methods=["GET"])
def get_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE posts SET views = views + 1 WHERE id = ?", (id,))
    conn.commit()

    cursor.execute("SELECT * FROM posts WHERE id = ?", (id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return jsonify({"error": "Post not found"}), 404

    conn.close()

    post = {
        "id": row["id"],
        "title": row["title"],
        "content": row["content"],
        "author_id": row["author_id"],
        "views": row["views"]
    }
    return jsonify(post)


@app.route("/posts", methods=["POST"])
def add_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data for post provided"}), 400

    title = data.get("title")
    content = data.get("content")
    author_id = data.get("author_id")

    if not title or not content or not author_id:
        return jsonify({"error": "Fields title, content, author_id must be filled"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
        (title, content, author_id)
    )

    new_id = cursor.lastrowid

    cursor.execute("SELECT * FROM posts WHERE id = ?", (new_id,))
    row = cursor.fetchone()

    conn.commit()
    conn.close()

    return jsonify({
    "id": row["id"],
    "title": row["title"],
    "content": row["content"],
    "author_id": row["author_id"],
    "views": row["views"]
}), 201


if __name__ == "__main__":
    app.run(debug=True)