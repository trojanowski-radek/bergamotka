#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.config import Configurator

from .models import (
    DBSession,
    Base,
    Users,
    Reservations,
    Events, )

from booking.security import groupfinder

def main(global_config, **settings):
    """ 
        This function returns a Pyramid WSGI application.
    """
    
    from sqlalchemy import engine_from_config
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    #Security rules
    authentication_policy = AuthTktAuthenticationPolicy('s3qr3db00k1ng', hashalg='sha512')
    authorization_policy = ACLAuthorizationPolicy()
    
    #Config
    config = Configurator(settings=settings,
                          root_factory='booking.models.RootFactory',
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy)

    config.include('pyramid_chameleon')
    
    #Views
    config.add_static_view('static', 'static', cache_max_age=30)
    config.add_static_view('gallery', 'gallery', cache_max_age=30)
    
    #---------ROUTES
    #HOME
    config.add_route('home', '/')
    
    #LOGGING
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    
    #NEWS
    config.add_route('news', '/news')
    config.add_route('news_add', '/news_add')
    config.add_route('news_image_upload', '/news_image_upload')
    config.add_route('news_edit', '/news_edit')
    config.add_route('news_delete', '/news_delete')
    
    #CALENDAR
    config.add_route('calendar', '/calendar')
    config.add_route('events_view', '/events_view')
    config.add_route('events_add', '/events_add')
    config.add_route('events_edit', '/events_edit')
    config.add_route('events_delete', '/events_delete')
    
    #RESERVATION
    config.add_route('reservations', '/reservations')
    config.add_route('reservations_add', '/reservations_add')
    config.add_route('reservations_edit', '/reservations_edit')
    config.add_route('reservations_delete', '/reservations_delete')
    
    #GALLERY
    config.add_route('gallery', '/gallery')
    config.add_route('gallery_upload', '/gallery_upload')

    #DISHES
    config.add_route('dishes', '/dishes')
    config.add_route('dishes_add', '/dishes_add')
    config.add_route('dishes_image_upload', '/dishes_image_upload')
    config.add_route('dishes_edit', '/dishes_edit')
    config.add_route('dishes_delete', '/dishes_delete')
    
    #ABOUT
    config.add_route('about', '/about')
    
    #ADMIN PANEL
    config.add_route('admin', '/admin')
    #--------
    
    config.scan()

    app = config.make_wsgi_app()
    
    return app