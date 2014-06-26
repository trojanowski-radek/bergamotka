#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid

from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Users,
    Reservations,
    News,
    Events,
    Dishes)

from datetime import datetime, timedelta

from security import groupfinder

import bookingfacade

import os
import transaction

from pyramid.security import remember
from pyramid.security import forget
from pyramid.url import route_url

import logging
log = logging.getLogger('booking')
log.debug('initialized')

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    """
    Home page view.
        request - Return top events and news to home.pt template.
    """
    try:

        logged_in = False

        logged_in = authenticated_userid(request)

        json_news = bookingfacade.getTopNews()

        json_events = bookingfacade.getTopEvents()

        return dict(news=json_news['news'] if json_news else None,
                    events=json_events['events'] if json_events else None, logged_in=logged_in)

    except DBAPIError, ex:
        print ex
        return dict(status=False, news=None, events=None, desc=ex, logged_in=False)

    except Exception, ex:
        print ex
        return dict(status=False, news=None, events=None, desc=ex, logged_in=False)


@view_config(route_name='news', renderer='templates/news.pt')
def news(request):
    """
    News page view.
        request - Return top events and news to news.pt template.
    """
    try:
        json_news = bookingfacade.getTopNews()
        json_events = bookingfacade.getTopEvents()

        return dict(news=json_news['news'] if json_news else None,
                    events=json_events['events'] if json_events else None)

    except DBAPIError, ex:
        print ex
        return dict(news=None, events=None)

    except Exception, ex:
        print ex
        return dict(news=None, events=None)


@view_config(route_name='news_add', renderer='json', permission='admin')
def news_add(request):
    """
    Add News view.
        request - Reads AJAX request and inserts news into database.
    """
    try:

        if 'title' and 'content' and 'user' in request.json_body:

            title = request.json_body['title']
            content = request.json_body['content']
            user = request.json_body['user']

            added = datetime.now()

            if 'image' in request.json_body:
                image = request.json_body['image']
                if image is not None:
                    item = News(title=title, content=content, added=added, image=image)
                else:
                    item = News(title=title, content=content, added=added)
            else:
                item = News(title=title, content=content, added=added)

            DBSession.add(item)

            transaction.commit()

            return dict(status=True)

    except DBAPIError, ex:
        print ex
        return dict(status=True, desc=ex)

    except Exception, ex:
        print ex
        return dict(status=True, desc=ex)


@view_config(route_name='news_edit', renderer='json', permission='admin')
def news_edit(request):
    """
    Edit News view.
        request - Reads AJAX request to get news data and modifies news on database.
    """
    try:

        if 'title' and 'content' and 'id' in request.json_body:

            title = request.json_body['title']
            content = request.json_body['content']
            id = request.json_body['id']

            item = DBSession.query(News).get(id)

            item.title = title
            item.content = content

            if 'image' in request.json_body:
                image = request.json_body['image']
                if len(image) > 0:
                    item.image = image

            DBSession.add(item)

            transaction.commit()

            return dict(status=True)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='news_delete', renderer='json', permission='admin')
def news_delete(request):
    """
    Delete News view.
        request - Reads AJAX request and deletes news from database.
    """
    try:
        item_id = request.json_body['id']

        if id:
            item = DBSession.query(News).get(item_id)

            if item:
                DBSession.delete(item)
                transaction.commit()
                return dict(status=True)
            else:
                return dict(status=False)

        else:
            return dict(status=False)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='news_image_upload', renderer='json', permission='admin')
def news_image_upload(request):
    """
    Uploads Image to Admin/Add News view.
        request - Reads AJAX request to get reservation data and inserts reservation into database.
    """

    filename = request.POST['...'].filename

    if any(filename.lower().endswith(extension) for extension in ('.jpg', '.gif', '.bmp', '.gif', '.png')):

        input_file = request.POST['...'].file

        saved_image = bookingfacade.upload_image(input_file=input_file, folder='news')

        return saved_image

    else:
        return "Cannot upload file with extension another than: '.jpg' or '.bmp' or '.gif' or '.png'."


