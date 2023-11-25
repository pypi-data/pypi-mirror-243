# coding=utf-8
from pathlib import Path

package_name = (Path(__file__).parent.parent).name


def main():
    print(f"you are use {package_name} package now!!!")


if __name__ == "__main__":
    main()
