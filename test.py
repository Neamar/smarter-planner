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
            # Create all periods within that time span
            p = Period(planning=self, start=cursor)
            self.periods.append(p)
            cursor += period_length

    def __str__(self):
        """
        Display a nicely rendered view of the planning,
        day by day, hour by hour
        """
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

    def fill(self, index=0):
        """
        Fill out the planning according to current constraint
        """
        if index >= len(self.periods):
            return True

        period = self.periods[index]
        available_resources = [r for r in self.resources if r.can_work(period)]
        for resource in available_resources:
            period.assignment = resource
            r = self.fill(index + 1)
            if r:
                return True
            # otherwise, it's not working, try next resource
            period.assignment = None
        return False


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

    def can_work(self, period):
        for constraint in self.must:
            # print(m.__name__, period, m(period))
            if not constraint(period, self):
                return False
        return True

    def __str__(self):
        return self.name


class NonWorkingHours(Resource):
    name = "----"
    must = [
        constraint_or(end_before(8), start_after(18)),
    ]


class Weekends(Resource):
    name = "----"
    must = [weekend()]


class Employee(Resource):
    name = "Employee"
    must = [
        start_after(8),
        end_before(18),
        max_hours_in_shift(6),
        max_hours_in_week(17),
        constraint_not(weekend()),
    ]


class Prisca(Employee):
    name = "Prisca"
    must = [*Employee.must, constraint_not(weekday(4))]


class Charlotte(Employee):
    name = "Charlotte"
    must = [*Employee.must, constraint_not(weekday(1))]


class Nicolas(Employee):
    name = "Nicolas"
    must = [*Employee.must]


p = Planning(
    "Librairie",
    "procure",
    [NonWorkingHours(), Weekends(), Prisca(), Charlotte(), Nicolas()],
    datetime(2021, 11, 1),
    datetime(2021, 11, 8),
)
# print(p.resources[2].can_work(Period(p, datetime(2021, 11, 1, 10))))
r = p.fill()
print(p)
if not r:
    print("Unsolvable.")