@view_config(route_name='calendar', renderer='templates/calendar.pt')
def calendar(request):
    """
    Calendar page view (for this moment its just plain view - do not nothing else generating template).
        Returns top events and news to news.pt template.
    """
    return dict(status=True)


@view_config(route_name='events_view', renderer='json')
def events_view(request):
    """
    Events view.
        request - Reads AJAX request to get times for query.
        Returns list of events for given date range.
    """
    try:

        if 'start' and 'end' in request.params:
            datetime_start = datetime.fromtimestamp(int(request.params['start']))
            datetime_end = datetime.fromtimestamp(int(request.params['end']))

            events = DBSession.query(Events.id, Events.date_start, Events.date_end, Events.title).filter(
                Events.date_start.between(datetime_start, datetime_end)).all()

            return [dict(id=item.id, title=item.title, start=str(item.date_start), end=str(item.date_end), allDay=False)
                    for item in events]

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='events_add', renderer='json', permission='admin')
def events_add(request):
    """
    Add Events view.
        request - Reads AJAX request to get event data and inserts event into database.
    """
    try:

        if 'date_start' and 'date_end' and 'title' and 'user' in request.json_body:
            date_start = request.json_body['date_start']
            date_end = request.json_body['date_end']
            title = request.json_body['title']
            user = request.json_body['user']

            item = Events(date_start=date_start, date_end=date_end, title=title, user=user)

            DBSession.add(item)

            transaction.commit()

            return dict(status=True)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='events_edit', renderer='json', permission='admin')
def events_edit(request):
    """
    Edit Events view.
        request - Reads AJAX request to get event data and modifies event on database.
    """
    try:

        if 'date_start' and 'date_end' and 'title' and 'id' in request.json_body:
            date_start = request.json_body['date_start']
            date_end = request.json_body['date_end']
            title = request.json_body['title']
            event_id = request.json_body['id']

            item = DBSession.query(Events).get(event_id)

            item.date_start = date_start
            item.date_end = date_end
            item.title = title

            DBSession.add(item)

            transaction.commit()

            return dict(status=True)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='events_delete', renderer='json', permission='admin')
def events_delete(request):
    """
    Delete Events view.
        request - Reads AJAX request to get event ID and deletes this event from database.
    """
    try:
        event_id = request.json_body['id']

        if id:
            item = DBSession.query(Events).get(event_id)

            if item:
                DBSession.delete(item)
                transaction.commit()
                return dict(status=True)
            else:
                return dict(status=False)

        else:
            return dict(status=False)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='reservations', renderer='templates/reservations.pt')
def reservations(request):
    """
    Reservations view (for this moment its just plain view - do not nothing else generating template).
    """
    return dict(status=True)


@view_config(route_name='reservations_add', renderer='json')
def reservations_add(request):
    """
    Add Reservations view.
        request - Reads AJAX request to get reservation data and inserts reservation into database.
    """
    try:

        if 'date_start' and 'date_end' and 'title' and 'email' and 'phone' in request.json_body:
            date_start = request.json_body['date_start']
            date_end = request.json_body['date_end']
            title = request.json_body['title']
            email = request.json_body['email']
            phone = request.json_body['phone']

            item = Reservations(date_start=date_start, date_end=date_end, title=title, user=email, phone=phone)

            DBSession.add(item)

            transaction.commit()

            return dict(status=True)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='reservations_edit', renderer='json', permission='admin')
