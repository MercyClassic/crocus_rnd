from config import Config


def get_logging_dict(config: Config) -> dict:
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'main': {
                'format': '{asctime} - {levelname} - {module} - '
                '{message} - {user_id} - {message_id}',
                'style': '{',
            },
        },
        'handlers': {
            'main': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 1_048_576,
                'backupCount': 50,
                'formatter': 'main',
                'filename': f'{config.ROOT_DIR}/logs/error.log',
            },
        },
        'loggers': {
            'main': {
                'handlers': ['main'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
