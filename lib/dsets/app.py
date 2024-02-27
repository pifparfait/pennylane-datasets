from pathlib import Path
from typing import Annotated

import typer

from dsets.lib import progress, s3
from dsets.lib.context import Context

app = typer.Typer(name="dsets", add_completion=True)


@app.command()
def version():
    """Print version and exit."""
    print("0.1.0")


@app.command(name="upload")
def upload(
    src_file: Annotated[
        Path,
        typer.Argument(help="Path to dataset .h5 file", file_okay=True, dir_okay=False),
    ],
) -> None:
    """Upload a new dataset file to the data bucket, and create an upload
    receipt in pennylande-datasets/data.
    """
    ctx = Context()
    src_file = src_file.expanduser()

    repo = s3.S3DatasetRepo(
        ctx.data_dir,
        ctx.s3_client,
        ctx.settings.data_bucket_name,
        ctx.settings.data_bucket_key_prefix,
    )

    print(f"Uploading '{src_file.absolute()}'")
    file_size = src_file.stat().st_size

    with progress.IOProgressBarManager() as pbars:
        key = repo.upload_file(
            src_file,
            hash_progress_cb=pbars.add_bar(file_size, "Generating SHA1 hash.."),
            upload_progress_cb=pbars.add_bar(file_size, "Uploading..."),
        )

    print(f"File uploaded to '{key}'. Be sure to commit upload receipt!")
