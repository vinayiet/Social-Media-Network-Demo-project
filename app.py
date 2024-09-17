# from flask import Flask, jsonify, request
# from neo4j import GraphDatabase

# app = Flask(__name__)

# # Neo4j Aura connection details
# uri = "neo4j+s://a01a7d6c.databases.neo4j.io:7687"  # Replace with your Aura URI
# driver = GraphDatabase.driver(uri, auth=("neo4j", "WvcXNlyWhzYhHuUqbw2qCi9RGjCfmM_gWQTVSLGiN2k"))  # Replace with your credentials

# def find_posts_by_friends(tx, user_name):
#     query = """
#     MATCH (u:User)-[:FRIEND]-(f)-[:POSTED]->(post)
#     WHERE u.name = $user_name
#     RETURN f.name AS friend, post.text AS content
#     """
#     result = tx.run(query, user_name=user_name)
#     return [{"friend": record["friend"], "content": record["content"]} for record in result]

# def find_posts_with_likes(tx, user_name):
#     query = """
#     MATCH (u:User)-[:FRIEND]-(f)-[:POSTED]->(post)<-[like:LIKED]-(liker)
#     WHERE u.name = $user_name
#     RETURN f.name AS friend, post.text AS content, COLLECT(liker.name) AS liked_by
#     """
#     result = tx.run(query, user_name=user_name)
#     return [{"friend": record["friend"], "content": record["content"], "liked_by": record["liked_by"]} for record in result]

# def find_all_actions_on_posts(tx, user_name):
#     query = """
#     MATCH (u:User)-[:FRIEND]-(f)-[:POSTED]->(post)<-[a:LIKED|:COMMENTED]-(person)
#     WHERE u.name = $user_name
#     RETURN f.name AS friend, post.text AS content,
#            COLLECT({ text: a.text, person: person.name, action: TYPE(a)}) AS actions
#     """
#     result = tx.run(query, user_name=user_name)
#     return [{"friend": record["friend"], "content": record["content"], "actions": record["actions"]} for record in result]

# @app.route('/')
# def index():
#     return "Welcome to the Neo4j Social Media Network Demo!"

# @app.route('/posts/<username>')
# def get_posts(username):
#     with driver.session() as session:
#         posts = session.read_transaction(find_posts_by_friends, username)
#     return jsonify(posts)

# @app.route('/posts/likes/<username>')
# def get_posts_with_likes(username):
#     with driver.session() as session:
#         posts = session.read_transaction(find_posts_with_likes, username)
#     return jsonify(posts)

# @app.route('/posts/actions/<username>')
# def get_all_actions(username):
#     with driver.session() as session:
#         actions = session.read_transaction(find_all_actions_on_posts, username)
#     return jsonify(actions)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j Aura connection details
uri = "neo4j+s://a01a7d6c.databases.neo4j.io:7687"  # Replace with your Aura URI
driver = GraphDatabase.driver(uri, auth=("neo4j", "WvcXNlyWhzYhHuUqbw2qCi9RGjCfmM_gWQTVSLGiN2k"))  # Replace with your credentials

def fetch_all_posts(tx):
    query = """
    MATCH (u:User)-[:POSTED]->(post)
    RETURN u.name AS username, post.text AS post_content
    """
    result = tx.run(query)
    return [{"username": record["username"], "post_content": record["post_content"]} for record in result]

def fetch_all_posts_with_likes(tx):
    query = """
    MATCH (u:User)-[:POSTED]->(post)<-[like:LIKED]-(liker)
    RETURN u.name AS username, post.text AS post_content, COLLECT(liker.name) AS liked_by
    """
    result = tx.run(query)
    return [{"username": record["username"], "post_content": record["post_content"], "liked_by": record["liked_by"]} for record in result]

def fetch_all_posts_with_comments(tx):
    query = """
    MATCH (u:User)-[:POSTED]->(post)<-[:COMMENTED]-(commenter:User)
    RETURN u.name AS username, post.text AS post_content, COLLECT(commenter.name) AS commenters
    """
    result = tx.run(query)
    return [{"username": record["username"], "post_content": record["post_content"], "commenters": record["commenters"]} for record in result]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    with driver.session() as session:
        posts = session.read_transaction(fetch_all_posts)
    return render_template('posts.html', posts=posts)

@app.route('/likes')
def likes():
    with driver.session() as session:
        posts_with_likes = session.read_transaction(fetch_all_posts_with_likes)
    return render_template('likes.html', posts_with_likes=posts_with_likes)

@app.route('/comments')
def comments():
    with driver.session() as session:
        posts_with_comments = session.read_transaction(fetch_all_posts_with_comments)
    return render_template('comments.html', posts_with_comments=posts_with_comments)

if __name__ == '__main__':
    app.run(debug=True)
