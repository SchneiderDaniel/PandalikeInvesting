from flask import render_template, request, redirect, url_for, flash, abort, Blueprint
from flask_login import current_user
from homepage import login_required_author
from homepage import db, login_manager
from homepage.models import Post, Comment, PostLikes, Tag, PostTags, CommentLikes
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

        tags = form.tags.data.split(',') 
        for t in tags:
            # print('Id: '  + str(post.id) + ' Tag: ' + t, file=sys.stderr)
            current_Tag = db.session.query(Tag).filter(Tag.name ==t.upper()).first()
            if not current_Tag:
                # print('Adding now Tag: ' + t + ' as ' + t.upper(), file=sys.stderr)
                current_Tag = Tag(name=t.upper())
                db.session.add(current_Tag)
                db.session.commit()
                # print('Added Tag: ' + str(current_Tag.id), file=sys.stderr)

            # print('Now relations for Post:' + str(post.id) + ' and Tag: ' + str(current_Tag.id), file=sys.stderr)
            tag_relation = PostTags(post_id=post.id,tag_id=current_Tag.id)
            db.session.add(tag_relation)
        db.session.commit()
        # print('Rdy', file=sys.stderr)
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
        meTo = url_for('posts.post', post_id=post_id)+ '#comment_button'
        return redirect(meTo)
    return render_template('new_comment.html', title='New Comment', form=form, legend='New Comment')

@posts.route('/post/<int:post_id>/update_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required_author()
def update_comment(post_id,comment_id ):
    comment = Comment.query.get_or_404(comment_id)
    post = Post.query.get_or_404(post_id)
    if comment.author_comment != current_user:
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return (redirect(url_for('posts.post', post_id=post.id)))
    elif request.method == 'GET':
        form.content.data = comment.content
    return render_template('new_comment.html', title='Update Comment', form=form, legend='Update Comment')

@posts.route('/post/<int:post_id>/delete_comment/<int:comment_id>', methods=['POST'])
@login_required_author()
def delete_comment(post_id,comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    if comment.author_comment != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return (redirect(url_for('posts.post', post_id=post.id)))


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
        likesList = db.session.query(PostTags).filter(PostTags.post_id == post.id ).all()
        tagsText = ''
        for l in likesList:
            toAdd = Tag.query.get_or_404(l.tag_id).name
            tagsText = tagsText + toAdd + ',' 
        form.tags.data = tagsText
       
    return render_template('new_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = db.session.query(Comment).filter(Comment.pid == post_id).all()
    amount_comments = len(comments)
    textlist = post.title, post.abstract, post.content
    time_to_read = estimate_reading_time(textlist) +1
    likesList = db.session.query(PostLikes).filter(PostLikes.post_id == post_id ).all()
    likes = len(likesList)
    theTagRel = db.session.query(PostTags).filter(PostTags.post_id == post_id ).all()
    theTags = []
    for t in theTagRel:
        toAdd = Tag.query.get_or_404(t.tag_id)
        theTags.append(toAdd)
    return render_template('post.html', title=post.title, post=post, comments=comments, time_to_read=round(time_to_read), amount_comments=amount_comments, likes = likes, theTags=theTags)

@posts.route('/post/<int:post_id>/like')
@login_required_author()
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    # print(current_user.id, file=sys.stderr)
    likes = db.session.query(PostLikes).filter(PostLikes.user_id == current_user.id).filter(PostLikes.post_id == post_id).all()
    # print('TESTI ' +str(current_user.id) +' ' +  str(post_id), file=sys.stderr)
    # print(likes, file=sys.stderr)
    if likes:
        flash('You have already liked that post', 'info')
    else:
        newLike = PostLikes(user_id=current_user.id, post_id=post_id)
        db.session.add(newLike)
        db.session.commit()
        flash('You liked that post', 'success')

    return (redirect(url_for('posts.post', post_id=post.id)))


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required_author()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    comments = db.session.query(Comment).filter(Comment.pid == post_id).all()
    for comment in comments:
        db.session.delete(comment)
    

    tagRels = db.session.query(PostTags).filter(PostTags.post_id == post_id).all()
    for tr in tagRels:
        db.session.delete(tr)

    likes = db.session.query(PostLikes).filter(PostLikes.user_id == post_id).all()
    for l in likes:
        db.session.delete(l)

    commentLikes = db.session.query(CommentLikes).filter(CommentLikes.user_id == post_id).all()
    for c in commentLikes:
        db.session.delete(c)

    

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return (redirect(url_for('main.blog', post_id=post.id)))
