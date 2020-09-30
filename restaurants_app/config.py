class Config(object):
    """This will be the base class to extend in the rest of the config"""
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQL_ALCHEMY_ECHO = True


# Todo:Create the rest of the extensions of the Config class


class ProductionConfig(Config):
    """Here we define a production config"""
    DEBUG = True
    pass


class TestingConfig(Config):
    """This is the class for the test part of the production"""
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
