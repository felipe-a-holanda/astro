#!/usr/bin/python
activate_this = '/var/www/astro/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/astro/")

from astro import app as application
application.secret_key = 'Add your secret key'

if __name__ == '__main__':
    application.run()
