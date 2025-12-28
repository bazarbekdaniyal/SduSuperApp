"""
Room Controller (available classrooms)
Adapted for working with real SDU data
"""
from flask import Blueprint, render_template, request, jsonify, session
from facade.sdu_facade import SDUFacade
from datetime import datetime
from models.room import TIME_SLOTS
from utils.i18n import get_days_of_week, DEFAULT_LANGUAGE, get_translation

room_bp = Blueprint('rooms', __name__)
facade = SDUFacade()


@room_bp.route('/')
def list_rooms():
    """List of available rooms."""
    week_id = request.args.get('day', type=int)
    time = request.args.get('time')
    building = request.args.get('building')

    # If day/time not specified, use current
    now = datetime.now()

    if not week_id:
        week_id = now.weekday() + 1  # 1-6 (Monday-Saturday)
        if week_id == 7:  # Weekend - always rest
            week_id = 1

    if not time:
        current_time = now.strftime('%H:%M')
        # Find nearest slot
        time = TIME_SLOTS[0][0]
        for start, end in TIME_SLOTS:
            if current_time <= start:
                time = start
                break

    free_cabinets = facade.get_free_cabinets(week_id, time, building)
    buildings = facade.get_buildings()
    time_slots = [slot[0] for slot in TIME_SLOTS]
    lang = session.get('language', DEFAULT_LANGUAGE)
    days = get_days_of_week(lang)

    return render_template('rooms/list.html',
                          cabinets=free_cabinets,
                          buildings=buildings,
                          days=days,
                          time_slots=time_slots,
                          current_day=week_id,
                          current_time=time,
                          current_building=building)


@room_bp.route('/search')
def search_cabinets():
    """Search rooms by name."""
    query = request.args.get('q', '').strip()

    if not query:
        return render_template('rooms/search.html',
                              cabinets=[],
                              query='',
                              buildings=facade.get_buildings())

    cabinets = facade.search_cabinets(query)

    return render_template('rooms/search.html',
                          cabinets=cabinets,
                          query=query,
                          buildings=facade.get_buildings())


@room_bp.route('/schedule/<int:cabinet_id>')
def cabinet_schedule(cabinet_id):
    """Room schedule."""
    cabinet = facade.get_cabinet_by_id(cabinet_id)

    if not cabinet:
        return render_template('404.html'), 404

    schedule = facade.get_cabinet_schedule(cabinet_id)

    # Organize schedule by slots
    schedule_grid = {}
    for start, end in TIME_SLOTS:
        schedule_grid[(start, end)] = {day: None for day in range(1, 7)}

    for lesson in schedule:
        slot_key = (lesson.start_time, lesson.end_time)
        if slot_key in schedule_grid:
            schedule_grid[slot_key][lesson.week_id] = lesson

    lang = session.get('language', DEFAULT_LANGUAGE)
    days = get_days_of_week(lang)

    return render_template('rooms/schedule.html',
                          cabinet=cabinet,
                          schedule_grid=schedule_grid,
                          time_slots=TIME_SLOTS,
                          days=days)


@room_bp.route('/api/search')
def api_search_cabinets():
    """API search cabinets"""
    query = request.args.get('q', '').strip()

    if not query or len(query) < 2:
        return jsonify([])

    cabinets = facade.search_cabinets(query)

    return jsonify([{
        'id': c.id,
        'name': c.name,
        'building': c.parent_building_en
    } for c in cabinets[:20]])


@room_bp.route('/current')
def current_free_rooms():
    """Rooms available now."""
    building = request.args.get('building')
    cabinets = facade.get_current_free_cabinets(building)
    buildings = facade.get_buildings()

    now = datetime.now()
    week_id = now.weekday() + 1
    current_time = now.strftime('%H:%M')

    is_weekend = week_id == 7
    lang = session.get('language', DEFAULT_LANGUAGE)
    days = get_days_of_week(lang)

    # If weekend, don't show day in header
    if week_id == 7:
        current_day = ''
    else:
        current_day = days.get(week_id, '')

    return render_template('rooms/current.html',
                          cabinets=cabinets,
                          buildings=buildings,
                          current_day=current_day,
                          current_time=current_time,
                          current_building=building,
                          is_weekend=is_weekend)


@room_bp.route('/next')
def next_slot_free_rooms():
    """Rooms available for next lesson."""
    building = request.args.get('building')
    week_id, time, cabinets = facade.get_next_slot_free_cabinets(building)
    buildings = facade.get_buildings()
    lang = session.get('language', DEFAULT_LANGUAGE)
    days = get_days_of_week(lang)

    return render_template('rooms/next.html',
                          cabinets=cabinets,
                          buildings=buildings,
                          week_id=week_id,
                          day_name=days.get(week_id, ''),
                          time=time,
                          current_building=building)
