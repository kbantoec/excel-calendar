from datetime import date, datetime
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import pandas as pd

load_dotenv()


def test_dotenv():
    print(os.getenv("RESULTS"))
    res = Path(os.getenv("RESULTS"))
    print(res.exists())


def create_calendar(start_year: int,
                    end_year: int,
                    start_month: Optional[int] = 1,
                    end_month: Optional[int] = 12,
                    start_day: Optional[int] = 1,
                    end_day: Optional[int] = 31,
                    show_year: bool = True,
                    show_quarters: bool = True,
                    show_week_no: bool = True,
                    show_date: bool = True,
                    freq: str = 'D',
                    only_business_days: bool = False):
    """

    :param start_year:
    :param end_year:
    :param show_quarters:
    :param freq: 'D': day, 'M': month, 'Q', quarter.
    :param only_business_days:
    :return:
    """

    mycalendar: pd.DataFrame = pd.date_range(start=date(year=start_year, month=start_month, day=start_day),
                                             end=date(year=end_year, month=end_month, day=end_day),
                                             freq=freq).to_frame(index=False, name="dt_time")
    if show_year:
        mycalendar["year"] = mycalendar.dt_time.dt.year

    if show_quarters:
        mycalendar["quarter_no"] = mycalendar.dt_time.dt.quarter

    if show_quarters:
        mycalendar["quarter_year"] = mycalendar.quarter_no.astype(str) + "-" + mycalendar.dt_time.dt.year.astype(str)

    if show_week_no:
        mycalendar["week_no"] = mycalendar.dt_time.dt.isocalendar().week

    if show_week_no:
        mycalendar["week_year"] = mycalendar.week_no.astype(str) + "-" + mycalendar.dt_time.dt.year.astype(str)

    if show_week_no and show_quarters:
        mycalendar["week_quarter_year"] = mycalendar.week_no.astype(str) + "-" + mycalendar.quarter_no.astype(str) + "-" + mycalendar.dt_time.dt.year.astype(str)

    if not show_date:
        mycalendar.drop("date", axis=1, inplace=True)

    if show_date:
        mycalendar["day_name"] = mycalendar.dt_time.dt.day_name()
        mycalendar["day_of_month_no"] = mycalendar.dt_time.dt.day
        mycalendar["day_of_year_no"] = mycalendar.dt_time.dt.dayofyear
        mycalendar["day_of_week_no"] = mycalendar.dt_time.dt.dayofweek

    mycalendar["date"] = mycalendar.dt_time.dt.date
    mycalendar["month_name"] = mycalendar.dt_time.dt.month_name()

    return mycalendar


if __name__ == "__main__":
    # test_dotenv()
    mycal = create_calendar(start_year=2023, end_year=2023)

    res = Path(os.getenv("RESULTS"))
    mycal.to_excel(res / f'{datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")}_mycal.xlsx', index=False)
