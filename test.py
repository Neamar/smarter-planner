from datetime import datetime, timedelta

from tabulate import tabulate

from constraints import *


class Planning:
    name = ""
    location = ""
    start: datetime = None
    end: datetime = None
    period_length: timedelta
    periods = []

    resources = []

    def __init__(self, name, location, resources, start, end, period_length=timedelta(hours=1)):
        self.name = name
        self.location = location
        self.start = start
        self.end = end
        self.period_length = period_length
        self.resources = resources
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
                    today.append(period.assignment.name if period.assignment is not None else "?")
            out.append(today)
        return tabulate(zip(hours, *out), headers=["hours", *days])

    def fill(self):
        for period in self.periods:
            for resource in self.resources:
                if resource.can_work(period):
                    period.assignment = resource


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

    def can_work(self, period):
        for m in self.must:
            if not m(period):
                return False
        return True

    def __str__(self):
        return self.name


class NonWorkingHours(Resource):
    name = "----"
    must = [
        constraint_or(constraint_not(end_after(8)), constraint_not(start_before(18))),
    ]


class Weekends(Resource):
    name = "----"
    must = [weekend()]


class Employee(Resource):
    name = "Employee"
    must = [
        constraint_not(start_before(8)),
        constraint_not(end_after(18)),
        constraint_not(weekend()),
    ]
    should = []


class Prisca(Employee):
    name = "Prisca"
    pass


class Prisca(Employee):
    name = "Prisca"
    must = [*Employee.must, constraint_not(weekday(0))]


p = Planning(
    "Librairie",
    "procure",
    [NonWorkingHours(), Weekends(), Prisca()],
    datetime(2021, 11, 1),
    datetime(2021, 11, 8),
)
print(NonWorkingHours().can_work(Period(p, datetime(2021, 11, 1, 10))))
p.fill()
print(p)
