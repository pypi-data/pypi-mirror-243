from __future__ import annotations
from typing import overload
import scpup


__all__ = [
  "EauLayout",
  "EauPosition",
  "EauGrid"
]


class EauLayout:
  """A value used for setting the position of a coordinate

  Attributes:
    type: The type of layout.
    value: The value that will be used to calculate the position
  """

  __slots__ = (
    "type",
    "value"
  )

  def __init__(self, type: scpup.EauLayoutType, value: int | float = 0):
    """Initialize a layout object with the type and a value.

    Layouts can be created directly but it is highly recommended to use the
    respective classmethod of this class instead.
    EauLayout objects are not aware of what axis are they being used on (x or y)

    Args:
      type: The type of layout.
      value: The value that will be used to calculate the position.
    """
    self.type = type
    self.value = value

  def __add__(self, other: int | EauLayout):
    if isinstance(other, int):
      return EauLayout(self.type, round(self.value + other))
    elif isinstance(other, EauLayout):
      return EauLayout(self.type, self.value + other.value)
    return NotImplemented

  def __radd__(self, other: int):
    if isinstance(other, int):
      return other + self.value
    return NotImplemented

  def __iadd__(self, other: int | EauLayout):
    if isinstance(other, int):
      self.value += other
      return self
    elif isinstance(other, EauLayout):
      self.value += other.value
      return self
    return NotImplemented

  def __sub__(self, other: int | EauLayout):
    if isinstance(other, int):
      return EauLayout(self.type, round(self.value - other))
    elif isinstance(other, EauLayout):
      return EauLayout(self.type, self.value - other.value)
    return NotImplemented

  def __rsub__(self, other: int):
    if isinstance(other, int):
      return other - self.value
    return NotImplemented

  def __isub__(self, other: int | EauLayout):
    if isinstance(other, int):
      self.value -= other
      return self
    elif isinstance(other, EauLayout):
      self.value -= other.value
      return self
    return NotImplemented

  @classmethod
  def Position(cls, value: int | float):
    """Create an EauLayout of Position type

    - Positioning: value
    - Anchor: centerx, centery
    """
    return cls(scpup.EauLayoutType.Position, value)

  @classmethod
  def Top(cls, value: int | float):
    """Create an EauLayout of Top type

    - Positioning: abs(value)
    - Anchor: centerx, top
    """
    return cls(scpup.EauLayoutType.Top, value)

  @classmethod
  def Bottom(cls, value: int | float):
    """Create an EauLayout of Bottom type

    - Positioning: size - abs(value)
    - Anchor: centerx, bottom
    """
    return cls(scpup.EauLayoutType.Bottom, value)

  @classmethod
  def Center(cls, value: int | float = 0):
    """Create an EauLayout of Center type

    - Positioning: size // 2 + value
    - Anchor: centerx, centery
    """
    return cls(scpup.EauLayoutType.Center, value)

  @classmethod
  def Left(cls, value: int | float):
    """Create an EauLayout of Left type

    - Positioning: abs(value)
    - Anchor: left, centery
    """
    return cls(scpup.EauLayoutType.Left, value)

  @classmethod
  def Right(cls, value: int | float):
    """Create an EauLayout of Right type

    - Positioning: size - abs(value)
    - Anchor: right, centery
    """
    return cls(scpup.EauLayoutType.Right, value)

  def parse(self, size: int) -> int | float:
    """Parse the layout and return the computed value. For types that require a
    size you have to pass it here

    Args:
      size:
        The width or height of where this layout will be positionated. Only
        needed in some layout types.

    Raises:
      ValueError: The type of this EayLayout is not a valid layout type.

    Returns:
      int: The computed value of this EauLayout (given it's type and value).
    """
    if self.type == scpup.EauLayoutType.Position:
      return self.value
    elif self.type == scpup.EauLayoutType.Top or self.type == scpup.EauLayoutType.Left:
      return abs(self.value)
    elif self.type == scpup.EauLayoutType.Right or self.type == scpup.EauLayoutType.Bottom:
      return size - abs(self.value)
    elif self.type == scpup.EauLayoutType.Center:
      return size // 2 + (self.value)
    raise ValueError(f"Unknown layout type: {self.type}")


