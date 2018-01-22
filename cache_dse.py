"""
Design space exploration on cache energy
"""

from jinja2 import Template
from subprocess import call
import numpy as np
import os

cache_size_low = 12     # 2^12=4KB
cache_size_high = 27    # 2^(27-1)=64MB
num_banks_high = 7      # 2^(7-1) = 64 banks
block_size = 64         # 64B

if os.path.exists("cache.cfg.csv"):
    os.rename("cache.cfg.csv", "cache.cfg.csv.bak")

with open("cache.cfg.jinja", "r") as f:
    tmpl = Template(f.read())

for cache_size in np.power(2, range(cache_size_low, cache_size_high)):
    for num_banks in np.power(2, range(num_banks_high)):
        associativity_high = int(np.log2(cache_size/block_size))
        for associativity in np.append(np.power(2, range(associativity_high)), 0):
            if associativity == 0:
                num_search_ports = 1
            else:
                num_search_ports = 0
            
            cfg = tmpl.render(
                cache_size = cache_size,
                num_banks = num_banks,
                associativity = associativity,
                num_search_ports = num_search_ports
            )

            with open("cache.cfg", "w") as f:
                f.write(cfg)

            call(["./cacti", "-infile", "cache.cfg"])
