import logging
import logging.config


def logger_init(logdir):
    """
    usage:
    import logging
    curdir = os.path.dirname(os.path.realpath(__file__))
    logdir = os.path.join(curdir, 'log')
    logger_init(logdir)
    logging.info('TEST')
    """
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    filename = os.path.join(logdir, "run.log")
    config = {
        "version": 1,
        "formatters": {
            "standard": {
                "format": "[%(levelname)s] [%(asctime)s]  [%(pathname)s: %(lineno)d] %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "standard",
            },
            "file": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": filename,
                "maxBytes": 100 * 1024 * 1024,
                "backupCount": 10,
                "encoding": "utf-8",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["file", "console"]},
    }
    logging.config.dictConfig(config)
