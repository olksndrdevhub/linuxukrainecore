from app import app
from flask import render_template, request
from models import Post, Tag

@app.route('/')
def index():
    if Post.query.first():
        tags = Tag.query.all()

        page = request.args.get('page')
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1
        posts = Post.query.order_by(Post.created.desc())

        tag_guides = Tag.query.filter(Tag.name=='гайди').first_or_404()
        guides = tag_guides.posts.order_by(Post.created.desc()).all()
        last_guides = guides[-3:]
        last_guides.reverse()
        q = request.args.get('q')

        if q:
            posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
            posts_count = posts.count()
            if posts_count > 0:
                alert2 = 'Знайдено {}'.format(posts_count)+' дописів за запитом "{}"...'.format(q)
                pages = posts.paginate(page=page, per_page=posts_count)
                return render_template('index.html', pages=pages, posts_count=posts_count, tags=tags, alert2=alert2, last_guides=last_guides)
            else:
                return render_template('index.html', q=q)
        pages = posts.paginate(page=page, per_page=4)


        return render_template('index.html', q=q, tags=tags, pages=pages, last_guides=last_guides)
    else:

        return render_template('no_posts.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@app.route('/programs/')
def programs(slug='програми'):
    tag = Tag.query.filter(Tag.slug==slug).first()
    if tag:
        tags = Tag.query.all()
        posts = Post.query.order_by(Post.created.desc())
        posts = tag.posts.order_by(Post.created.desc())
        posts_c = tag.posts.count()
        page = request.args.get('page')
        pages = posts.paginate(page=page, per_page=4)
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1
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
                return render_template('index.html', pages=pages, posts_count=posts_count, tags=tags, alert2=alert2)
            else:
                posts = Post.query.order_by(Post.created.desc()).all()
                return render_template('index.html', q=q)
        return render_template('programs.html', tag=tag, pages=pages, posts_c=posts_c)
    else:
        return render_template('no_posts.html')

@app.route('/news/')
def news(slug='новини'):
    tag = Tag.query.filter(Tag.slug==slug).first()
    if tag:
        tags = Tag.query.all()
        page = request.args.get('page')
        posts = Post.query.order_by(Post.created.desc())
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1
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
                return render_template('index.html', pages=pages, posts_count=posts_count, tags=tags, alert2=alert2)
            else:
                posts = Post.query.order_by(Post.created.desc()).all()


                return render_template('index.html', q=q)


        tag = Tag.query.filter(Tag.slug==slug).first_or_404()
        posts = tag.posts.order_by(Post.created.desc())
        posts_c = tag.posts.count()
        pages = posts.paginate(page=page, per_page=4)

        return render_template('news.html', tag=tag, pages=pages, posts_c=posts_c)
    else:
        return render_template('no_posts.html')

@app.route('/guides/', methods=['POST', 'GET'])
def guides(slug='гайди'):
    tag = Tag.query.filter(Tag.slug==slug).first()
    if  tag:
        tags = Tag.query.all()
        page = request.args.get('page')
        posts = Post.query.order_by(Post.created.desc())
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1
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
                return render_template('index.html', pages=pages, posts_count=posts_count, tags=tags, alert2=alert2)
            else:
                posts = Post.query.order_by(Post.created.desc()).all()


                return render_template('index.html', q=q)



        tag = Tag.query.filter(Tag.slug==slug).first_or_404()
        posts = tag.posts.order_by(Post.created.desc())
        posts_c = tag.posts.count()
        pages = posts.paginate(page=page, per_page=4)
        return render_template('guides.html', tag=tag, pages=pages, posts_c=posts_c)
    else:
        return render_template('no_posts.html')
@app.route('/about')
def about():
    q = request.args.get('q')
    if q:
        tags = Tag.query.all()
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
            return render_template('index.html', pages=pages, posts_count=posts_count, tags=tags, alert2=alert2)
        else:
            posts = Post.query.order_by(Post.created.desc()).all()
            return render_template('index.html', q=q)
    return render_template('contacts.html')