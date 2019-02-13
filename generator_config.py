import logging

h = logging.FileHandler("sample_file_generator.log", encoding="utf-8")
logger = logging.getLogger(__name__)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s :%(message)s")
logging.basicConfig(filename='logger.log',level=logging.DEBUG, format=fmt)
h.setFormatter(fmt)
logger.setLevel(logging.ERROR)
logger.addHandler(h)