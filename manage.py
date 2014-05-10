#!/usr/bin/env python
import web
import jinja2
import json
from utils import render_template
from settings import DB

urls = (
    '/', 'Index',
    '/(\d+)', 'ShowShop',
    #'/search/(\w+)', 'Search',
    '/add', 'Add',
    '/addShop', 'AddShop',
    '/edit/(\d+)', 'Edit',
    '/editShop/(\d+)', 'EditShop',
)

app = web.application(urls, globals())

class Index():
    def GET(self):
        return render_template('index.html')

class ShowShop():
    def GET(self, sid):
        sid = int(sid)
        shops = DB.shops
        s = shops.find_one({'sid':sid})
        if s:
            shop = {'name':s['name'],'addr':s['addr']}
            shopInfo = DB.shopInfo
            shop_info = shopInfo.find_one({'sid':sid})
            if shop_info:
                current_info = shop_info['current_info']
            else:
                current_info = None
            return render_template('show.html', sid=sid, shop=shop, c_info=current_info)
        else:
            return "Not found"
        

class Search():
    def GET(self, address):
        pass
        
class Add():
    def GET(self):
        #address = web.input().address
        return render_template('add.html')

class AddShop():
    def POST(self):
        result = {}
        name = web.input().name
        address = web.input().address
        shops = DB.shops
        if name and address:
            if not shops.find_one({'addr':address}):
                #global g_sid
                g_sid = 1
                sid = g_sid
                g_sid = g_sid + 1
                s = {'sid':sid, 'addr':address, 'name':name}
                shops.insert(s)
                raise web.redirect('/edit/%d' % sid)
            else:
                return "Exist"
        return "Wrong input"

class Edit():
    def GET(self, sid):
        shops = DB.shops
        sid = int(sid)
        s = shops.find_one({'sid':sid})
        if s:
            name = s['name']
            shop = DB.shopInfo.find_one({'sid':sid})
            if shop:
                current_info = shop['current_info']
            else:
                current_info = None
            return render_template('edit.html', sid=sid, name=name, c_info=current_info)
        else:
            return "Not found"
        return
        
class EditShop():
    def POST(self, sid):
        sid = int(sid)
        shopInfo = DB.shopInfo
        s = shopInfo.find_one({'sid':sid})
        news = web.input().news
        tv = web.input().tv
        if not s:
            shop_info = {'sid':sid, 'current_info':{'news':news, 'tv':tv}, 'previous_info_list':[]}
            shopInfo.insert(shop_info)
        else:
            c_info = s['current_info']
            shopInfo.update({'sid':sid}, {'$push': {'previous_info_list':c_info}})
            c_info['news'] = news
            c_info['tv'] = tv
            shopInfo.update({'sid':sid}, {'$set': {'current_info':c_info}})
        raise web.redirect('/%d' % sid)


if __name__ == "__main__":
    app.internalerror = web.debugerror
    app.run()
