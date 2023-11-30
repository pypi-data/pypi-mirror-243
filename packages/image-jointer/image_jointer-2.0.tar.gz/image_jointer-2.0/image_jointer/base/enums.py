from enum import Enum, auto


class JointAlign(Enum):
    """
    Relative position to the source image.

    SIDE_TOP: Connect to right side of source image. Align the tops of both images.
    SIDE_CENTER: Connect to right side of source image. Align the centers of both images.
    SIDE_BOTTOM: Connect to right side of source image. Align the tops of both images.

    UNDER_LEFT: Connect to bottom of source image. Align the left sides of both images.
    UNDER_CENTER: Connect to bottom of source image. Align the centers of both images.
    UNDER_RIGHT: Connect to bottom of source image. Align the right sides of both images.
    """

    # 元画像の右側に連結する。connect to right side of source image.
    SIDE_TOP = auto()  # 上端ぞろえ。Align the tops of both images.
    SIDE_CENTER = auto()  # 中心ぞろえ。Align the centers of both images.
    SIDE_BOTTOM = auto()  # 下端ぞろえ。Align the tops of both images.
    # 元画像の下側に連結する。
    UNDER_LEFT = auto()  # 左端ぞろえ。Align the left sides of both images.
    UNDER_CENTER = auto()  # 中心ぞろえ。Align the centers of both images.
    UNDER_RIGHT = auto()  # 右端ぞろえ。Align the right sides of both images.


class PositionAlign(Enum):
    """
    Aliment position in a bounding.
    """

    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()

    CENTER_LEFT = auto()
    CENTER_CENTER = auto()
    CENTER_RIGHT = auto()

    BOTTOM_LEFT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_RIGHT = auto()