def reservations_edit(request):
    """
    Edit reservations view.
        request - Reads AJAX request to get reservation data and modifies dish on database.
    """
    try:

        if 'time_start' and 'time_end' and 'title' and 'email' and 'phone' and 'id' and 'date' in request.json_body:

            time_start = request.json_body['time_start']
            time_end = request.json_body['time_end']
            title = request.json_body['title']
            email = request.json_body['email']
            phone = request.json_body['phone']
            id = request.json_body['id']
            date = request.json_body['date']

            item = DBSession.query(Reservations).get(id)

            item.title = title
            item.date_start = '%s %s' % (date, time_start)
            item.date_end = '%s %s' % (date, time_end)
            item.user = email
            item.phone = phone

            DBSession.add(item)

            transaction.commit()

            return dict(status=True)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='reservations_delete', renderer='json', permission='admin')
def reservations_delete(request):
    """
    Delete Reservations view.
        request - Reads AJAX request to get reservation ID and deletes this reservation from database.
    """
    try:
        reservation_id = request.json_body['id']

        if id:
            item = DBSession.query(Reservations).get(reservation_id)

            if item:
                DBSession.delete(item)
                transaction.commit()
                return dict(status=True)
            else:
                return dict(status=False)

        else:
            return dict(status=False)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='gallery', renderer='templates/gallery.pt')
def gallery(request):
    """
    Gallery view (for this moment its just plain view - do not nothing else generating template).
    """

    try:

        from os import listdir
        from os.path import isfile, join
        here = os.getcwd()
        folder_path = os.path.normpath(os.path.join(here, '..', 'bergamotka', 'src', 'booking', 'gallery'))

        onlyfiles = ['/gallery/%s' % f for f in listdir(folder_path) if isfile(join(folder_path, f)) and 'thumb' not in f]

        if len(onlyfiles) > 0:
            return dict(status=True, files=sorted(onlyfiles, reverse=True))
        else:
            return dict(status='No images have been uploaded yet.', files=None)

    except Exception, ex:
        print ex
        return dict(status=False, files=[])


@view_config(route_name='gallery_upload', renderer='json', permission='admin')
def gallery_upload(request):
    """Uploads Image to Admin/Add Gallery view."""

    filename = request.POST['...'].filename

    if any(filename.lower().endswith(extension) for extension in ('.jpg', '.gif', '.bmp', '.gif', '.png')):

        input_file = request.POST['...'].file

        saved_image = bookingfacade.upload_image(input_file=input_file)

        return saved_image

    else:
        return "Cannot upload file with extension another than: '.jpg' or '.bmp' or '.gif' or '.png'."


@view_config(route_name='dishes', renderer='templates/dishes.pt')
def dishes(request):
    """
    Dishes page view.
        request - Return all dishes to news.pt template.
    """
    try:

        all_dishes = bookingfacade.getAllDishes()

        types = []

        grouped_dishes = dict()

        for dish in all_dishes.get('dishes'):
            if dish.get('type') not in types:
                types.append(dish.get('type'))
                grouped_dishes[dish.get('type')] = []

        for dish in all_dishes.get('dishes'):
            for type in types:
                if dish.get('type') == type:
                    grouped_dishes[dish.get('type')].append(dish)

        if grouped_dishes:
            return dict(dishesall=grouped_dishes, status=True)
        else:
            return dict(status=True)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='dishes_add', renderer='json', permission='admin')
def dishes_add(request):
    """
    Add Dishes view.
        request - Reads AJAX request and inserts dish into database.
    """
    try:

        if 'title' and 'ingredients' and 'price' and 'type' in request.json_body:

            title = request.json_body['title']
            ingredients = request.json_body['ingredients']
            price = request.json_body['price']
            type = request.json_body['type']
            if 'image' in request.json_body:
                image = request.json_body['image']
                item = Dishes(title=title, ingredients=ingredients, price=price, type=type, image=image)
            else:
                item = Dishes(title=title, ingredients=ingredients, price=price, type=type)

            DBSession.add(item)

            transaction.commit()

            return dict(status=True)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='dishes_image_upload', renderer='json', permission='admin')
