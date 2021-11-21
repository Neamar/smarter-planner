def constraint_not(c):
    def i(p, r):
        return not c(p, r)

    i.__name__ = "(not %s)" % c.__name__
    return i


def constraint_or(c1, c2):
    def i(p, r):
        return c1(p, r) or c2(p, r)

    i.__name__ = "(%s or %s)" % (c1, c2)
    return i


def start_after(hour):
    def i(p, r):
        return p.start.hour >= hour

    i.__name__ = "[start>=%s]" % hour
    return i


def end_before(hour):
    def i(p, r):
        return p.start.hour < hour

    i.__name__ = "[end<%s]" % hour
    return i


def weekend():
    def i(p, r):
        weekday = p.start.weekday()
        return weekday == 5 or weekday == 6

    i.__name__ = "[weekend]"
    return i


def weekday(day):
    def i(p, r):
        weekday = p.start.weekday()
        return weekday == day

    i.__name__ = "[weekday=%s]" % day
    return i


def max_hours_in_week(hours):
    def i(period, r):
        periods = period.planning.periods
        week = period.start.isocalendar().week
        i = periods.index(period) - 1
        count = 0
        while i >= 0:
            period_before = periods[i]
            if period_before.start.isocalendar().week != week:
                break
            if period_before.assignment == r:
                count += 1
                if count >= hours:
                    return False
            i -= 1
        return True

    i.__name__ = "[max_hours_in_week=%s]" % hours
    return i


def max_hours_in_shift(hours):
    def i(period, r):
        periods = period.planning.periods
        i = periods.index(period) - 1
        count = 0
        while i >= 0:
            period_before = periods[i]
            if period_before.assignment != r:
                break

            count += 1
            if count >= hours:
                return False
            i -= 1
        return True

    i.__name__ = "[max_hours_in_shift=%s]" % hours
    return i
