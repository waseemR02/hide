#!/usr/bin/env python3

import argparse
from hide.lsb import encode, decode


def main():
    parser = argparse.ArgumentParser(
        description="Encode and decode data into/from images using LSB technique."
    )
    subparsers = parser.add_subparsers(dest="command")

    encode_parser = subparsers.add_parser("encode", help="Encode data into an image")
    encode_parser.add_argument("img_path", type=str, help="Path to the image file")
    encode_parser.add_argument("data", type=str, help="Data to be encoded")
    encode_parser.add_argument(
        "new_img_name", type=str, help="Name of the new image file"
    )

    decode_parser = subparsers.add_parser("decode", help="Decode data from an image")
    decode_parser.add_argument("img_path", type=str, help="Path to the image file")

    args = parser.parse_args()

    if args.command == "encode":
        encode(args.img_path, args.data, args.new_img_name)
    elif args.command == "decode":
        decoded_data = decode(args.img_path)
        print(f"Decoded data: {decoded_data}")


if __name__ == "__main__":
    main()

