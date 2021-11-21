def constraint_not(c):
    def i(p):
        return not c(p)

    i.__name__ = "(not %s)" % c.__name__
    return i


def constraint_or(c1, c2):
    def i(p):
        return c1(p) or c2(p)

    i.__name__ = "(%s or %s)" % (c1, c2)
    return i


def start_after(hour):
    def i(p):
        return p.start.hour >= hour

    i.__name__ = "[start>=%s]" % hour
    return i


def end_before(hour):
    def i(p):
        return p.start.hour < hour

    i.__name__ = "[end<%s]" % hour
    return i


def weekend():
    def i(p):
        weekday = p.start.weekday()
        return weekday == 5 or weekday == 6

    i.__name__ = "[weekend]"
    return i


def weekday(day):
    def i(p):
        weekday = p.start.weekday()
        return weekday == day

    i.__name__ = "[weekday=%s]" % day
    return i
