# -*- coding:utf-8 -*-
from app import app

import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    #db.create_all()
    app.debug = True
    app.run(host='0.0.0.0')