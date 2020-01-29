TEX_TEMPLATES_PATH = 'tex_templates'
from .tikz import *
from .catalan import *
from .asciiDrawing import *
from .catalan_families.brackets import *
from .catalan_families.trees import *
from .catalan_families.tableaux import *
from .catalan_families.dyckPaths import *
from .catalan_families.productStrings import *
from .catalan_families.triangulations import *
from .catalan_families.mountainsAscii import *
from .catalan_families.nestedMatchings import *
from .catalan_families.staircasePolygons import *
from .catalan_families.friezePatterns import *

 
for Catalan_Family in Catalan.all_catalan_families():
  Catalan_Family.init_norm_cache()