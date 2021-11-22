A constraint solver.

Example constraints:

* Employees must start after 8
* Employees must end before 18
* Employees must not work over the weekend
* Employees must not work more than six (6) consecutive hours
* Employees must not work more than seventeen (17) hours in a week

We have three employees, Prisca, Nicolas and Charlotte. Prisca must not work on Fridays, and Charlotte must not work on Tuesdays.

This is how those constraints would be defined:
```python
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


p = Planning(
    "Librairie",
    "somewhere",
    [NonWorkingHours(), Weekends(), Prisca(), Charlotte(), Nicolas()],
    datetime(2021, 11, 1), # start date for the planning
    datetime(2021, 11, 8), # end date
)
r = p.fill() # fill out the planning based on specified constraints
print(p)
if not r:
    print("Unsolvable.")
```

Result:

| hours   | 2021-11-01   | 2021-11-02   | 2021-11-03   | 2021-11-04   | 2021-11-05   | 2021-11-06   | 2021-11-07   |
|---------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| ------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ |
| 0       | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 1       | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 2       | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 3       | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 4       | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 5       | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 6       | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 7       | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 8       | Prisca       | Prisca       | Charlotte    | Charlotte    | Nicolas      | ----         | ----         |
| 9       | Prisca       | Prisca       | Charlotte    | Charlotte    | Nicolas      | ----         | ----         |
| 10      | Prisca       | Prisca       | Charlotte    | Charlotte    | Nicolas      | ----         | ----         |
| 11      | Prisca       | Prisca       | Charlotte    | Charlotte    | Charlotte    | ----         | ----         |
| 12      | Prisca       | Prisca       | Charlotte    | Charlotte    | Nicolas      | ----         | ----         |
| 13      | Prisca       | Prisca       | Charlotte    | Charlotte    | Nicolas      | ----         | ----         |
| 14      | Charlotte    | Nicolas      | Nicolas      | Nicolas      | Nicolas      | ----         | ----         |
| 15      | Prisca       | Prisca       | Charlotte    | Nicolas      | Nicolas      | ----         | ----         |
| 16      | Prisca       | Prisca       | Charlotte    | Nicolas      | Nicolas      | ----         | ----         |
| 17      | Prisca       | Nicolas      | Charlotte    | Nicolas      | Nicolas      | ----         | ----         |
| 18      | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 19      | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 20      | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 21      | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 22      | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
| 23      | ----         | ----         | ----         | ----         | ----         | ----         | ----         |
