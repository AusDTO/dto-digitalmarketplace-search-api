#!/usr/bin/env python

import os
import sys
from app import create_app
from dmutils import init_manager


port = int(os.getenv('PORT', '5001'))
application = create_app(os.getenv('DM_ENVIRONMENT') or 'development')
manager = init_manager(application, port, [])

@manager.command
def update_index(index_name):
    from app.main.services.search_service import create_index
    with application.app_context():
        application.logger.info("Creating index %s", index_name)
        message, status = create_index(index_name)
    assert status == 200, message
    application.logger.info("Created index %s", index_name)

application.logger.info('Command line: {}'.format(sys.argv))

if __name__ == '__main__':
    try:
        application.logger.info('Running manager')
        manager.run()
    finally:
        application.logger.info('Manager finished')
