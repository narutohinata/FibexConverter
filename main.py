from posixpath import dirname
import sys
import os
import argparse

from configuration_to_json import build_json



def main():
    print(sys.path)
    parser = argparse.ArgumentParser()
    parser.add_argument("--fibex", dest="fibex_path", required=True)
    parser.add_argument("--output", dest="output_path", required=True)

    args = parser.parse_args()
    if os.path.exists(args.fibex_path):
        print(args.fibex_path)
        with open(args.output_path, 'w') as f:
            build_json([args.fibex_path], f, 0)

if __name__ == "__main__":
    main()