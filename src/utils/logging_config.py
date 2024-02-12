import os
from logging.handlers import TimedRotatingFileHandler
from django.conf import settings

LOGS_DIR = settings.LOGS_DIR


def create_rotating_handler_config(filename):
    return {
        'level': 'DEBUG' if 'error' not in filename else 'ERROR',
        '()': TimedRotatingFileHandler,
        'filename': os.path.join(LOGS_DIR, filename),
        'when': 'D',
        'interval': 1,
        'backupCount': 30,
        'formatter': 'verbose',
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} \n{message}',
            'style': '{',
        },
    },
    'handlers': {
        'db_log_handler': create_rotating_handler_config('db_queries.log'),
        'app_log_handler': create_rotating_handler_config('app_events.log'),
        'error_log_handler': create_rotating_handler_config('error.log'),
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['db_log_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'app.events': {
            'handlers': ['app_log_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'app.errors': {
            'handlers': ['error_log_handler'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
