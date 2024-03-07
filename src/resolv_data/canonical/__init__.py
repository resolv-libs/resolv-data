"""
Author: Matteo Pettenò.
Copyright (c) 2024, Matteo Pettenò
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""
from . import adapters
from . import exceptions
from .base import CanonicalFormat, DataAdapter
from .wrapper import to_canonical_format, to_source_format
