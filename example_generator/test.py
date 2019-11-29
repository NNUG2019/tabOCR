from save_csv import save_csv
from bare_bones_lister import bare_bones_lister
import time
from bare_bones_generator import bare_bones_generator

bef = time.time()
bare_bones_generator(100, './saved')
aft = time.time()
print("bare_bones_generator: ", aft-bef)

"""
bef = time.time()
lst = bare_bones_lister(5, 10000, 20, 10)
aft = time.time()
print("bare_bones_lister: ", aft-bef)
bef = time.time()
save_csv(lst, './saved')
aft = time.time()
print("save_csv: ", aft-bef)
"""
