
import sys
from typing import List, Tuple, Dict, Sequence, Optional, Any, Callable, Union, TypeVar, Literal

if sys.version_info.minor < 10:
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias

Number: TypeAlias = Union[int, float]

import numpy as np

array1D: TypeAlias = np.ndarray
array2D: TypeAlias = np.ndarray

