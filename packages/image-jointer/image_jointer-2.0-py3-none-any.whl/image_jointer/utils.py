from __future__ import annotations

from .base.blank import Blank
from .base.enums import JointAlign, PositionAlign
from .base.interfaces import _iSize
from .image_jointer import ImageJointer


class Utility(object):
    def __init__(
        self,
    ):
        raise NotImplementedError("Cannot construct")

    @staticmethod
    def unify_image_size(inputs: tuple[_iSize] | list[_iSize], align: PositionAlign):
        """
        All image will be unified to maximum width and heigh.
        Add transparent padding if image width (height) is smaller then maximum width (height).

        Args:
            inputs (tuple[_iSize] | list[_iSize]): images
            align (PositionAlign): how to add transparent padding

        Returns:
            tuple[ImageJointer]: tuple of adjusted image
        """
        width = max(element.width for element in inputs)
        height = max(element.height for element in inputs)

        match align:
            case PositionAlign.TOP_LEFT:
                height_align = JointAlign.SIDE_TOP
                width_align = JointAlign.UNDER_LEFT
            case PositionAlign.TOP_CENTER:
                height_align = JointAlign.SIDE_TOP
                width_align = JointAlign.UNDER_CENTER
            case PositionAlign.TOP_RIGHT:
                height_align = JointAlign.SIDE_TOP
                width_align = JointAlign.UNDER_RIGHT
            case PositionAlign.CENTER_LEFT:
                height_align = JointAlign.SIDE_CENTER
                width_align = JointAlign.UNDER_LEFT
            case PositionAlign.CENTER_CENTER:
                height_align = JointAlign.SIDE_CENTER
                width_align = JointAlign.UNDER_CENTER
            case PositionAlign.CENTER_RIGHT:
                height_align = JointAlign.SIDE_CENTER
                width_align = JointAlign.UNDER_RIGHT
            case PositionAlign.BOTTOM_LEFT:
                height_align = JointAlign.SIDE_BOTTOM
                width_align = JointAlign.UNDER_LEFT
            case PositionAlign.BOTTOM_CENTER:
                height_align = JointAlign.SIDE_BOTTOM
                width_align = JointAlign.UNDER_CENTER
            case PositionAlign.BOTTOM_RIGHT:
                height_align = JointAlign.SIDE_BOTTOM
                width_align = JointAlign.UNDER_RIGHT

        return tuple(
            ImageJointer(Blank(0, height)).joint(element, height_align).joint(Blank(width, 0), width_align)
            for element in inputs
        )
