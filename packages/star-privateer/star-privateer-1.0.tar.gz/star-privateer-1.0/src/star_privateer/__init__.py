from importlib.metadata import version

__version__ = version ('star_privateer')

from .rotation_pipeline import *

from .wavelets import *

from .correlation import *

from .lomb_scargle import *

from .rooster import *

from .aux import *

from .background import *

from .morphology import *

import star_privateer.timeseries 

import star_privateer.catalogs 

import star_privateer.rooster_instances 

import star_privateer.constants 
