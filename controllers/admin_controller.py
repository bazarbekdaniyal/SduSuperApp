"""
Admin Panel Controller
"""
import os
import uuid
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from facade.sdu_facade import SDUFacade
from services.teacher_service import TeacherService
from services.news_service import NewsService
from services.shop_service import ShopService
from repository.subscriber_repository import SubscriberRepository

admin_bp = Blueprint('admin', __name__)
facade = SDUFacade()


# File upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOAD_FOLDER = 'static/uploads'


def allowed_file(filename):
    """Checks for allowed file extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_image(file, subfolder):
    """Saves uploaded file and returns URL."""
    if file and file.filename and allowed_file(file.filename):
        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"

        # Path for saving
        upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, subfolder)
        os.makedirs(upload_path, exist_ok=True)

        filepath = os.path.join(upload_path, filename)
        file.save(filepath)

        # Return URL for accessing the file
        return f"/{UPLOAD_FOLDER}/{subfolder}/{filename}"
    return None


def login_required(f):
    """Decorator for admin authorization check."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin panel login page."""
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == current_app.config['ADMIN_USERNAME'] and password == current_app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Welcome to the admin panel!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid login or password', 'error')

    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    """Logout from admin panel."""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('admin.login'))


@admin_bp.route('/')
@login_required
def dashboard():
    """Admin Dashboard."""
    stats = facade.get_dashboard_stats()
    pending_reviews = facade.get_pending_reviews()
    pending_orders = facade.get_pending_orders()

    # Create dictionary of teachers for displaying full names
    teachers_dict = {}
    all_teachers = facade.get_all_teachers()
    for teacher in all_teachers:
        teachers_dict[teacher.id] = teacher

    return render_template('admin/dashboard.html',
                          stats=stats,
                          pending_reviews=pending_reviews[:5],
                          pending_orders=pending_orders[:5],
                          teachers=teachers_dict)


@admin_bp.route('/reviews')
@login_required
def reviews():
    """Review Moderation."""
    pending = facade.get_pending_reviews()

    # Create dictionary of teachers for displaying full names
    teachers_dict = {}
    all_teachers = facade.get_all_teachers()
    for teacher in all_teachers:
        teachers_dict[teacher.id] = teacher

    return render_template('admin/reviews.html', reviews=pending, teachers=teachers_dict)


@admin_bp.route('/reviews/approve/<review_id>', methods=['POST'])
@login_required
def approve_review(review_id):
    """Approving a review."""
    facade.approve_review(review_id)
    flash('Review approved', 'success')
    return redirect(url_for('admin.reviews'))


@admin_bp.route('/reviews/reject/<review_id>', methods=['POST'])
@login_required
def reject_review(review_id):
    """Rejecting a review."""
    facade.reject_review(review_id)
    flash('Review rejected', 'success')
    return redirect(url_for('admin.reviews'))


@admin_bp.route('/reviews/delete/<review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    """Deleting a review."""
    # Get teacher_id for redirect (optional)
    redirect_url = request.form.get('redirect_url')

    facade.delete_review(review_id)
    flash('Review deleted', 'success')

    if redirect_url:
        return redirect(redirect_url)
    return redirect(url_for('admin.reviews'))


@admin_bp.route('/teachers')
@login_required
def teachers():
    """Teacher Management."""
    all_teachers = facade.get_all_teachers()
    return render_template('admin/teachers.html', teachers=all_teachers)


@admin_bp.route('/teachers/add', methods=['GET', 'POST'])
@login_required
def add_teacher():
    """Adding a teacher."""
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'department': request.form.get('department'),
            'position': request.form.get('position'),
            'email': request.form.get('email'),
            'bio': request.form.get('bio'),
            'subjects': request.form.get('subjects', '').split(',')
        }

        service = TeacherService()
        service.create_teacher(data)
        flash('Teacher added', 'success')
        return redirect(url_for('admin.teachers'))

    return render_template('admin/teacher_form.html', teacher=None)


