"""Import operations."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional

from nextpy.base import Base


def merge_imports(*imports) -> ImportDict:
    """Merge multiple import dicts together.

    Args:
        *imports: The list of import dicts to merge.

    Returns:
        The merged import dicts.
    """
    all_imports = defaultdict(list)
    for import_dict in imports:
        for lib, fields in import_dict.items():
            all_imports[lib].extend(fields)
    return all_imports


class ImportVar(Base):
    """An import var."""

    # The name of the import tag.
    tag: Optional[str]

    # whether the import is default or named.
    is_default: Optional[bool] = False

    # The tag alias.
    alias: Optional[str] = None

    # Whether this import need to install the associated lib
    install: Optional[bool] = True

    # whether this import should be rendered or not
    render: Optional[bool] = True

    @property
    def name(self) -> str:
        """The name of the import.

        Returns:
            The name(tag name with alias) of tag.
        """
        return self.tag if not self.alias else " as ".join([self.tag, self.alias])  # type: ignore

    def __hash__(self) -> int:
        """Define a hash function for the import var.

        Returns:
            The hash of the var.
        """
        return hash((self.tag, self.is_default, self.alias, self.install, self.render))


ImportDict = Dict[str, List[ImportVar]]