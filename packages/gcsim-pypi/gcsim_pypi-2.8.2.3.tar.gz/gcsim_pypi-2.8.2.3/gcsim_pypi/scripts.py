import json
from pathlib import Path

with open(Path(__file__).parent.joinpath("available_characters.json"), "w") as f:
    json.dump(
        [
            f.stem
            for f in (
                Path(__file__)
                .parent.parent.joinpath("gcsim")
                .joinpath("internal")
                .joinpath("characters")
            ).iterdir()
            if f.is_dir()
        ],
        f,
    )

with open(Path(__file__).parent.joinpath("available_artifacts.json"), "w") as f:
    json.dump(
        [
            f.stem
            for f in (
                Path(__file__)
                .parent.parent.joinpath("gcsim")
                .joinpath("internal")
                .joinpath("artifacts")
            ).iterdir()
            if f.is_dir()
        ],
        f,
    )

with open(Path(__file__).parent.joinpath("available_weapons.json"), "w") as f:
    json.dump(
        [
            ff.stem
            for f in (
                Path(__file__)
                .parent.parent.joinpath("gcsim")
                .joinpath("internal")
                .joinpath("weapons")
            ).iterdir()
            if f.is_dir()
            and f.stem in ("sword", "claymore", "spear", "catalyst", "bow")
            for ff in f.iterdir()
        ],
        f,
    )
