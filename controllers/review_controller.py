"""
Review Controller
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from facade.sdu_facade import SDUFacade

review_bp = Blueprint('reviews', __name__)
facade = SDUFacade()


@review_bp.route('/add/<teacher_id>', methods=['POST'])
def add_review(teacher_id):
    """Adding a review."""
    author_name = request.form.get('author_name', 'Anonymous')
    rating = int(request.form.get('rating', 3))
    comment = request.form.get('comment', '')
    is_anonymous = request.form.get('is_anonymous') == 'on'

    if not comment.strip():
        flash('Please write a review', 'error')
        return redirect(url_for('teachers.teacher_detail', teacher_id=teacher_id))

    review = facade.add_review(
        teacher_id=teacher_id,
        author_name=author_name,
        rating=rating,
        comment=comment,
        is_anonymous=is_anonymous
    )

    flash('Your review has been submitted for moderation', 'success')
    return redirect(url_for('teachers.teacher_detail', teacher_id=teacher_id))


@review_bp.route('/api/<teacher_id>')
def get_reviews_api(teacher_id):
    """API for retrieving reviews."""
    reviews = facade.get_teacher_reviews(teacher_id)
    return jsonify([{
        'id': r.id,
        'author_name': r.author_name,
        'rating': r.rating,
        'comment': r.comment,
        'created_at': r.created_at,
        'is_anonymous': r.is_anonymous
    } for r in reviews])