class EauPosition:
  """A position (x, y)

  Attributes:
    x: The EauLayout object for the x coordinate
    y: The EauLayout object for the y coordinate
    margin:
      The space between the boundaries of an imaginary rectangle and the
      boundaries of the game window, if this value is 0 then that imaginary
      rectangle would be the game window rectangle.
  """

  __slots__ = (
    "x",
    "y",
    "margin"
  )

  def __init__(
    self,
    x: int | EauLayout,
    y: int | EauLayout,
    *,
    margin: int | tuple[int, int] | tuple[int, int, int, int] = 0
  ):
    """Initialize a position object

    Args:
      x: The EauLayout describing the x coordinate of this position.
      y: The EauLayout describing the y coordinate of this position.
      margin:
        A value that can be either and int (an equal margin for all sides), a
        tuple with 2 values (first value for left and right, and second value
        for top and bottom), or a tuple with 4 values (each for one side in the
        following order: left, right, top, bottom).
    """
    self.x = x if isinstance(x, EauLayout) else EauLayout.Position(x)
    self.y = y if isinstance(y, EauLayout) else EauLayout.Position(y)
    self.margin = margin

  @classmethod
  def Corner(cls, left: bool, top: bool, x: int, y: int) -> EauPosition:
    return cls(
      EauLayout.Left(x) if left else EauLayout.Right(x),
      EauLayout.Top(y) if top else EauLayout.Bottom(y)
    )

  def as_rectargs(self) -> dict[str, int | float]:
    """Convert this EauPosition instance to a dict with each key being the
    position argument for a pygame.Rect and each value the value for that
    argument."""
    displayService = scpup.EauService.get("EauDisplayService")
    width, height = displayService.size
    if isinstance(self.margin, int):
      ml = mr = mt = mb = self.margin
    elif len(self.margin) == 2:
      (ml, mt), (mr, mb) = self.margin, self.margin
    else:
      ml, mr, mt, mb = self.margin
    xarg = self.x.type.name.lower() if self.x.type in [
      scpup.EauLayoutType.Left,
      scpup.EauLayoutType.Right
    ] else "centerx"
    yarg = self.y.type.name.lower() if self.y.type in [
      scpup.EauLayoutType.Top,
      scpup.EauLayoutType.Bottom
    ] else "centery"
    if self.x.type == scpup.EauLayoutType.Right:
      ml = 0
      width -= mr
    if self.y.type == scpup.EauLayoutType.Bottom:
      mt = 0
      height -= mb
    return {
      xarg: ml + self.x.parse(width - (ml + mr)),
      yarg: mt + self.y.parse(height - (mt + mb))
    }


type EauGridMargin = tuple[int | float, int | float, int | float, int | float] | tuple[int | float, int | float] | int
type EauGridSize = tuple[int | float | None, int | float | None] | int | float | None


