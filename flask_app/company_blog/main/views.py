from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from company_blog.models import BlogCategory, BlogPost
from company_blog.main.forms import BlogCategoryForm, UpdateCategoryForm, BlogPostForm, BlogSearchForm
from company_blog import db
from company_blog.main.image_handler import add_featured_image

main = Blueprint('main', __name__)

@main.route('/category_maintenance', methods=['GET', 'POST'])
@login_required
def category_maintenance():
	page = request.args.get('page', 1, type=int)
	blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).paginate(page=page, per_page=10)
	form = BlogCategoryForm()

	if form.validate_on_submit():
		blog_category = BlogCategory(category=form.category.data)
		db.session.add(blog_category)
		db.session.commit()
		flash('ブログカテゴリが追加されました')
		return redirect(url_for('main.category_maintenance'))
	elif form.errors:
		form.category.data = ""
		flash(form.errors['category'][0])
	return render_template('category_maintenance.html', blog_categories=blog_categories, form=form)

@main.route('/<int:blog_category_id>/blog_category', methods=['GET', 'POST'])
@login_required
def blog_category(blog_category_id):
	if not current_user.is_administrator():
		abort(403)
	blog_category = BlogCategory.query.get_or_404(blog_category_id)
	form = UpdateCategoryForm(blog_category_id)

	if form.validate_on_submit():
		blog_category.category = form.category.data
		db.session.commit()
		flash('ブログカテゴリが更新されました')
		return redirect(url_for('main.category_maintenance'))
	elif request.method == 'GET':
		form.category.data = blog_category.category
	return render_template('blog_category.html', form=form)

@main.route('/<int:blog_category_id>/delete_category', methods=['GET', 'POST'])
@login_required
def delete_category(blog_category_id):
	if not current_user.is_administrator():
		abort(403)
	blog_category = BlogCategory.query.get_or_404(blog_category_id)
	db.session.delete(blog_category)
	db.session.commit()
	flash('ブログカテゴリが削除されました')
	return redirect(url_for('main.category_maintenance'))

@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
	form = BlogPostForm()
	if form.validate_on_submit():
		if form.picture.data:
			pic = add_featured_image(form.picture.data)
		else:
			pic = ''
		blog_post = BlogPost(title=form.title.data, text=form.text.data, featured_image=pic, userid=current_user.id, category_id=form.category.data, summary=form.summary.data)
		db.session.add(blog_post)
		db.session.commit()
		flash('ブログ投稿が作成されました')
		return redirect(url_for('main.blog_maintenance'))
	return render_template('create_post.html', form=form)

@main.route('/blog_maintenance', methods=["GET", "POST"])
@login_required
def blog_maintenance():
	page = request.args.get('page', 1, type=int)
	blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)
	return render_template('blog_maintenance.html', blog_posts=blog_posts)

@main.route('/<int:blog_post_id>/blog_post', methods=["GET", "POST"])
def blog_post(blog_post_id):
	blog_post = BlogPost.query.get_or_404(blog_post_id)
	return render_template('blog_post.html', post=blog_post)

@main.route('/<int:blog_post_id>/delete_post', methods=["GET", "POST"])
@login_required
def delete_post(blog_post_id):
	blog_post = BlogPost.query.get_or_404(blog_post_id)
	if blog_post.author != current_user:
		abort(403)
	db.session.delete(blog_post)
	db.session.commit()
	flash('ブログ投稿が削除されました')	
	return redirect(url_for('main.blog_maintenance'))

@main.route('/<int:blog_post_id>/update_post', methods=["GET", "POST"])
@login_required
def update_post(blog_post_id):
	blog_post = BlogPost.query.get_or_404(blog_post_id)
	if blog_post.author != current_user:
		abort(403)
	form = BlogPostForm()
	if form.validate_on_submit():
		blog_post.title = form.title.data
		if form.picture.data:
			blog_post.featured_image = add_featured_image(form.picture.data)
		blog_post.text = form.text.data
		blog_post.category_id = form.category.data
		db.session.commit()
		flash('ブログ投稿が更新されました')
		return redirect(url_for('main.blog_post', blog_post_id=blog_post.id))
	elif request.method == 'GET':
		form.title.data = blog_post.title
		form.picture.data = blog_post.featured_image
		form.text.data = blog_post.text
		form.summary.data = blog_post.summary
		form.category.data = blog_post.category_id
	return render_template('create_post.html', form=form)

@main.route('/')
def index():
	form = BlogSearchForm()

	page = request.args.get('page', 1, type=int)
	blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

	recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

	blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

	return render_template('index.html', blog_posts=blog_posts, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, form=form)

@main.route('/search', methods=["GET", "POST"])
def search():
	form = BlogSearchForm()
	searchtext = ""
	if form.validate_on_submit():
		searchtext = form.searchtext.data
	elif request.method == 'GET':
		form.searchtext.data = ""

	page = request.args.get('page', 1, type=int)
	blog_posts = BlogPost.query.filter((BlogPost.text.contains(searchtext)) | (BlogPost.title.contains(searchtext)) | (BlogPost.summary.contains(searchtext))).order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

	recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

	blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

	return render_template('index.html', blog_posts=blog_posts, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, form=form, searchtext=searchtext)

