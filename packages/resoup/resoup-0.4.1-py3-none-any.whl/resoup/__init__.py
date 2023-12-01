"""
██████╗░███████╗░██████╗░██╗░░░██╗███████╗░██████╗████████╗░██████╗░░░░░░██╗░░░██╗████████╗██╗██╗░░░░░░██████╗
██╔══██╗██╔════╝██╔═══██╗██║░░░██║██╔════╝██╔════╝╚══██╔══╝██╔════╝░░░░░░██║░░░██║╚══██╔══╝██║██║░░░░░██╔════╝
██████╔╝█████╗░░██║██╗██║██║░░░██║█████╗░░╚█████╗░░░░██║░░░╚█████╗░█████╗██║░░░██║░░░██║░░░██║██║░░░░░╚█████╗░
██╔══██╗██╔══╝░░╚██████╔╝██║░░░██║██╔══╝░░░╚═══██╗░░░██║░░░░╚═══██╗╚════╝██║░░░██║░░░██║░░░██║██║░░░░░░╚═══██╗
██║░░██║███████╗░╚═██╔═╝░╚██████╔╝███████╗██████╔╝░░░██║░░░██████╔╝░░░░░░╚██████╔╝░░░██║░░░██║███████╗██████╔╝
╚═╝░░╚═╝╚══════╝░░░╚═╝░░░░╚═════╝░╚══════╝╚═════╝░░░░╚═╝░░░╚═════╝░░░░░░░░╚═════╝░░░░╚═╝░░░╚═╝╚══════╝╚═════╝░

Various convenient features related to requests.
"""

__title__ = "requests_utils"
__description__ = 'Various convenient features related to requests.'
__url__ = "https://github.com/ilotoki0804/requests-utils"
__raw_source_url__ = "https://raw.githubusercontent.com/ilotoki0804/requests-utils/master"
__version_info__ = (0, 4, 1)
__version__ = str.join('.', map(str, __version_info__))
__author__ = "ilotoki0804"
__author_email__ = "ilotoki0804@gmail.com"
__license__ = "MIT License"

from . import requests_ as requests
from .custom_defaults import CustomDefaults
from .header_utils import clean_headers
from .sessions_with_tools import Session
from .souptoolsclass import SoupTools
