from configparser import ConfigParser

TOKEN_SECTION_NAME = "TOKENS"
TS_TOKEN_NAME = "ts_token"

config = ConfigParser()
config.read("../crius.properties")


def getProperty(section_name, property_name):
    return config[section_name][property_name]
