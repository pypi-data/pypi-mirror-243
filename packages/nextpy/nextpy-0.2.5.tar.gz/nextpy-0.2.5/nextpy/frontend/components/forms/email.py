"""An email input component."""

from nextpy.frontend.components.forms.input import Input
from nextpy.utils.vars import Var


class Email(Input):
    """An email input component."""

    # The type of input.
    type_: Var[str] = "email"  # type: ignore
