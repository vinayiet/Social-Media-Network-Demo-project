
# Social Media Network Demo porject

This project is a demonstration of a social media network using Flask and Neo4j. It showcases how to interact with a Neo4j graph database to perform operations related to posts, likes, and comments within a social network.

## Project Structure

- `app.py`: The main Flask application that connects to the Neo4j database and exposes endpoints for retrieving posts, likes, and comments.
- `templates/`: Contains HTML templates for displaying posts, likes, and comments.
- `requirements.txt`: Lists the dependencies required for this project.

## Prerequisites

- Python 3.x
- Neo4j Aura account with connection details

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/social-media-network-demo.git
cd social-media-network-demo
```

### 2. Create and Activate a Virtual Environment

**On Windows:**

```bash
python -m venv envvv
.\envvv\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv envvv
source envvv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Neo4j Connection

Update the `app.py` file with your Neo4j Aura connection details:

```python
uri = "neo4j+s://your-database-uri:7687"  # Replace with your Aura URI
driver = GraphDatabase.driver(uri, auth=("neo4j", "your-password"))  # Replace with your credentials
```

### 5. Run the Application

```bash
python app.py
```

The application will start, and you can access it via `http://127.0.0.1:5000`.

## Endpoints

- **Home Page**

  ```http
  GET / 
  ```

  Displays a welcome message.

- **Posts by Friends**

  ```http
  GET /posts/<username>
  ```

  Replace `<username>` with the name of the user whose friends' posts you want to retrieve.

- **Posts with Likes**

  ```http
  GET /posts/likes/<username>
  ```

  Replace `<username>` with the name of the user whose friends' posts with likes you want to retrieve.

- **All Actions on Posts**

  ```http
  GET /posts/actions/<username>
  ```

  Replace `<username>` with the name of the user whose friends' posts with all actions (likes and comments) you want to retrieve.

## HTML Templates

- `index.html`: Displays posts from friends.
- `posts.html`: Displays posts with likes.
- `actions.html`: Displays all actions on posts.


## Acknowledgments

- [Neo4j](https://neo4j.com) for the graph database technology.
- [Flask](https://flask.palletsprojects.com/) for the web framework.

