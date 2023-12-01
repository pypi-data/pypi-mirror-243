# -*- coding: utf-8 -*-
"""Documentation about geo rasterizer"""

import logging

from logginginitializer.logging_config import LoggingConfig
from logginginitializer.logging_initializer import LoggingInitializer

from geo_rasterizer.geo_rasterizer import *

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "RWS Datalab"
__email__ = "datalab.codebase@rws.nl"
__version__ = "0.1.0"

logging_config = LoggingConfig(
    identifier=__name__,
    # directory="/path/to/file.log", # FIXME (optional)
)
LoggingInitializer(logging_config, quiet=False)
