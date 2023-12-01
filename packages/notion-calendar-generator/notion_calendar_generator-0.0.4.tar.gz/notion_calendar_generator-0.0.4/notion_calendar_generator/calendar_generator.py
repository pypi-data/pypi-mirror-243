from datetime import datetime, timedelta
import calendar


class Calendar:

    def __init__(self, year: int) -> None:
        """Create a calendar with days, weeks, months, quarters and year in a
        format that is easily passed to the Notion API to generate these pages

        Args:
            year (dict): year (name, start, end, quarters, months)

        Important Attributes:
            quarters (dict) : 4 total (name, start, end, year, months)
            months (dict): year -> 12, quarters -> 3 (name, start, end, year, quarter)
            weeks (dict): month -> ~? (name, start, end, month, days)
            days: (dict) total: 365/366, week -> 7 (name, start, week)
        """
        self.year_long = year
        self.year_short = year % 100
        self.jan_1 = datetime(year, 1, 1)
        self.__create_days()
        self.__create_weeks()
        self.__create_months()
        self.__create_quarters()
        self.__create_year()

    def __create_year(self) -> None:
        """
        Create the year attribute for the Calendar instance.
        """
        days = self.__calculate_leap_year(self.year_long)
        self.year = {
            "title": f"{self.year_long}",
            "start": self.jan_1.strftime("%Y-%m-%d"),
            "end": (self.jan_1 + timedelta(days=days)).strftime("%Y-%m-%d")
        }

    def __create_quarters(self) -> None:
        """
        Create the quarters attribute for the Calendar instance.
        """
        self.quarters = []
        for i in range(0, 4):
            self.quarters.append({
                "title": f'{self.year_short}-Q{i + 1}',
                "start": self.months[i * 3]['start'],
                "end": self.months[i * 3 + 2]['end']
            })

    def __create_months(self) -> None:
        """
        Create the months attribute for the Calendar instance.
        """
        self.months = []
        for i in range(1, 13):
            _, month_end = calendar.monthrange(self.year_long, i)
            self.months.append({
                "title": f'{self.year_short}-{datetime(self.year_long, i, 1).strftime("%B")}',
                "start": datetime(self.year_long, i, 1).strftime("%Y-%m-%d"),
                "end": datetime(self.year_long, i, month_end).strftime("%Y-%m-%d")
            })

    def __create_weeks(self) -> None:
        """
        Create the weeks attribute for the Calendar instance.
        """
        self.weeks = []
        start_date = self.jan_1
        for i in range(1, 54):
            end_date = datetime(self.year_long, 1, 1) + timedelta(days=6 + 7 * (i - 1))
            if end_date.year > self.year_long:
                end_date = datetime(self.year_long, 12, 31)
            self.weeks.append({
                "title": f"{self.year_short}-week-{i}",
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            })
            start_date = end_date + timedelta(days=1)
            if start_date.year > self.year_long:
                break

    def __create_days(self) -> None:
        """
        Create the days attribute for the Calendar instance.
        """
        self.days = [{
            "title": f"{self.year_short}-day-{1}",
            "start_dt": self.jan_1,
            "start": f"{self.year_long}-01-01"
        }]
        days = self.__calculate_leap_year(self.year_long)
        for i in range(2, days):
            start_dt = self.jan_1 + timedelta(days=i - 1)
            self.days.append({
                "title": f"{self.year_short}-day-{i}",
                "start_dt": start_dt,
                "start": start_dt.strftime("%Y-%m-%d")
            })

    @staticmethod
    def __calculate_leap_year(year: int) -> int:
        """
        Calculate if a year is a leap year.

        Args:
            year (int): The year to check.

        Returns:
            int: The number of days in the year.
        """
        if year % 4 == 0:
            return 367
        return 366

    def update_quarters(self, year_id: str) -> None:
        """
        Update the quarters attribute with relation to the year.

        Args:
            year_id (str): The ID of the year.
        """
        for quarter in self.quarters:
            quarter.update({"relations": {"🕯 annual-data": [year_id]}})

    def update_months(self, year_id: str, quarter_ids: list) -> None:
        """
        Update the months attribute with relation to the year and quarters.

        Args:
            year_id (str): The ID of the year.
            quarter_ids (list): The IDs of the quarters.
        """
        for i, month in enumerate(self.months):
            quarter_index = i // 3
            month.update({"relations": {"🕯 annual-data": [year_id], "❄ quarterly-data": [quarter_ids[quarter_index]]}})

    def update_weeks(self, month_ids: list) -> None:
        """
        Update the weeks attribute with relation to the months.

        Args:
            month_ids (list): The IDs of the months.
        """
        for week in self.weeks:
            month_index = datetime.strptime(week['start'], "%Y-%m-%d").month - 1
            week.update({"relations": {"🌘 monthly-data": [month_ids[month_index]]}})

    def update_days(self, week_ids: list) -> None:
        """
        Update the days attribute with relation to the weeks.

        Args:
            week_ids (list): The IDs of the weeks.
        """
        for day in self.days:
            week_number = day["start_dt"].isocalendar()[1]
            if day["start_dt"].month == 12 and week_number == 1:
                week_number = 53 if calendar.isleap(day["start_dt"].year) else 52
            week_number -= 1
            day.update({"relations": {"🏁 weekly-data": [week_ids[week_number]]}})

