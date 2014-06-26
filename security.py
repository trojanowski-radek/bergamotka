from .models import (
    DBSession,
    Users)

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s')
log = logging.getLogger(__name__)

def groupfinder(email, pwd, request):
    """
    Checks if user for email exist in database, checks password and returns permission or
    """

    users = DBSession.query(Users.permission, Users.pwd).filter(Users.email == email).first()

    if users:
        permission = users[0]
        password = users[1]

        log.info('pwd:%s' % pwd)
        log.info('password:%s' % password)
        log.info('permission:%s' % permission)

        return 'permission:%s' % permission if pwd == password else None

    return []