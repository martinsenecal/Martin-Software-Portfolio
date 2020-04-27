import os

class Config:
    # Secret Key
    SECRET_KEY = 'SDF3W478_HS3ish34'

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # Flask-Mail Setup

    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    # My Email
    MAIL_USERNAME = 'test@gmail.com',
    MAIL_PASSWORD = 'TODO'  # ToDo: UseOS



