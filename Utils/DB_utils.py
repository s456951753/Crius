import datetime
import Utils.configuration_file_service as config_service


def getTableName(date, base_name):
    """
    Calculate table name out based on the give date and base api name. The table name will be in the below format:
    basename_startyear_endyear
    Specifically, the difference between start and end year is defined in config file. If the value is not defined,
    default difference will be 5.
    :param date: date of the data you want to insert
    :param base_name: name of the api
    :return: basename_startyear_endyear
    """


def getYears():
    """
    Return a list of calculated start and end years.
    :return: a list of calculated start and end years.
    """
    startEndYears = {}
    year = config_service.getProperty(config_service.DATA_CONFIG_SECTION_NAME,
                                      config_service.DATA_CONFIG_YEAR_GRANULARITY_NAME);
    if (year is None):
        return
