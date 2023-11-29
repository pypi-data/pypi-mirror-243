import logging

# Default logging. This can be overridden by the user in their application
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
