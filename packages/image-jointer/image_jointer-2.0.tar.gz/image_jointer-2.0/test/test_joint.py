# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from pathlib import Path

IMAGE_FOLDER = Path("./test/image/")


def test_vector():
    from image_jointer import Vector

    assert Vector(5, 5) + Vector(6, 6) == Vector(11, 11)


def test_joint_side_top():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (100, 200), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.SIDE_TOP)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint" / "SIDE_TOP.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[0:100, 0:100, 0] = 255
    correct_array[0:100, 0:100, 3] = 255
    correct_array[0:200, 100:200, 2] = 255
    correct_array[0:200, 100:200, 3] = 255

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_side_center():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (100, 200), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.SIDE_CENTER)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint" / "SIDE_CENTER.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[50:150, 0:100, 0] = 255
    correct_array[50:150, 0:100, 3] = 255
    correct_array[0:200, 100:200, 2] = 255
    correct_array[0:200, 100:200, 3] = 255

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_side_bottom():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (100, 200), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.SIDE_BOTTOM)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint" / "SIDE_BOTTOM.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[100:200, 0:100, 0] = 255
    correct_array[100:200, 0:100, 3] = 255
    correct_array[0:200, 100:200, 2] = 255
    correct_array[0:200, 100:200, 3] = 255

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_down_left():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (200, 100), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.UNDER_LEFT)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint" / "DOWN_LEFT.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[0:100, 0:100, 0] = 255
    correct_array[0:100, 0:100, 3] = 255
    correct_array[100:200, 0:200, 2] = 255
    correct_array[100:200, 0:200, 3] = 255

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_down_center():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (200, 100), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.UNDER_CENTER)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint" / "DOWN_CENTER.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[0:100, 50:150, 0] = 255
    correct_array[0:100, 50:150, 3] = 255
    correct_array[100:200, 0:200, 2] = 255
    correct_array[100:200, 0:200, 3] = 255

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_down_right():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (200, 100), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.UNDER_RIGHT)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint" / "DOWN_RIGHT.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[0:100, 100:200, 0] = 255
    correct_array[0:100, 100:200, 3] = 255
    correct_array[100:200, 0:200, 2] = 255
    correct_array[100:200, 0:200, 3] = 255

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_nest():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    green = Image.new("RGBA", (100, 100), (0, 255, 0))
    blue = Image.new("RGBA", (100, 100), (0, 0, 255))

    nest0 = (
        ImageJointer(red)
        .joint(green, JointAlign.SIDE_CENTER)
        .joint(ImageJointer(blue).joint(blue, JointAlign.SIDE_CENTER), JointAlign.UNDER_LEFT)
    )
    nest0_image = nest0.to_image()
    nest0_image.save(IMAGE_FOLDER / "joint" / "nest.png")

    nest1 = (
        ImageJointer()
        .joint(ImageJointer(red).joint(blue, JointAlign.UNDER_CENTER), JointAlign.SIDE_CENTER)
        .joint(ImageJointer(green).joint(blue, JointAlign.UNDER_CENTER), JointAlign.SIDE_CENTER)
    )
    nest1_image = nest1.to_image()

    assert np.array_equal(np.asarray(nest0_image), np.asarray(nest1_image))


def test_blank():
    from image_jointer import JointAlign, ImageJointer, Blank
    from PIL import Image
    import numpy as np

    red = Image.new("RGB", (100, 100), (255, 0, 0))
    blank = Blank(50, 100)
    green = Image.new("RGB", (100, 100), (0, 255, 0))

    jointed = ImageJointer(red).joint(blank, JointAlign.SIDE_CENTER).joint(green, JointAlign.SIDE_CENTER)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "blank" / "Blank.png")

    correct_array = np.zeros((100, 250, 4), dtype=np.uint8)
    correct_array[0:100, 0:100, 0] = 255
    correct_array[0:100, 0:100, 3] = 255
    correct_array[0:100, 150:250, 1] = 255
    correct_array[0:100, 150:250, 3] = 255

    assert np.array_equal(np.asarray(joint_img), correct_array)
