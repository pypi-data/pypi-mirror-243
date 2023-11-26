Vanilla = 1
Chocolate = 2
Strawberry = 3

import numpy as np

def make_icecream():
    return np.random.choice([Vanilla, Chocolate, Strawberry])

icecream = make_icecream()
if icecream == Vanilla:
    print("Yum!")
else:
    print("Yuck!")
