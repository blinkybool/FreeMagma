TEX_TEMPLATES_PATH = 'tex_templates'
from .tikz import *
from .asciiDrawing import *

from .catalan import *
from .catalan_families.brackets import *
from .catalan_families.trees import *
from .catalan_families.tableaux import *
from .catalan_families.dyckPaths import *
from .catalan_families.productStrings import *
from .catalan_families.triangulations import *
from .catalan_families.matchings import *
from .catalan_families.staircasePolygons import *
from .catalan_families.friezePatterns import *

from .motzkin import *
from .motzkin_families.motzkinPaths import *
 
for Catalan_Family in Catalan.iter_families():
  Catalan_Family.init_norm_cache()

for Motzkin_Family in Motzkin.iter_families():
  Motzkin_Family.init_norm_cache()