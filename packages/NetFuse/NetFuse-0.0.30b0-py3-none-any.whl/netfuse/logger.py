import logging

LOGGER = logging.getLogger(__name__)
_HANDLER = logging.StreamHandler()
_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - [%(module)s:%(lineno)d] - %(funcName)s - %(message)s')
_HANDLER.setFormatter(_FORMATTER)
LOGGER.addHandler(_HANDLER)
LOGGER.setLevel(logging.INFO)
