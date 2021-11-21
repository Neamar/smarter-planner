def constraint_not(c):
    def i(p):
        print("not", c(p))
        return not c(p)

    return i


def constraint_or(c1, c2):
    def i(p):
        print("or", c1(p), c2(p))
        return c1(p) or c2(p)

    return i


def start_before(hour):
    def i(p):
        print("start before", hour, p.start.hour)
        return p.start.hour < hour

    return i


def end_after(hour):
    def i(p):
        print("end after", hour, p.start.hour)
        return p.start.hour >= hour

    return i


def weekend():
    def i(p):
        weekday = p.start.weekday()
        return weekday == 5 or weekday == 6

    return i


def weekday(day):
    def i(p):
        weekday = p.start.weekday()
        return weekday == day

    return i
