from datetime import date

# from django.utils import timezone
import calendar


class Day:
    def __init__(self, number, past):
        self.number = number
        self.past = past

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.month_names = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]

    def get_month(self):
        return self.month_names[self.month - 1]

    def get_day_names(self):
        return self.day_names[-1:] + self.day_names[:-1]

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        today = date.today()
        days = []
        for week in weeks:
            for day, _ in week:
                if day:
                    past = date(self.year, self.month, day) <= today
                else:
                    past = True
                days.append(Day(day, past))

        # days = []
        # weeks = self.monthdayscalendar(self.year, self.month)
        # for week in weeks:
        #     days.extend(week)

        return days


new_cal = Calendar(2022, 6)
new_cal.get_days()
