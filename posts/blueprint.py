import json
import os
from flask import Blueprint
from flask import render_template

from models import Post, Tag, User
from .forms import PostForm, TagForm, ImageForm

from flask import request
from app import *

from flask import redirect
from flask import url_for, flash

from werkzeug.utils import secure_filename

from flask_security import login_required

posts = Blueprint('posts', __name__, template_folder='templates')



@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostForm()

    if request.method == 'POST':
        tags = form.tags.data
        tags_all = Tag.query.all()#get all tags
        tags_all_ids = []         #
        i = 1                     #
        for x in tags_all:        #
            tags_all_ids.append(i)#
            i = i + 1             #create list with id for every tag
        tags_all_dict = dict(zip(tags_all_ids, tags_all))#create dict using tags_all and tags_all_ids
        tags_ids = request.form.getlist('tags')#get ids of tags from inpyt
        tags_inpyt = []#get value in dict for tags_ids as key
        for id in tags_ids:#
            tag = tags_all_dict.get(int(id))#
            tags_inpyt.append(tag)#

        tags = list(tags_inpyt)
        title = request.form['title']
        description = request.form['description']
        body = request.form['body']
        filename = secure_filename(form.image.data.filename)
        img_url = os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename)
        form.image.data.save(img_url)
        post = Post(title=title, description=description, body=body, img_filename=filename, tags=tags)
        db.session.add(post)
        post.set_author(current_user.login)
        db.session.commit()
        post_id = post.id
        print('Post ID: '+str(post_id))
        flash("Success create post {}".format(post.title))

    taglist = Tag.query.all()
    form.tags.choices = [(g.id, g.name) for g in taglist ]
    return render_template('posts/create_post.html', form=form)

@posts.route('/create_tag', methods=['POST', 'GET'])
@login_required
def create_tag():
    tag_form = TagForm()

    if request.method == 'POST':
        if request.form['add_tag']:
            name = request.form['add_tag']
            if Tag.query.filter(Tag.name==name).first() == None:
                try:
                    tag = Tag(name=name)
                    db.session.add(tag)
                    db.session.commit()
                    tag_id = tag.id
                    print(tag_id)

                    flash('Saccess add tag {}'.format(tag.name))

                except:
                    flash('Some erors...')
            else:
                flash('This tag exist!', category=Warning)



    return render_template('posts/create_tag.html', tag_form=tag_form)

@posts.route('/add_image', methods=['POST', 'GET'])
@login_required
def add_image():
    img_form = ImageForm()
    if request.method == 'POST':
        # filename = request.form.get('add_img')
        filename = secure_filename(img_form.add_img.data.filename)
        print(filename)
        img_url = os.path.join(app.config['UPLOADS_DEFAULT_DEST_IMG'], filename)
        img_form.add_img.data.save(img_url)


        image = Image(img_filename=filename)
        db.session.add(image)
        db.session.commit()
        flash('Зображення додано!')

    return render_template('posts/add_image.html', img_form=img_form)

@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug==slug).first_or_404()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    taglist = post.tags
    form.tags.choices = [(g.id, g.name) for g in taglist ]
    return render_template('posts/edit.html', post=post, form=form)



@posts.route('/<slug>', methods=['POST', 'GET'])
def post_detail(slug):
    if request.method == 'POST':
        if request.form.get('yes'):
            post_for_del = Post.query.filter(Post.slug == slug).first_or_404()
            print(post_for_del)
            db.session.delete(post_for_del)
            db.session.commit()
            return redirect(url_for('index'))
    q = request.args.get('q')
    if q:
        page = request.args.get('page')
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)) #.all()
        posts_count = posts.count()
        if posts_count > 0:
            alert2 = 'Знайдено {}'.format(posts_count)+' дописів за запитом "{}"...'.format(q)
            pages = posts.paginate(page=page, per_page=posts_count)
            return render_template('posts/index.html', pages=pages, posts_count=posts_count, alert2=alert2)
        else:
            posts = Post.query.order_by(Post.created.desc()).all()
            
            
            return render_template('index.html', q=q)
    post = Post.query.filter(Post.slug==slug).first_or_404()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


@posts.route('tag/<slug>', methods=['POST', 'GET'])
def tag_detail(slug):
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if q:
        page = request.args.get('page')
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)) #.all()
        posts_count = posts.count()
        if posts_count > 0:
            alert2 = 'Знайдено {}'.format(posts_count)+' дописів за запитом "{}"...'.format(q)
            pages = posts.paginate(page=page, per_page=posts_count)
            return render_template('index.html', pages=pages, posts_count=posts_count, alert2=alert2)
        else:
            posts = Post.query.order_by(Post.created.desc()).all()
            
            
            return render_template('index.html', q=q)
    tag = Tag.query.filter(Tag.slug==slug).first_or_404()
    tag_slug = tag.slug
    tags = tag.posts.order_by(Post.created.desc())
    pages = tags.paginate(page=page, per_page=4)
    return render_template('posts/tag_detail.html', tag=tag, tag_slug=tag_slug, pages=pages)