@admin_bp.route('/news')
@login_required
def news():
    """News Management."""
    service = NewsService()
    all_news = service._news_repo.get_all()
    # Sort by date - newest first
    all_news = sorted(all_news, key=lambda n: n.created_at, reverse=True)
    return render_template('admin/news.html', news=all_news)


@admin_bp.route('/news/add', methods=['GET', 'POST'])
@login_required
def add_news():
    """Adding news."""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        author = request.form.get('author', 'Admin')
        publish = request.form.get('publish') == 'on'

        # Image processing
        image = None
        # First check uploaded file
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                image = save_uploaded_image(file, 'news')

        # If file not uploaded, check URL
        if not image:
            image_url = request.form.get('image_url', '').strip()
            if image_url:
                image = image_url

        service = NewsService()
        service.create_news(title, content, category, author, image=image, publish=publish)
        flash('News added', 'success')
        return redirect(url_for('admin.news'))

    return render_template('admin/news_form.html', news_item=None)


@admin_bp.route('/news/edit/<news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    """Editing news."""
    service = NewsService()
    news_item = service.get_news_by_id(news_id)

    if not news_item:
        flash('News not found', 'error')
        return redirect(url_for('admin.news'))

    if request.method == 'POST':
        # Image processing
        image = news_item.image  # Save current by default

        # Check if image needs to be removed
        if request.form.get('remove_image') == 'yes':
            image = None
        else:
            # Check uploaded file
            if 'image_file' in request.files:
                file = request.files['image_file']
                if file and file.filename:
                    image = save_uploaded_image(file, 'news')

            # If file not uploaded, check URL
            if image == news_item.image:
                image_url = request.form.get('image_url', '').strip()
                if image_url:
                    image = image_url

        data = {
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'category': request.form.get('category'),
            'author': request.form.get('author', 'Admin'),
            'image': image,
            'is_published': request.form.get('publish') == 'on'
        }

        service.update_news(news_id, data)
        flash('News updated', 'success')
        return redirect(url_for('admin.news'))

    return render_template('admin/news_form.html', news_item=news_item)


@admin_bp.route('/news/delete/<news_id>', methods=['POST'])
@login_required
def delete_news(news_id):
    """Deleting news."""
    service = NewsService()
    if service.delete_news(news_id):
        flash('News deleted', 'success')
    else:
        flash('Error deleting news', 'error')
    return redirect(url_for('admin.news'))


@admin_bp.route('/orders')
@login_required
def orders():
    """Order Management."""
    service = ShopService()
    all_orders = service._order_repo.get_all()
    all_orders.sort(key=lambda o: o.created_at, reverse=True)
    return render_template('admin/orders.html', orders=all_orders)


@admin_bp.route('/orders/confirm/<order_id>', methods=['POST'])
@login_required
def confirm_order(order_id):
    """Confirming an order."""
    facade.confirm_order(order_id)
    flash('Order confirmed', 'success')
    return redirect(url_for('admin.orders'))


@admin_bp.route('/orders/cancel/<order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Cancelling an order."""
    facade.cancel_order(order_id)
    flash('Order cancelled', 'success')
    return redirect(url_for('admin.orders'))


@admin_bp.route('/products')
@login_required
def products():
    """Product Management."""
    service = ShopService()
    all_products = service._product_repo.get_all()
    return render_template('admin/products.html', products=all_products)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """Adding a product."""
    if request.method == 'POST':
        # Image processing
        image = None
        # First check uploaded file
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                image = save_uploaded_image(file, 'products')

        # If file not uploaded, check URL
        if not image:
            image_url = request.form.get('image_url', '').strip()
            if image_url:
                image = image_url

        data = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': float(request.form.get('price', 0)),
            'category': request.form.get('category'),
            'stock': int(request.form.get('stock', 0)),
            'image': image,
            'is_available': request.form.get('is_available') == 'yes'
        }

        service = ShopService()
        service.create_product(data)
        flash('Product added', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', product=None)


@admin_bp.route('/products/edit/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """Editing a product."""
    service = ShopService()
    product = service.get_product_by_id(product_id)

    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('admin.products'))

    if request.method == 'POST':
        # Image processing
        image = product.image  # Save current by default

        # Check if image needs to be removed
        if request.form.get('remove_image') == 'yes':
            image = None
        else:
            # Check uploaded file
            if 'image_file' in request.files:
                file = request.files['image_file']
                if file and file.filename:
                    image = save_uploaded_image(file, 'products')

            # If file not uploaded, check URL
            if image == product.image:
                image_url = request.form.get('image_url', '').strip()
                if image_url:
                    image = image_url

        data = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': float(request.form.get('price', 0)),
            'category': request.form.get('category'),
            'stock': int(request.form.get('stock', 0)),
            'image': image,
            'is_available': request.form.get('is_available') == 'yes'
        }

        service.update_product(product_id, data)
        flash('Product updated', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', product=product)


@admin_bp.route('/products/delete/<product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    """Deleting a product."""
    service = ShopService()
    if service.delete_product(product_id):
        flash('Product deleted', 'success')
    else:
        flash('Error deleting product', 'error')
    return redirect(url_for('admin.products'))


# ==========================================
# Subscriber Management
# ==========================================

@admin_bp.route('/subscribers')
@login_required
def subscribers():
    """Subscriber Management."""
    repo = SubscriberRepository()
    all_subscribers = repo.get_all()
    active_count = len([s for s in all_subscribers if s.is_active])
    return render_template('admin/subscribers.html',
                          subscribers=all_subscribers,
                          active_count=active_count)


@admin_bp.route('/subscribers/toggle/<subscriber_id>', methods=['POST'])
@login_required
def toggle_subscriber(subscriber_id):
    """Toggle subscriber activation/deactivation."""
    repo = SubscriberRepository()
    subscriber = repo.get_by_id(subscriber_id)

    if subscriber:
        if subscriber.is_active:
            repo.deactivate(subscriber_id)
            flash('Subscriber deactivated', 'success')
        else:
            repo.activate(subscriber_id)
            flash('Subscriber activated', 'success')
    else:
        flash('Subscriber not found', 'error')

    return redirect(url_for('admin.subscribers'))


@admin_bp.route('/subscribers/delete/<subscriber_id>', methods=['POST'])
@login_required
def delete_subscriber(subscriber_id):
    """Deleting a subscriber."""
    repo = SubscriberRepository()
    if repo.delete(subscriber_id):
        flash('Subscriber deleted', 'success')
    else:
        flash('Error deleting subscriber', 'error')
    return redirect(url_for('admin.subscribers'))


@admin_bp.route('/subscribers/edit/<subscriber_id>', methods=['GET', 'POST'])
@login_required
def edit_subscriber(subscriber_id):
    """Editing a subscriber."""
    repo = SubscriberRepository()
    subscriber = repo.get_by_id(subscriber_id)

    if not subscriber:
        flash('Subscriber not found', 'error')
        return redirect(url_for('admin.subscribers'))

    if request.method == 'POST':
        subscriber.name = request.form.get('name', subscriber.name)
        subscriber.email = request.form.get('email', subscriber.email)
        subscriber.is_active = request.form.get('is_active') == 'yes'
        subscriber.language = request.form.get('language', subscriber.language or 'ru')

        categories = request.form.getlist('categories')
        if categories:
            subscriber.categories = categories
        else:
            subscriber.categories = ['all']

        repo.update(subscriber)
        
        # Update observer in NewsService
        from facade.sdu_facade import SDUFacade
        facade = SDUFacade()
        facade.update_subscriber_observer(subscriber.id)
        
        flash('Subscriber updated', 'success')
        return redirect(url_for('admin.subscribers'))

    return render_template('admin/subscriber_form.html', subscriber=subscriber)


