## pnt2
Calculating the degree of similarity between two geometric figures of different shapes (by 2 points).

### Installation
```
pip install pnt2
```
### How to use:
```Python
from pathlib import Path

from pnt2.src import cfg_pnt2
from pnt2.src.get_similarity import get_similarity

""" Get input data """
cfg_pnt2.image_name = 'shape_1.png'
cfg_pnt2.templ_name = 'shape_2.png'

path_image = str(Path.cwd() / 'DATA' / cfg_pnt2.image_name)
path_templ = str(Path.cwd() / 'DATA' / cfg_pnt2.templ_name)

similarity = get_similarity(path_image, path_templ)

print(f'\nSimilarity = {round(similarity, 5)}')
```
