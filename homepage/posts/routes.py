from flask import render_template, request, redirect, url_for, flash, abort, Blueprint
from flask_login import current_user
from homepage import login_required_author
from homepage import db
from homepage.models import Post, Comment
from homepage.posts.forms import (PostForm, CommentForm)
import sys

from homepage.main.reading_time import estimate_reading_time

posts = Blueprint('posts', __name__)


@posts.route('/new_post', methods=['GET', 'POST'])
@login_required_author('admin')
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, abstract = form.abstract.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.blog'))
    return render_template('new_post.html', title='New post', form=form, legend='New Post')

@posts.route('/post/<int:post_id>/new_comment', methods=['GET', 'POST'])
@login_required_author()
def new_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content = form.content.data, author_comment = current_user, pid = post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    return render_template('new_comment.html', title='New Comment', form=form, legend='New Comment')

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required_author()
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.abstract = form.abstract.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return (redirect(url_for('posts.post', post_id=post.id)))
    elif request.method == 'GET':
        form.title.data = post.title
        form.abstract.data = post.abstract
        form.content.data = post.content
    return render_template('new_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    # comments = Comment.query.filter(Comment.pid == post_id).get_or_404()
    comments = db.session.query(Comment).filter(Comment.pid == post_id).all()
    # print (comments)
    time_to_read = 0
    if not request.args.get('silent'): 
        time_to_read = estimate_reading_time(request.url+"?silent=True")
    return render_template('post.html', title=post.title, post=post, comments=comments, time_to_read=round(time_to_read))



@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required_author()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return (redirect(url_for('main.blog', post_id=post.id)))
