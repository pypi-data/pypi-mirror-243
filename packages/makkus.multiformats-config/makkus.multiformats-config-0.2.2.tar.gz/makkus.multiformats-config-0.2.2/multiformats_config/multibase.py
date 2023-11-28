r"""
    Utilities to load and build the multibase table.
"""

from __future__ import annotations # See https://peps.python.org/pep-0563/

import importlib.resources as importlib_resources
import json
from typing import Dict, Iterable, Tuple, TYPE_CHECKING

from .config import _enabled_multibases

if TYPE_CHECKING:
    from multiformats.multibase import Multibase

def build_multibase_tables(bases: Iterable[Multibase]) -> Tuple[Dict[str, Multibase], Dict[str, Multibase]]:
    """
        Creates code->encoding and name->encoding mappings from a finite iterable of encodings, returning the mappings.

        Example usage:

        >>> code_table, name_table = build_multicodec_tables(bases)

        :raises ValueError: if the same encoding code or name is encountered multiple times
    """
    # pylint: disable = import-outside-toplevel
    from multiformats.multibase import Multibase
    from multiformats.multibase.err import MultibaseValueError
    # validate(multicodecs, Iterable[Multicodec]) # TODO: not yet properly supported by typing-validation
    code_table: Dict[str, Multibase] = {}
    name_table: Dict[str, Multibase] = {}
    for e in bases:
        if e.code in code_table:
            raise MultibaseValueError(f"Multicodec name {e.name} appears multiple times in table.")
        code_table[e.code] = e
        if e.name in name_table:
            raise MultibaseValueError(f"Multicodec name {e.name} appears multiple times in table.")
        name_table[e.name] = e
    return code_table, name_table

def load_multibase_table() -> Tuple[Dict[str, Multibase], Dict[str, Multibase]]:
    """
        Returns code->encoding and name->encoding mappings created (via :func:`build_multibase_tables`) from the local copy of `multibase-table.json`.
        If a subset of multibases has been enabled, only those multibases are loaded.

        Example usage:

        >>> code_table, name_table = load_multibase_table()

    """
    # pylint: disable = import-outside-toplevel
    from multiformats.multibase import Multibase
    with importlib_resources.open_text("multiformats_config", "multibase-table.json", encoding="utf8") as _table_f:
        table_json = json.load(_table_f)
        multibases = (Multibase(**row) for row in table_json)
        if _enabled_multibases is not None:
            multibases = (m for m in multibases if m.name in _enabled_multibases or m.code in _enabled_multibases)
        code_table, name_table = build_multibase_tables(multibases)
    return code_table, name_table