class EauGrid:
  """A grid for positioning objects in the game window

  Attributes:
    rows:
      The number of rows that this grid has. If None then this grid won't be
      able to calculate values for 'y' coordinates
    cols:
      The number of columns that this grid has. If None then this grid won't be
      able to calculate values for 'x' coordinates
    margin:
      A tuple equal to the space between the boundaries of an imaginary
      rectangle and the boundaries of the game window, if this value is 0 then
      that imaginary rectangle would be the game window rectangle.
      The tuple has the following structure:
      (margin_left, margin_right, margin_top, margin_bottom)
    size:
      A tuple with the size of the grid. The first value is the width of the
      grid and the second is the height.
  """
  __slots__ = (
    "rows",
    "cols",
    "_margin",
    "_size"
  )

  def __init__(self,
               rows: int | None = None,
               cols: int | None = None,
               *,
               size: EauGridSize = None,
               margin: EauGridMargin = 0):
    """Initializes a grid object

    Args:
      rows: The number of rows that this grid has. Defaults to None.
      cols: The number of columns that this grid has. Defaults to None.
      size:
        A tuple containing the width and height of the grid (w, h). If an int is
        received then it will count as both width and height. If either the
        width or height passed is a number between 0 and 1, then it will be
        taken as a fraction of the whole game display. If None then the whole
        game display size will be used, this also applies to either width or
        height when passing a tuple. Defaults to None. Technically passing None
        is the same as passing (1, 1) or 1
      margin:
        A value that can be either and int (an equal margin for all sides), a
        tuple with 2 values (first value for left and right, and second value
        for top and bottom), or a tuple with 4 values (each for one side in the
        following order: left, right, top, bottom).
    """
    self.rows = rows
    self.cols = cols
    self.margin = margin
    self.size = size
    if margin == 0:
      displaysize = scpup.EauService.get("EauDisplayService").size
      self.margin = (
        (displaysize[0] - self.size[0]) // 2,  # type: ignore
        (displaysize[1] - self.size[1]) // 2  # type: ignore
      )

  @property
  def size(self) -> tuple[int | float, int | float]:
    return self._size

  @size.setter
  def size(self, size: EauGridSize):
    displaysize = scpup.EauService.get("EauDisplayService").size
    if size is None:
      self._size = (displaysize[0] - sum(self.margin[:2]), displaysize[1] - sum(self.margin[2:]))
    elif isinstance(size, (float, int)):
      if 0 <= size <= 1:
        self._size = (displaysize[0] * size, displaysize[1] * size)
      else:
        self._size = (size, size)
    else:
      if size[0] is None:
        width = displaysize[0] - sum(self.margin[:2])
      elif 0 <= size[0] <= 1:
        width = displaysize[0] * size[0]
      else:
        width = size[0]
      if size[1] is None:
        height = displaysize[1] - sum(self.margin[2:])
      elif 0 <= size[1] <= 1:
        height = displaysize[1] * size[1]
      else:
        height = size[1]
      self._size = (width, height)

  @property
  def margin(self) -> tuple[int | float, int | float, int | float, int | float]:
    return self._margin

  @margin.setter
  def margin(self, margin: EauGridMargin):
    if isinstance(margin, int):
      self._margin = (margin, margin, margin, margin)
    elif len(margin) == 2:
      self._margin = (margin[0], margin[0], margin[1], margin[1])
    else:
      self._margin = margin

  def subgrid(self,
              x: int | None = None,
              y: int | None = None,
              *,
              rows: int | None = None,
              cols: int | None = None):
    if not x and not y:
      raise TypeError('Either x or y (or both) have to be passed to know where is the subgrid going to be')
    leftmargin = topmargin = width = height = 0
    if self.cols:
      width = self.size[0] // self.cols
      if x:
        leftmargin = self.margin[0] + self.size[0] * (x - 1) // self.cols
    if self.rows:
      height = self.size[1] // self.rows
      if y:
        topmargin = self.margin[2] + self.size[1] * (y - 1) // self.rows
    return EauGrid(rows=rows, cols=cols, size=(width, height), margin=(leftmargin, 0, topmargin, 0))

  @overload
  def __call__(self, n: int) -> EauLayout:
    """Get the EauLayout of a row / column. This is used when either rows or
    cols is None.

    Args:
      n: The row / column to get. Starting from 1

    Returns:
      EauLayout: The calculated layout of the row / column.
    """
  @overload
  def __call__(self, x: int, y: int) -> EauPosition:
    """Get the EauPosition of a cell

    Args:
      x: The column to get. Starting from 1
      y: The row to get. Starting from 1

    Returns:
      EauPosition: The calculated position of the cell
    """
  def __call__(self, x: int, y: int | None = None) -> EauPosition | EauLayout:  # type: ignore
    if y is not None:
      return self.cell(x, y)
    elif self.rows is None:
      return self.x(x)
    else:
      return self.y(x)

  def x(self, num: int) -> EauLayout:
    """Get the EauLayout of a column.

    Args:
      num: The column to get. Starting from 1.

    Returns:
      EauLayout: The calculated layout of the column.
    """
    if not self.cols:
      raise ValueError("Columns were not specified for this grid.")
    elif 1 > num > self.cols:
      raise ValueError(f"Column value must be between 1 and {self.cols}.")
    w = self.size[0] // (self.cols * 2)
    t = num * 2 - 1
    return EauLayout.Position(self.margin[0] + w * t)

  def y(self, num: int) -> EauLayout:
    """Get the EauLayout of a row.

    Args:
      n: The row to get. Starting from 1.

    Returns:
      EauLayout: The calculated layout of the row.
    """
    if not self.rows:
      raise ValueError("Rows were not specified for this grid.")
    elif 1 > num > self.rows:
      raise ValueError(f"Row value must be between 1 and {self.rows}.")
    w = self.size[1] // (self.rows * 2)
    t = num * 2 - 1
    return EauLayout.Position(self.margin[2] + w * t)

  def cell(self, x: int, y: int) -> EauPosition:
    """Get the EauPosition of a cell

    Args:
      x: The column to get. Starting from 1.
      y: The row to get. Starting from 1.

    Returns:
      EauPosition: The calculated position of the cell
    """
    if not self.rows or not self.cols:
      raise ValueError("Grid is not made for 2 axis.")
    elif 1 <= x <= self.cols and 1 <= y <= self.rows:
      return EauPosition(
        self.x(x),
        self.y(y)
      )
    raise ValueError("Row and column values must be between 1 and the total of each axis.")
