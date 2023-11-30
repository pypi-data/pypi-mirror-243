# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from pathlib import Path

IMAGE_FOLDER = Path("./test/image/")


def test_unify_image_size():
    from image_jointer import Blank, ImageJointer, JointAlign, PositionAlign, Utility
    from PIL import Image

    image_tuple = (
        Image.new("RGB", (30, 30), (255, 0, 0)),
        Image.new("RGB", (100, 50), (0, 255, 0)),
        Image.new("RGB", (50, 100), (0, 0, 255)),
        Blank(30, 30),
    )

    for align in PositionAlign:
        result_tuple = Utility.unify_image_size(image_tuple, align)

        assert len(image_tuple) == len(result_tuple)

        jointed = ImageJointer()
        for result in result_tuple:
            assert result.width == 100
            assert result.height == 100
            jointed = jointed.joint(result, JointAlign.SIDE_CENTER)

        joint_img = jointed.to_image()
        joint_img.save(IMAGE_FOLDER / "unify_image_size" / f"{align.name}.png")
