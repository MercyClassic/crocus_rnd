

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_format': {
            'format': '{asctime} - {levelname} - {module} - {view} - {session_id} - {message}',
            'style': '{',
        },
        'telegram_format': {
            'format': '{asctime} - {levelname} - {module} - {message} - {user_id} - {message_id}',
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
            'filename': 'logs/market_log.log',
        },
        'telegram': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1_048_576,
            'backupCount': 50,
            'formatter': 'telegram_format',
            'filename': 'logs/telegram_log.log',
        },
        'payment_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1_048_576,
            'backupCount': 50,
            'formatter': 'payment_format',
            'filename': 'logs/payment_info_log.log',
        },
        'payment_warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1_048_576,
            'backupCount': 50,
            'formatter': 'payment_format',
            'filename': 'logs/payment_warning_log.log',
        },
    },
    'loggers': {
        'unexpected_errors': {
            'handlers': ['market'],
            'level': 'ERROR',
            'propagate': True,
        },
        'telegram_errors': {
            'handlers': ['telegram'],
            'level': 'ERROR',
            'propagate': True,
        },
        'payment': {
            'handlers': ['payment_info', 'payment_warning'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
