#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import transaction
import datetime

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Users,
    Reservations,
    Base,
    News,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    
    if len(argv) != 2:
        usage(argv)
        
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    
    #INITIALIZE DATABASE WITH WORKING DATA
    #with transaction.manager:
        #users = Users(fname='Radosław', lname='Trojanowski', email='trojanowski.radek@gmail.com')
        #DBSession.add(users)
        
        #reservations = Reservations(user=1, date='2013-11-11 11:11')
        #DBSession.add(reservations)
        
        #news = News(title='Title', date='2013-11-11 11:11', content='Content here')
        #DBSession.add(news)