# __init__.py
#
# Created:  Aug 2015, T. Lukacyzk
# Modified: Feb 2016, T. MacDonald

from make_hashable import make_hashable

from Object         import Object
from Descriptor     import Descriptor

from Dict           import Dict
from OrderedDict    import OrderedDict
from IndexableDict  import IndexableDict
from HashedDict     import HashedDict

from Bunch          import Bunch
from OrderedBunch   import OrderedBunch
from IndexableBunch import IndexableBunch
from Property       import Property

from DataBunch       import DataBunch
from DiffedDataBunch import DiffedDataBunch

odict  = OrderedDict
idict  = IndexableDict
hdict  = HashedDict
bunch  = Bunch
obunch = OrderedBunch
ibunch = IndexableBunch
dbunch  = DataBunch

import scaling