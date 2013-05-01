import datetime


class News:

    def __init__(self, news_f):
        self._news_f = news_f

    @property
    def news_f(self):
        return self._news_f

    def parse(self, number_of_items=None):
        '''

        This function returns the `number_of_items` most recent news item
        parsed from `news_f'.

        Args:
            number_of_items (int): The number of (most recent) news items to
            return. If set to None, all available news items in `news_f` will
            be returned.
        '''
        print 'Start parsing'
        news_items = []

        with open(self.news_f, 'r') as fin:

            news_items = []
            num_items = int(fin.readline())

            if(number_of_items is None):
                number_of_items = num_items

            for i in xrange(min(num_items, number_of_items)):
                fin.readline()
                date = datetime.datetime.strptime(fin.readline().strip(),
                                                  '%Y-%m-%d')
                title = fin.readline().strip()
                text = fin.readline().strip()
                published = eval(fin.readline())

                news_items.append((date, title, text, published))

        print news_items
        return news_items
