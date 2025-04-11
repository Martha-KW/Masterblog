from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)

def load_posts():
    with open("posts.json", "r") as file:
        return json.load(file)


def save_posts(posts):
    with open("posts.json", "w") as file:
        json.dump(posts, file, indent=4)


def fetch_post_by_id(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts=load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        existing_ids = [post['id'] for post in load_posts()]
        new_id = 1

        while new_id in existing_ids:  # loops to find unique post id
            new_id += 1

        new_post = {'id': new_id, 'title': title, 'author': author, 'content': content}
        blog_posts=load_posts()
        blog_posts.append(new_post)
        save_posts((blog_posts))

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts =load_posts()
    updated_posts = [post for post in posts if post['id'] != post_id]

    with open("posts.json", "w") as file:
        json.dump(updated_posts, file, indent=4)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
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
    posts = load_posts()
    for post in posts:
        if post['id'] == id:

            post['likes'] = post.get('likes', 0) + 1
            breåçak
    else:
        return "Post not found", 404

    save_posts(posts)
    return redirect(url_for('index'))


@app.route('/post/<int:post_id>')
def view_post(post_id):
    posts = load_posts()  # ← das hat gefehlt
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        abort(404)
    return render_template('view_post.html', post=post)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
