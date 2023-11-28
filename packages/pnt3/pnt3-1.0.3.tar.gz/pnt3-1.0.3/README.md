## pnt3
Calculating the degree of similarity between geometric figures of different shapes (by 3 points)

### Installation
```
pip install pnt3
```
### How to use:
```Python
from pathlib import Path
from pnt3.src.get_similarity import get_similarity, calc_similarity, convert_to_canonical

""" Get input data """
path_1 = str(Path.cwd() / 'DATA' / 'first.png')
path_2 = str(Path.cwd() / 'DATA' / 'second.png')

similarity_1 = get_similarity(path_1, path_2)

image_1_can = convert_to_canonical('1', path_1)
image_2_can = convert_to_canonical('2', path_2)

similarity_2 = calc_similarity(image_1_can, image_2_can)

print(f'\nsimilarity_1 = {round(similarity_1, 7)}'
      f'\nsimilarity_2 = {round(similarity_2, 7)}')
```
