from typing import List

from datetime import date
from dateutil import relativedelta


def generateDailyDateRange(startDate: date, endDate: date) -> List[date]:
    date_modified = startDate
    dateList = [startDate]

    while date_modified < endDate:
        date_modified += relativedelta.relativedelta(days=1)
        dateList.append(date_modified)

    return dateList