def dishes_image_upload(request):
    """
    Uploads Image to Admin/Add Dishes view.
        request - Reads AJAX request to get reservation data and inserts reservation into database.
    """

    filename = request.POST['...'].filename

    if any(filename.lower().endswith(extension) for extension in ('.jpg', '.gif', '.bmp', '.gif', '.png')):

        input_file = request.POST['...'].file

        saved_image = bookingfacade.upload_image(input_file=input_file, folder='dishes')

        return saved_image

    else:
        return "Cannot upload file with extension another than: '.jpg' or '.bmp' or '.gif' or '.png'."


@view_config(route_name='dishes_edit', renderer='json', permission='admin')
def dishes_edit(request):
    """
    Edit Dishes view.
        request - Reads AJAX request to get dish data and modifies dish on database.
    """
    try:

        if 'title' and 'ingredients' and 'price' and 'type' and 'id' in request.json_body:

            title = request.json_body['title']
            ingredients = request.json_body['ingredients']
            price = request.json_body['price']
            type = request.json_body['type']
            id = request.json_body['id']

            item = DBSession.query(Dishes).get(id)

            item.title = title
            item.ingredients = ingredients
            item.price = price
            item.type = type

            if 'image' in request.json_body:
                image = request.json_body['image']
                if len(image) > 0:
                    item.image = image

            DBSession.add(item)

            transaction.commit()

            return dict(status=True)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='dishes_delete', renderer='json', permission='admin')
def dishes_delete(request):
    """
    Delete Dishes view.
        request - Reads AJAX request and deletes dishes from database.
    """
    try:
        item_id = request.json_body['id']

        if id:
            item = DBSession.query(Dishes).get(item_id)

            if item:
                DBSession.delete(item)
                transaction.commit()
                return dict(status=True)
            else:
                return dict(status=False)

        else:
            return dict(status=False)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='admin', renderer='templates/admin.pt', permission='admin')
def admin(request):
    """
    Admin view.
        Returns lists of:
        1) events
        2) news
        3) reservations
    """
    try:

        logged_in = authenticated_userid(request)

        all_news = bookingfacade.getAllNews()

        all_events = bookingfacade.getAllEvents()

        all_reservations = bookingfacade.getAllReservations()

        today_reservations = bookingfacade.getTodayReservations()

        all_dishes = bookingfacade.getAllDishes()

        if all([all_events, all_news, all_reservations, today_reservations, all_dishes]):
            return dict(newsall=all_news, eventsall=all_events, reservationsall=all_reservations,
                        reservationstoday=today_reservations, logged_in=logged_in, dishesall=all_dishes)

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='about', renderer='templates/about.pt')
def about(request):
    """
    About view (for this moment its just plain view - do not nothing else generating template).
    """
    return dict(status=True)


@view_config(route_name='login', renderer='templates/dialogs/login.pt')
def login(request):
    """
    Login view.
        request - Reads AJAX request to get user data and checks permissions on database.
    """
    try:

        login_url = route_url('login', request)

        referrer = request.url

        if referrer == login_url:
            referrer = '/'

        came_from = request.params.get('came_from', referrer)

        message = ''
        email = ''
        password = ''

        if 'form.submitted' in request.params:

            login = request.params['login']
            password = request.params['password']

            permissions = groupfinder(login, password, request)

            if permissions is None:
                message = 'BŁĘDNE HASŁO.'
            elif permissions is []:
                message = 'UŻYTKOWNIK %s NIE JEST ZAREJESTROWANY.' % email
            elif 'permission:' in permissions:
                headers = remember(request, permissions)

                response = HTTPFound(location=came_from, headers=headers)

                #Add user cookie
                response.set_cookie('user', value=login, max_age=31536000)

                return response

        return dict(
            message=message,
            url=request.application_url + '/login',
            came_from=came_from,
            login=email,
            password=password, )

    except DBAPIError, ex:
        print ex
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    except Exception, ex:
        print ex
        return Response(ex, content_type='text/plain', status_int=500)


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    response = HTTPFound(location=route_url('home', request),
                     headers=headers)
    response.delete_cookie('user')
    return response


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_booking_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""