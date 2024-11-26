import logging.config
import os

def config_logger(level='INFO', handlers=['file_handler', 'console_handler'], filename='logs/logs.log'):
    log_dir = os.path.dirname(filename)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    config = {
        'version': 1,
        'disable_exisiting_loggers': True,

        'formatters': {
            'std_format': {
                'format': '{asctime} - {levelname} - {name} - {message}',
                'style': '{'
            }
        },

        'handlers': {
            'file_handler': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'std_format',
                'filename': filename
            },

            'console_handler': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'std_format'
            }
            # 'telegram_handler' {}
        },
        
        'loggers': {
            'mail_logger': {
                'level': level,
                'handlers': handlers,
                'propagate': False
            }
        } 
    }

    logging.config.dictConfig(config)

    return logging.getLogger('mail_logger')
