import os
import datetime

import cherrypy

import spicaweb

class News:

    @cherrypy.expose
    def index(self):

        hmi = 0

        kw_args = spicaweb.get_template_args(header_menu_index=hmi)
        kw_args['news_collection'] = self.parse_news()

        template_f = '%s.html' % (spicaweb.header_menu[hmi][0])

        return spicaweb.get_template(template_f, **kw_args)

    def parse_news(self):
        news_f = os.path.join(spicaweb.news_dir, 'news.txt')
        news_parser = NewsCollectionParser(news_f)
        news_collection = news_parser.parse()
        return news_collection

    #@lg_authority.groups('admin')
    def admin(self):
        return 'news_admin'


class NewsItem:

    def __init__(self, date, title, text, published, highlighted):
        self.date = date
        self.title = title
        self.text = text
        self.published = published
        self.highlighted = highlighted


class NewsCollectionParser:

    def __init__(self, news_file):
        self.news_file = news_file

    def parse(self):
        with open(self.news_file, 'r') as fin:

            news_collection = []
            num_items = int(fin.readline())

            for i in xrange(num_items):
                fin.readline()
                date = datetime.datetime.strptime(fin.readline().strip(),
                        '%Y-%m-%d')
                title = fin.readline().strip()
                text = fin.readline().strip()
                published = eval(fin.readline())
                highlighted = eval(fin.readline())

                news_item = NewsItem(date, title, text, published, highlighted)
                news_collection.append(news_item)

        return news_collection
