from CA import *
from CADrawer import *

# for i in xrange(256):
rule = 110
n = 300

ca = CA(rule, n)
ca.start_comp()
# ca.start_random()
ca.loop(n-1)

drawer = PyplotDrawer()
drawer.draw(ca)
drawer.show()
raw_input('')