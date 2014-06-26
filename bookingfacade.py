from .models import (
    DBSession,
    Reservations,
    News,
    Events,
    Dishes)

from datetime import datetime, timedelta, date

from sqlalchemy import and_

import os
import uuid
import shutil

import Image
import ImageOps

import logging

log = logging.getLogger(__name__)

IMAGE_EXTENSION = 'JPEG'
IMAGE_FORMAT = (1600, 1200)

THUMBNAIL_EXTENSION = 'JPEG'
THUMBNAIL_FORMAT = (400, 280)

def getAllNews():
    """
        Gets all news from database.
    """
    try:
        news = DBSession.query(News.title, News.added, News.content, News.id, News.image).order_by(News.added.desc()).all()

        json_news = []

        if news:
            json_news.extend(dict(title=item.title, added=unicode(item.added), content=item.content, id=item.id,
                                  image=item.image or None) for item in news)

            return dict(status=True, news=json_news)

        else:
            return dict(status=False, desc='No news found')

    except Exception, ex:
        print ex


def getTopNews():
    """
        Gets top 3 news from database.
    """
    try:
        news = DBSession.query(News.title, News.added, News.content, News.image).order_by(News.id.desc()).limit(6).all()

        json_news = []

        json_news.extend(dict(title=item.title, added=unicode(item.added), content=item.content, image=item.image)
                         for item in news if news)

        return dict(status=True, news=json_news)
    
    except Exception, ex:
        print ex


def getAllEvents():
    """
        Gets all events from database.
    """
    try:
        events = DBSession.query(Events.id, Events.date_start, Events.date_end, Events.title)\
            .order_by(Events.date_start.desc()).all()

        json_events = []

        if events:
            json_events.extend(dict(id=item.id, date_start=unicode(item.date_start), date_end=unicode(item.date_end),
                                    title=item.title) for item in events)

            return dict(status=True, events=json_events)

        else:
            return dict(status=False, desc='No events found')
        
    except Exception, ex:
        print ex

            
def getTopEvents():
    """
        Gets top 4 events from database.
    """
    try:
        events = DBSession.query(Events.id, Events.date_start, Events.title).filter(Events.date_start > datetime.now())\
            .order_by(Events.date_start.desc()).limit(4).all()

        json_events = []

        json_events.extend([dict(id=item.id, date_start=unicode(item.date_start), title=item.title) for item in events
                            if events])

        return dict(status=True, events=json_events)
    
    except Exception, ex:
        print ex


def getAllReservations():
    """
        Gets all reservations from database.
    """
    try:
        reservations = DBSession.query(Reservations.id, Reservations.date_start, Reservations.date_end, Reservations.title,
                                       Reservations.user, Reservations.phone).order_by(Reservations.date_start.desc()).all()
        json_reservations = []

        if reservations:
            json_reservations.extend(dict(id=item.id, date_start=unicode(item.date_start), date_end=unicode(item.date_end),
                                          title=item.title, email=item.user, phone=item.phone) for item in reservations)

            return dict(status=True, reservations=json_reservations)

        else:
            return dict(status=False, desc='No reservations found')
        
    except Exception, ex:
        print ex


def getTodayReservations():
    """
        Gets today reservations from database.
    """
    try:

        reservations = DBSession.query(Reservations.id, Reservations.date_start, Reservations.date_end, Reservations.title,
                       Reservations.user, Reservations.phone).filter(and_(Reservations.date_start >= date.today() +
                       timedelta(hours=0), Reservations.date_start < date.today() + timedelta(hours=24)))\
                       .order_by(Reservations.date_start.desc()).all()

        json_reservations = []

        if len(reservations) > 0:
            json_reservations.extend(dict(id=item.id, date_start=unicode(item.date_start), date_end=unicode(item.date_end),
                                          title=item.title, email=item.user, phone=item.phone) for item in reservations)

        if len(json_reservations) > 0:
            return dict(status=True, reservations=json_reservations)
        else:
            return dict(status=False, desc='No reservations found')

    except Exception, ex:
        print ex


def getAllDishes():
    """
        Gets all menu dishes from database.
    """
    try:
        dishes = DBSession.query(Dishes.id, Dishes.title, Dishes.ingredients, Dishes.price, Dishes.type, Dishes.image).\
            order_by(Dishes.type.asc(), Dishes.title.asc()).all()

        json_dishes = []

        if dishes:
            json_dishes.extend(dict(id=item.id, title=item.title, ingredients=item.ingredients,
                                    price=item.price, type=item.type, image=item.image) for item in dishes)

            return dict(status=True, dishes=json_dishes)

        else:
            return dict(status=False, desc='No dishes found')

    except Exception, ex:
        print ex

def upload_image(input_file, folder=None):
    """ Universal function to upload image to gallery """
    try:

        here = os.getcwd()

        if folder is not None:
            folder_path = os.path.normpath(os.path.join(here, '..', 'bergamotka', 'src', 'booking', 'gallery', folder))

        else:
            folder_path = os.path.normpath(os.path.join(here, '..', 'bergamotka', 'src', 'booking', 'gallery'))

        file_count = len(os.listdir(folder_path))

        file_path = os.path.normpath(os.path.join(folder_path, '%06d_%s' % ((file_count + 1), uuid.uuid4())))

        with open(file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        log.info('Writing %s into %s location.' % (input_file, file_path))

        img = Image.open(file_path)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.thumbnail(IMAGE_FORMAT, Image.ANTIALIAS)

        os.remove(os.path.normpath(file_path))

        log.info('Original file %s removed.' % input_file)

        img.save(file_path, IMAGE_EXTENSION, quality=70)

        log.info('Image %s resized to %s saved into %s location.' % (input_file, 'x'.join(str(pix) for pix in IMAGE_FORMAT), file_path))

        mini = Image.open(file_path)

        if mini.mode != 'RGB':
            mini = mini.convert('RGB')

        mini.thumbnail(THUMBNAIL_FORMAT, Image.ANTIALIAS)
        mini.save('%s.thumb' % file_path, THUMBNAIL_EXTENSION, quality=70)

        return file_path.split('booking')[1]

    except Exception, ex:
        print ex