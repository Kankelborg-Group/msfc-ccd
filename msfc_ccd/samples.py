"""
Sample FITS files gathered from the MSFC cameras.
"""

import pathlib

__all__ = [
    "path_fe55_esis1",
    "path_fe55_esis3",
]

path_fe55_esis1 = pathlib.Path(__file__).parent / "_data/ESIS1_00002.fit"
"""
An Fe 55 sample image from the ESIS channel 1 camera gathered by the MSFC 
sounding rocket team during camera testing and validation on 2017-07-06. 
"""

path_fe55_esis3 = pathlib.Path(__file__).parent / "_data/ESIS3_05384.fit"
"""
An Fe 55 sample image from the ESIS channel 3 camera gathered by the MSFC 
sounding rocket team during camera testing and validation on 2017-07-12. 
"""
