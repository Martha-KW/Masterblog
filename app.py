from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_posts():
    """Loads all posts from the posts.json file."""
    with open("posts.json", "r") as file:
        return json.load(file)


def save_posts(posts):
    """Saves the updated blog texts into the posts.json file."""
    with open("posts.json", "w") as file:
        json.dump(posts, file, indent=4)


def fetch_post_by_id(post_id):
    """Fetches a unique post via its post ID."""
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    """The home route that displays all existing posts on the blog homepage."""
    blog_posts=load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """The route for adding a totally new blog post, uses GET and POST"""
    if request.method == 'POST':
        # Extracts the data from the input form, the blogger typed in
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # gets all existing IDs and creates then an unused unique ID
        existing_ids = [post['id'] for post in load_posts()]
        new_id = 1

        while new_id in existing_ids:
            new_id += 1

        # creates a new post
        new_post = {'id': new_id, 'title': title, 'author': author, 'content': content}
        blog_posts=load_posts()
        blog_posts.append(new_post)
        save_posts((blog_posts))

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Route for deleting a post, selected by its unique ID"""
    posts =load_posts()
    updated_posts = [post for post in posts if post['id'] != post_id]

    with open("posts.json", "w") as file:
        json.dump(updated_posts, file, indent=4)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Route to update an existing blog post"""
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)

    if not post:
        return "Post not found", 404

    if request.method == 'POST':

        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)


@app.route('/like/<int:id>', methods=['POST'])
def like_post(id):
    """Route to like a post. Likes count is updated here."""
    posts = load_posts()
    for post in posts:
        if post['id'] == id:

            post['likes'] = post.get('likes', 0) + 1
            break
    else:
        return "Post not found", 404

    save_posts(posts)
    return redirect(url_for('index'))


@app.route('/post/<int:post_id>')
def view_post(post_id):
    """Route to view the full text of a single post on a new page"""
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        abort(404)
    return render_template('view_post.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
