import pytest
from PIL import Image
import os
from hide.lsb import encode, embed_data, decode


@pytest.fixture
def setup_image():
    # Create a temporary image for testing
    img_path = "test_image.png"
    new_img_name = "encoded_image.png"
    data = "Hello, World!"

    # Create a simple image
    image = Image.new("RGB", (10, 10), color="white")
    image.save(img_path)

    yield img_path, new_img_name, data

    # Teardown: Remove the temporary images after tests
    if os.path.exists(img_path):
        os.remove(img_path)
    if os.path.exists(new_img_name):
        os.remove(new_img_name)


def test_encode_with_valid_data(setup_image):
    img_path, new_img_name, data = setup_image
    # Test encoding with valid data
    encode(img_path, data, new_img_name)
    assert os.path.exists(new_img_name)


def test_encode_with_empty_data(setup_image):
    img_path, new_img_name, _ = setup_image
    # Test encoding with empty data
    with pytest.raises(ValueError):
        encode(img_path, "", new_img_name)


def test_embed_data(setup_image):
    img_path, _, data = setup_image
    # Test embedding data into an image
    image = Image.open(img_path)
    original_pixels = list(image.getdata())

    embed_data(image, data)
    modified_pixels = list(image.getdata())

    assert original_pixels != modified_pixels

def test_decode(setup_image):
    img_path, new_img_name, data = setup_image
    # Test encoding with valid data
    encode(img_path, data, new_img_name)
    assert os.path.exists(new_img_name)

    # Test decoding the data from the image
    decoded_data = decode(new_img_name)
    assert decoded_data == data

