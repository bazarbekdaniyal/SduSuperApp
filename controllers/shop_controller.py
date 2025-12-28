"""
Shop Controller
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from facade.sdu_facade import SDUFacade
from utils.data_i18n import get_translated_product, get_translated_products_list
from utils.i18n import DEFAULT_LANGUAGE, get_translation

shop_bp = Blueprint('shop', __name__)
facade = SDUFacade()


@shop_bp.route('/')
def list_products():
    """Product catalog."""
    category = request.args.get('category')
    search = request.args.get('search')
    lang = session.get('language', DEFAULT_LANGUAGE)

    if search:
        products = facade.search_products(search)
    elif category:
        products = facade.get_products_by_category(category)
    else:
        products = facade.get_products()

    # Translate products
    translated_products = get_translated_products_list(products, lang)

    categories = facade.get_product_categories()

    cart = session.get('cart', [])
    cart_product_ids = [item['product_id'] for item in cart]

    return render_template('shop/list.html',
                          products=translated_products,
                          categories=categories,
                          current_category=category,
                          search_query=search,
                          cart_product_ids=cart_product_ids)


@shop_bp.route('/product/<product_id>')
def product_detail(product_id):
    """Product page."""
    product = facade.get_product(product_id)

    if not product:
        return render_template('404.html'), 404

    lang = session.get('language', DEFAULT_LANGUAGE)
    translated_product = get_translated_product(product, lang)

    cart = session.get('cart', [])
    cart_product_ids = [item['product_id'] for item in cart]

    return render_template('shop/detail.html', product=translated_product, cart_product_ids=cart_product_ids)


@shop_bp.route('/cart')
def cart():
    """Shopping cart."""
    cart_items = session.get('cart', [])
    lang = session.get('language', DEFAULT_LANGUAGE)

    # Get product details
    items_with_details = []
    total = 0

    for item in cart_items:
        product = facade.get_product(item['product_id'])
        if product:
            subtotal = product.price * item['quantity']
            translated_product = get_translated_product(product, lang)
            items_with_details.append({
                'product': translated_product,
                'quantity': item['quantity'],
                'subtotal': subtotal
            })
            total += subtotal

    return render_template('shop/cart.html',
                          items=items_with_details,
                          total=total)


@shop_bp.route('/cart/add/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add to cart."""
    lang = session.get('language', DEFAULT_LANGUAGE)
    quantity = int(request.form.get('quantity', 1))

    product = facade.get_product(product_id)
    if not product:
        flash(get_translation('shop.errors.product_not_found', lang), 'error')
        return redirect(url_for('shop.list_products'))

    cart = session.get('cart', [])

    # Check if already in cart
    found = False
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            found = True
            break

    if not found:
        cart.append({'product_id': product_id, 'quantity': quantity})

    session['cart'] = cart
    translated_product = get_translated_product(product, lang)
    product_name = translated_product['name']
    flash(get_translation('shop.messages.product_added', lang, product_name=product_name), 'success')

    return redirect(url_for('shop.list_products'))


@shop_bp.route('/cart/remove/<product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Remove from cart."""
    lang = session.get('language', DEFAULT_LANGUAGE)
    cart = session.get('cart', [])
    cart = [item for item in cart if item['product_id'] != product_id]
    session['cart'] = cart

    flash(get_translation('shop.messages.product_removed', lang), 'success')
    return redirect(url_for('shop.cart'))


@shop_bp.route('/cart/update/<product_id>', methods=['POST'])
def update_cart(product_id):
    """Update quantity."""
    quantity = int(request.form.get('quantity', 1))

    cart = session.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] = max(1, quantity)
            break

    session['cart'] = cart
    return redirect(url_for('shop.cart'))


@shop_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout."""
    lang = session.get('language', DEFAULT_LANGUAGE)
    cart_items = session.get('cart', [])

    if not cart_items:
        flash(get_translation('shop.errors.cart_empty', lang), 'error')
        return redirect(url_for('shop.list_products'))

    if request.method == 'POST':
        customer_name = request.form.get('name', '').strip()
        customer_email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()

        # Check all required fields are filled
        if not customer_name or not customer_email or not address:
            flash(get_translation('shop.errors.fill_required_fields', lang), 'error')
            return redirect(url_for('shop.checkout'))

        # Get user language from session
        lang = session.get('language', DEFAULT_LANGUAGE)
        order = facade.create_order(customer_name, customer_email, cart_items, address, language=lang)

        if order:
            session['cart'] = []  # Clear cart
            flash(get_translation('shop.errors.order_success', lang), 'success')
            return render_template('shop/order_success.html', order=order)
        else:
            flash(get_translation('shop.errors.order_error', lang), 'error')

    # Calculate total
    total = facade.calculate_cart(cart_items)
    lang = session.get('language', DEFAULT_LANGUAGE)

    # Get products for display
    items = []
    for item in cart_items:
        product = facade.get_product(item['product_id'])
        if product:
            translated_product = get_translated_product(product, lang)
            items.append({
                'product': translated_product,
                'quantity': item['quantity'],
                'subtotal': product.price * item['quantity']
            })

    return render_template('shop/checkout.html', items=items, total=total)


@shop_bp.route('/orders')
def my_orders():
    """My orders."""
    email = request.args.get('email')

    if not email:
        return render_template('shop/find_orders.html')

    orders = facade.get_customer_orders(email)
    return render_template('shop/orders.html', orders=orders, email=email)

