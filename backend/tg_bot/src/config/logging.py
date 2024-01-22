import os


def get_logging_dict(root_dir: str) -> dict:
    if not os.path.exists(f'{root_dir}/logs/'):
        os.mkdir(f'{root_dir}/logs/')
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'main': {
                'format': '{asctime} - {levelname} - {module} - ' '{message} - {message}',
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
                'filename': f'{root_dir}/logs/error.log',
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
