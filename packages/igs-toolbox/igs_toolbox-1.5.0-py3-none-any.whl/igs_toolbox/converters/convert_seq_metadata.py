import json
import logging
import sys
from datetime import datetime
from pathlib import Path

if sys.version_info >= (3, 10):
    from typing import Annotated, Dict, Optional
else:
    from typing_extensions import Annotated, Dict, Optional

import pandas as pd
import typer

if sys.version_info >= (3, 9):
    from zoneinfo import ZoneInfo
else:
    from backports.zoneinfo import ZoneInfo

import igs_toolbox
from igs_toolbox.formatChecker import json_checker
from igs_toolbox.formatChecker.seq_metadata_schema import SeqMetadataKeys, ValidationError

sys.path.append(Path(__file__).resolve().parent.parent)

NOW = datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%dT%H-%M-%S")


def version_callback(value: bool) -> None:  # noqa: FBT001
    """Print toolbox version."""
    if value:
        print(f"IGS Toolbox Version: {igs_toolbox.__version__}")  # noqa: T201
        raise typer.Exit


app = typer.Typer()


def nest_files_and_upload_entries(entry_dict: Dict[str, str]) -> None:
    """Move files and uploads entries into list of dicts."""
    # If any file entry exists, add to dict
    if any(
        filename in entry_dict for filename in ["FILE_1_NAME", "FILE_1_SHA256SUM", "FILE_2_NAME", "FILE_2_SHA256SUM"]
    ):
        entry_dict[SeqMetadataKeys.FILES.value] = []
        for idx in ["1", "2"]:
            file_info = {}
            for field in ["NAME", "SHA256SUM"]:
                key = f"FILE_{idx}_{field}"
                if key in entry_dict:
                    file_info.update({f"FILE_{field}": entry_dict[key]})
                    del entry_dict[key]
            if len(file_info) > 0:
                entry_dict[SeqMetadataKeys.FILES.value].append(file_info)

    # If any upload entry exists, add to dict
    upload_keys = [
        SeqMetadataKeys.UPLOAD_DATE.value,
        SeqMetadataKeys.UPLOAD_STATUS.value,
        SeqMetadataKeys.UPLOAD_SUBMITTER.value,
        SeqMetadataKeys.REPOSITORY_ID.value,
        SeqMetadataKeys.REPOSITORY_NAME.value,
        SeqMetadataKeys.REPOSITORY_LINK.value,
    ]
    if any(filename in entry_dict for filename in upload_keys):
        entry_dict[SeqMetadataKeys.UPLOADS.value] = [{}]
        for field in upload_keys:
            if field in entry_dict:
                entry_dict[SeqMetadataKeys.UPLOADS.value][0].update({field: entry_dict[field]})
                del entry_dict[field]


@app.command(name="convertSeqMetadata", help="Convert table of seq metadata to json files.")
def convert(
    input_file: Annotated[
        Path,
        typer.Option(
            ...,
            "--input",
            "-i",
            dir_okay=False,
            file_okay=True,
            exists=True,
            help="Path to input excel or csv/tsv file.",
        ),
    ],
    output: Annotated[
        Path,
        typer.Option(
            ...,
            "--output",
            "-o",
            dir_okay=True,
            file_okay=False,
            help="Path to output folder for json files.",
        ),
    ],
    log_file: Annotated[
        Path,
        typer.Option("--log_file", "-l", dir_okay=False, help="Path to log file."),
    ] = Path(f"./output/{NOW}.log"),
    version: Annotated[  # noqa: ARG001
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    log_file.parent.mkdir(exist_ok=True, parents=True)
    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format="%(asctime)s %(levelname)s %(message)s",
        force=True,
    )

    meta_df: pd.DataFrame
    suffix = input_file.suffix
    if suffix == ".csv":
        meta_df = pd.read_csv(input_file, sep=",", dtype=str)
    elif suffix == ".tsv":
        meta_df = pd.read_csv(input_file, sep="\t", dtype=str)
    elif suffix == ".xlsx":
        meta_df = pd.read_excel(input_file, dtype=str)
    else:
        logging.error(f"Files of type {suffix} cannot be converted yet. Please provide either a xlsx, csv or tsv file.")
        raise typer.Abort

    # Create output directory
    output.mkdir(parents=True, exist_ok=True)
    # Convert to json
    meta_dict: list[dict[str, str]] = meta_df.to_dict(orient="records")
    for entry_dict in meta_dict:
        sample_id = entry_dict["LAB_SEQUENCE_ID"]
        # replace NANs
        clean_dict = {k: entry_dict[k] for k in entry_dict if not pd.isna(entry_dict[k])}
        # move files and uploads into nested list
        nest_files_and_upload_entries(clean_dict)
        try:
            with (output / f"{sample_id}_sequencing_metadata.json").open("w") as outfile:
                json.dump(clean_dict, outfile, indent=4)
            json_checker.check_seq_metadata(clean_dict)
            with (output / f"{sample_id}_sequencing_metadata.json").open("w") as outfile:
                json.dump(clean_dict, outfile, indent=4)
        except ValidationError as err:
            logging.exception("Invalid data.")
            raise typer.Abort from err


def main() -> None:
    """Entry point of CLI tool."""
    app()


if __name__ == "__main__":
    main()
