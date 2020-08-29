import datetime
import Utils.configuration_file_service as config_service
import logging

VERY_BEGINNING_YEAR = 1990


def getTableName(year: int, base_name) -> str:
    """
    Calculate table name out based on the give date and base api name. The table name will be in the below format:
    basename_startyear_endyear
    Specifically, the difference between start and end year will be 4 so each table contains 5 years of data
    - ranges will be like 1990 to 1994, 1995 to 1999

    :param year: year of the data you want to insert
    :param base_name: name of the api
    :return: basename_startyear_endyear. If the given year is not in the range supported (1990 to current year),
    basename_9995_10000 wil be returned. Hopefully we are not using this piece of shit by then.
    """
    tableName = None
    startEndYears = getYears()
    for startYear in startEndYears.keys():
        if (year >= startYear and year <= startEndYears.get(startYear)):
            tableName = base_name + '_' + str(startYear) + '_' + str(startEndYears.get(startYear))
            break
    if (tableName == None):
        logging.error(
            "The provided year argument " + str(
                year) + " is outside of the storage time interval. Please double check. We currently support between " + str(
                VERY_BEGINNING_YEAR) + " and " + str(datetime.date.today().year))
        return base_name + '_' + str(9995) + '_' + str(10000)
    return tableName


def getYears() -> {}:
    """
    Return a list of calculated start and end years.
    :return: a list of calculated start and end years.
    """
    startEndYears = {}
    # year = config_service.getProperty(config_service.DATA_CONFIG_SECTION_NAME,
    #                                 config_service.DATA_CONFIG_YEAR_GRANULARITY_NAME)
    currentYear = datetime.date.today().year

    thisYear = VERY_BEGINNING_YEAR
    while (thisYear <= currentYear):
        # startEndYears.append(str(thisYear) + '_' + str(thisYear+5))
        startEndYears[thisYear] = thisYear + 4
        thisYear = thisYear + 5
    if (thisYear > currentYear):
        # startEndYears.append(str(thisYear-5) + '_' + str(thisYear))
        startEndYears[thisYear - 5] = thisYear - 1
    return startEndYears
