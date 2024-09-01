# Hidden Intellectual Data Embedding (HIDE)

Hide is a Python library that implements steganography over images using a Binary Lower Triangle Matrix. We use `uv` to manage the project and run tests.

## Features

- Steganography using Binary Lower Triangle Matrix (to be implemented)
- Least Significant Bit (LSB) steganography (already implemented from GfG)
- Command Line Interface (CLI) to interact with the API

## Installation

To install the required dependencies, use:

```sh
uv sync
```

## Usage

### Encoding

To encode data into an image:

```sh
uv run hide encode something.png {data} encoded.png
```

### Decoding

To decode data from an image:

```sh
uv run hide decode encoded.png
```

## Running Tests

To run the tests, use:

```sh
uvx --with "pillow>=10.4.0" pytest -v
```