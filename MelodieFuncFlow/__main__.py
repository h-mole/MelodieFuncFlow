import argparse


def main():
    parser = argparse.ArgumentParser(description="Module Template")

    parser.add_argument("-f", "--file", type=str, help="Please input filename")
    parser.add_argument("--value", type=int, help="Please input integer value")

    args = parser.parse_args()

    print("argument-file:", args.file)
    print("argument-value:", args.value)


if __name__ == "__main__":
    main()
