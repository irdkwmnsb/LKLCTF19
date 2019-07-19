#!/usr/bin/env python3

import auth

import os
from collections import namedtuple

import tornado.ioloop
import tornado.web


Post = namedtuple('Post', ['title', 'text', 'author'])


def get_posts():
    return [
        Post(
            title='У нас появился сайт!',
            text=(
                'Приветствуем вас на нашем сайте! Мы создали его достаточно недавно, и он нам нужен, чтобы '
                'повысить качество обслуживания клиентов. Мы использовали только проверенные и безопасные '
                'технологии, так что вероятность взлома сайта или аккаунтов какого-то из пользователей '
                'сведена к минимуму. Надеемся, вам будет приятно пользоваться нашим сайтом'
            ),
            author='user1',
        ),
        Post(
            title='Без названия',
            text='<img src="/static/image1.png" width=200 height=200 alt="image"></img>',
            author='admin',
        ),
        Post(
            title='Тестовая запись',
            text='Текст тестовой записи',
            author='smart_bot',
        ),
    ]


class HomepageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html', posts=get_posts())

    def get_current_user(self):
        return auth.maybe_get_user_by_session(self.get_cookie('session_id'))


class SignInHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', '')
        password_hash = auth.hash_password(password)
        session_id = auth.maybe_authorize_user(username, password_hash)
        if session_id is None:
            self.render('templates/bad-auth.html')
        else:
            self.set_cookie('session_id', session_id)
            self.redirect('/')


class ViewUserInfoHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', '')
        password_hash = auth.hash_password(password)
        user = auth.maybe_get_user_by_full_creds(username, password_hash)
        if user is None:
            self.render('templates/bad-auth.html')
        else:
            self.render('templates/view-user-info.html', user=user)


class LogOutHandler(tornado.web.RequestHandler):
    def get(self):
        session_id = self.get_cookie('session_id')
        auth.delete_session_if_exists(session_id)
        self.clear_cookie('session_id')
        self.redirect('/')


class SimpleHandler(tornado.web.RequestHandler):
    def initialize(self, filename):
        self.filename = filename

    def get(self):
        self.render(self.filename)


def main():
    port = int(os.getenv('SERVICE_PORT', 9999))
    app = tornado.web.Application(
        [
            ('/', HomepageHandler),
            ('/log-out', LogOutHandler),
            ('/sign-in', SignInHandler),
            ('/view-user-info', ViewUserInfoHandler),
            ('/sign-in-form', SimpleHandler, {'filename': 'templates/sign-in-form.html'}),
            ('/static/(.*)', tornado.web.StaticFileHandler, {'path': './static'}),
        ],
        debug=True,
        autoreload=False,
    )
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
