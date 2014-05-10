#!/usr/bin/env python
import web
import jinja2
from utils import render_template

urls = (
    '/', 'Index',
)

app = web.application(urls, globals())

class Index():
    def GET(self):
        return render_template('index.html')


if __name__ == "__main__":
    app.internalerror = web.debugerror
    app.run()
