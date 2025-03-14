from pathlib import Path

if not Path('logs/').exists():
    Path('logs/').mkdir()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_format': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{',
        },
        'payment_format': {
            'format': '{asctime} - {levelname} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'market': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1_048_576,
            'backupCount': 50,
            'formatter': 'main_format',
            'filename': 'logs/market.log',
        },
        'payment_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1_048_576,
            'backupCount': 50,
            'formatter': 'payment_format',
            'filename': 'logs/payment_info.log',
        },
        'payment_warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1_048_576,
            'backupCount': 50,
            'formatter': 'payment_format',
            'filename': 'logs/payment_warning.log',
        },
    },
    'loggers': {
        'config.middlewares.log': {
            'handlers': ['market'],
            'level': 'ERROR',
            'propagate': True,
        },
        'payments': {
            'handlers': ['payment_info', 'payment_warning'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
