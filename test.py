from datetime import datetime, timedelta

from tabulate import tabulate


class Planning:
    name = ""
    location = ""
    start: datetime = None
    end: datetime = None
    period_length: timedelta
    periods = []

    def __init__(self, name, location, start, end, period_length=timedelta(hours=1)):
        self.name = name
        self.location = location
        self.start = start
        self.end = end
        self.period_length = period_length
        cursor = start
        while cursor < end:
            self.periods.append(Period(planning=self, start=cursor))
            cursor += period_length

    def __str__(self):
        hours = sorted(set([p.start.hour for p in self.periods]))
        days = sorted(set([p.start.date() for p in self.periods]))
        out = []
        for day in days:
            today = []
            for period in self.periods:
                if period.start.date() == day:
                    today.append(period.assignment if period.assignment is not None else "?")
            out.append(today)
        print(out)
        return tabulate(zip(hours, *out), headers=["hours", *days])


class Period:
    planning: Planning = None
    start: datetime = None
    assignment = None

    def __init__(self, planning, start):
        self.planning = planning
        self.start = start

    def __str__(self):
        return str(self.start)


class Resource:
    name = ""
    must = []
    should = []

    def can_work(period: Period):
        pass

    def __repr__(self):
        return self.name


class Employee(Resource):
    must = []
    should = []


p = Planning("Librairie", "procure", datetime(2021, 11, 1), datetime(2021, 11, 8))
print(p)
