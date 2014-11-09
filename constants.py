import site
from collections import namedtuple
LonLat=namedtuple('LonLat','lon,lat')
Box=namedtuple('Box','ll,lr,ur,ul')
ll=LonLat(85.,-10.)
lr=LonLat(160.,-10.)
ur=LonLat(160.,15.)
ul=LonLat(85.,15.)
warm_pool=Box(ll,lr,ur,ul)
