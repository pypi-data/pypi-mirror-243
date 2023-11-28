import re
import json
from pathlib import Path

GCSIM_PATH = Path(__file__).parent.joinpath("gcsim")
GCSIM_PYPI_PATH = Path(__file__).parent.joinpath("gcsim_pypi")


def generate_availability():
    print("Generating character availability...")
    with open(
        GCSIM_PYPI_PATH.joinpath("availability").joinpath("characters.py"),
        "w",
    ) as f:
        f.write("AVAILABLE_CHARACTERS = {\n")
        for character in sorted(
            list(
                set(
                    next(
                        filter(
                            lambda line: line.startswith("key:"),
                            f.read_text().split("\n"),
                        ),
                        f.parent.stem,
                    )
                    .split(" ")[-1]
                    .strip('"')
                    for f in (
                        GCSIM_PATH.joinpath("internal").joinpath("characters")
                    ).rglob("config.yml")
                ).union(
                    match
                    for match in re.findall(
                        r"\"(\w+)\":[ ]*keys",
                        GCSIM_PATH.joinpath("pkg")
                        .joinpath("shortcut")
                        .joinpath("characters.go")
                        .read_text(),
                    )
                )
            )
        ):
            f.write(f'  "{character}",\n')
        f.write("}")

    print("Generating artifact availability...")
    with open(
        Path(__file__)
        .parent.joinpath("gcsim_pypi")
        .joinpath("availability")
        .joinpath("artifacts.py"),
        "w",
    ) as f:
        f.write("AVAILABLE_ARTIFACTS = {\n")
        for art in sorted(
            list(
                set(
                    [
                        next(
                            filter(
                                lambda line: line.startswith("key:"),
                                f.read_text().split("\n"),
                            ),
                            f.parent.stem,
                        )
                        .split(" ")[-1]
                        .strip('"')
                        for f in (
                            Path(__file__)
                            .parent.joinpath("gcsim")
                            .joinpath("internal")
                            .joinpath("artifacts")
                        ).rglob("config.yml")
                    ]
                ).union(
                    match
                    for match in re.findall(
                        r"\"(\w+)\":[ ]*keys",
                        GCSIM_PATH.joinpath("pkg")
                        .joinpath("shortcut")
                        .joinpath("artifacts.go")
                        .read_text(),
                    )
                )
            )
        ):
            f.write(f'  "{art}",\n')
        f.write("}")

    print("Generating weapon availability...")
    with open(
        Path(__file__)
        .parent.joinpath("gcsim_pypi")
        .joinpath("availability")
        .joinpath("weapons.py"),
        "w",
    ) as f:
        f.write("AVAILABLE_WEAPONS = {\n")
        for weapon in sorted(
            list(
                set(
                    next(
                        filter(
                            lambda line: line.startswith("key:"),
                            f.read_text().split("\n"),
                        ),
                        f.parent.stem,
                    )
                    .split(" ")[-1]
                    .strip('"')
                    for f in (
                        Path(__file__)
                        .parent.joinpath("gcsim")
                        .joinpath("internal")
                        .joinpath("weapons")
                    ).rglob("config.yml")
                ).union(
                    match
                    for match in re.findall(
                        r"\"(\w+)\":[ ]*keys",
                        GCSIM_PATH.joinpath("pkg")
                        .joinpath("shortcut")
                        .joinpath("weapons.go")
                        .read_text(),
                    )
                )
            )
        ):
            f.write(f'  "{weapon}",\n')
        f.write("}")


if __name__ == "__main__":
    generate_availability()
