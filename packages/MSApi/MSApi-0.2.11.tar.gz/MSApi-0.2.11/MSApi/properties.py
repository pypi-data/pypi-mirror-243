
# deprecated

class Expand:

    def __init__(self, *args):
        self.expand_list: [str] = []
        for arg in args:
            self.expand_list.append(str(arg))

    def __str__(self):
        return f"expand={','.join(self.expand_list)}"


class Search:

    def __init__(self, *args):
        self.search_list = []
        for arg in args:
            self.search_list.append(str(arg))

    def __str__(self):
        return f"search={' '.join(self.search_list)}"


class Filter(object):

    @classmethod
    def eq(cls, parameter, data):
        filter_ = Filter()
        filter_._append_filter("=", parameter, data)
        return filter_

    @classmethod
    def gt(cls, parameter, data):
        filter_ = Filter()
        filter_._append_filter(">", parameter, data)
        return filter_

    @classmethod
    def lt(cls, parameter, data):
        filter_ = Filter()
        filter_._append_filter("<", parameter, data)
        return filter_

    @classmethod
    def gte(cls, parameter, data):
        filter_ = Filter()
        filter_._append_filter(">=", parameter, data)
        return filter_

    @classmethod
    def lte(cls, parameter, data):
        filter_ = Filter()
        filter_._append_filter("<=", parameter, data)
        return filter_

    @classmethod
    def ne(cls, parameter, data):
        filter_ = Filter()
        filter_._append_filter("!=", parameter, data)
        return filter_

    @classmethod
    def siml(cls, parameter, data):
        filter_ = Filter()
        filter_._append_filter("~=", parameter, data)
        return filter_

    @classmethod
    def simr(cls, parameter, data):
        filter_ = Filter()
        filter_._append_filter("=~", parameter, data)
        return filter_

    @classmethod
    def sim(cls, parameter, data):
        filter_ = Filter()
        filter_._append_filter("~", parameter, data)
        return filter_

        # ['=', '>', '<', '>=', '<=', '!=', '~', '~=', '=~']

    def __init__(self):
        self.filters = []

    def __str__(self):
        return "filter={0}".format(';'.join(self.filters))

    def __add__(self, other):
        self.filters += other.filters
        return self

    def _append_filter(self, operator, parameter, data):
        self.filters.append(f"{parameter}{operator}{data}")
