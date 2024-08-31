"""
This module provides functions to encode and decode data into/from images using the Least Significant Bit (LSB) technique.
"""

from PIL import Image


def encode(img_path: str, data: str, new_img_name: str) -> None:
    """
    Encode data into an image and save the new image.

    Args:
    img_path (str): The path to the image file.
    data (str): The data to be encoded into the image.
    new_img_name (str): The name of the new image file to be saved.

    Raises:
    ValueError: If the provided data is empty.
    """
    if not data:
        raise ValueError("Data is empty")

    image = Image.open(img_path, "r")
    new_image = image.copy()
    embed_data(new_image, data)
    new_image.save(new_img_name, new_img_name.split(".")[-1].upper())


def embed_data(image: Image.Image, data: str) -> None:
    """
    Encode the provided data into the given image.

    Args:
    image (Image.Image): The image in which data is to be encoded.
    data (str): The data to be encoded into the image.
    """
    width = image.size[0]
    (x, y) = (0, 0)

    for pixel in modify_pixels(image.getdata(), data):
        # Putting modified pixels in the new image
        image.putpixel((x, y), pixel)
        if x == width - 1:
            x = 0
            y += 1
        else:
            x += 1


def modify_pixels(pixels: iter, data: str) -> iter:
    """
    Modify the pixels to encode the data into the image.

    Args:
    pixels (iter): An iterator of pixel values.
    data (str): The data to be encoded into the image.

    Yields:
    iter: Modified pixel values with encoded data.
    """
    binary_data = generate_binary_data(data)
    data_length = len(binary_data)
    pixel_iterator = iter(pixels)

    for i in range(data_length):
        # Extracting 3 pixels at a time
        pixel_values = [
            value
            for value in next(pixel_iterator)[:3]
            + next(pixel_iterator)[:3]
            + next(pixel_iterator)[:3]
        ]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(8):
            if binary_data[i][j] == "0" and pixel_values[j] % 2 != 0:
                pixel_values[j] -= 1
            elif binary_data[i][j] == "1" and pixel_values[j] % 2 == 0:
                if pixel_values[j] != 0:
                    pixel_values[j] -= 1
                else:
                    pixel_values[j] += 1

        # Eighth pixel of every set tells
        # whether to stop or read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if i == data_length - 1:
            if pixel_values[-1] % 2 == 0:
                if pixel_values[-1] != 0:
                    pixel_values[-1] -= 1
                else:
                    pixel_values[-1] += 1
        else:
            if pixel_values[-1] % 2 != 0:
                pixel_values[-1] -= 1

        pixel_tuple = tuple(pixel_values)
        yield pixel_tuple[0:3]
        yield pixel_tuple[3:6]
        yield pixel_tuple[6:9]


def generate_binary_data(data: str) -> list[str]:
    """
    Convert encoding data into 8-bit binary form using ASCII value of characters.

    Args:
    data (str): The string data to be converted.

    Returns:
    list[str]: A list of binary strings representing the input data.
    """
    return [format(ord(char), "08b") for char in data]


def decode(img_path: str) -> str:
    """
    Decode data from an image provided by the user.

    Args:
    img_path (str): The path to the image file.

    Returns:
    str: The decoded data from the image.
    """
    image = Image.open(img_path, "r")

    decoded_data = ""
    pixel_iterator = iter(image.getdata())

    while True:
        pixels = [
            value
            for value in next(pixel_iterator)[:3]
            + next(pixel_iterator)[:3]
            + next(pixel_iterator)[:3]
        ]

        binary_str = ""

        for i in pixels[:8]:
            binary_str += "0" if i % 2 == 0 else "1"

        decoded_data += chr(int(binary_str, 2))
        if pixels[-1] % 2 != 0:
            break

    return decoded_data
