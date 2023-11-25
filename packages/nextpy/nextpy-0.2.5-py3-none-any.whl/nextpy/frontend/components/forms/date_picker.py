"""A date input component."""

from nextpy.frontend.components.forms.input import Input
from nextpy.utils.vars import Var


class DatePicker(Input):
    """A date input component."""

    # The type of input.
    type_: Var[str] = "date"  # type: ignore
