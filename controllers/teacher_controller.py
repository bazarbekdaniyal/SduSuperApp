"""
Teacher Controller
"""
from flask import Blueprint, render_template, request
from facade.sdu_facade import SDUFacade

teacher_bp = Blueprint('teachers', __name__)
facade = SDUFacade()


@teacher_bp.route('/')
def list_teachers():
    """List of teachers."""
    level = request.args.get('level')
    search = request.args.get('search')

    if search:
        teachers = facade.search_teachers(search)
    elif level:
        teachers = facade.get_teachers_by_level(level)
    else:
        teachers = facade.get_all_teachers()

    levels = facade.get_levels()

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 50
    total_teachers = len(teachers)
    total_pages = (total_teachers + per_page - 1) // per_page
    
    start = (page - 1) * per_page
    end = start + per_page
    current_teachers = teachers[start:end]

    return render_template('teachers/list.html',
                          teachers=current_teachers,
                          levels=levels,
                          current_level=level,
                          search_query=search,
                          page=page,
                          total_pages=total_pages)


@teacher_bp.route('/<teacher_id>')
def teacher_detail(teacher_id):
    """Teacher detail page."""
    info = facade.get_teacher_full_info(teacher_id)

    if not info:
        return render_template('404.html'), 404

    return render_template('teachers/detail.html',
                          teacher=info['teacher'],
                          schedule=info['schedule'],
                          reviews=info['reviews'],
                          rating=info['rating'],
                          rating_distribution=info['rating_distribution'])


@teacher_bp.route('/top')
def top_teachers():
    """Top teachers."""
    teachers = facade.get_top_teachers(20)
    return render_template('teachers/top.html', teachers=teachers)

