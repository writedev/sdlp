from rich.logging import RichHandler
import logging


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


class SytdlpLogger:
    def debug(self, msg):
        # if msg.startswith("[debug]"):
        #     pass
        # else:
        #     print(msg)
        logging.debug(msg=msg)

    def info(self, msg):
        logging.info(msg=msg)

    def warning(self, msg):
        logging.warning(msg=msg)

    def error(self, msg):
        logging.error(msg=msg)
