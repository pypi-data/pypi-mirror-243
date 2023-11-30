from tableau_helpers.cli import logs
from tableau_helpers import hyper
from tableau_helpers import server
from tableau_helpers import utils as th_utils
import logging
import os
from pathlib import Path
from tempfile import TemporaryDirectory


class EnvVarNotSet(Exception):
    """
    Exception to be thrown when a required envvar is not set.
    """


def literal(value: str) -> str:
    return value.encode().decode("unicode_escape")


def main():
    loglevel = os.getenv("LOGLEVEL", logging.WARNING)
    loglevel_stdout = os.getenv("LOGLEVEL_STDOUT", None)
    loglevel_stderr = os.getenv("LOGLEVEL_STDERR", logging.WARNING)
    logs.config_logs(loglevel, loglevel_stdout, loglevel_stderr)

    csv_path = os.getenv("TABLEAU_SOURCE_CSV")
    if csv_path is None:
        raise EnvVarNotSet("TABLEAU_SOURCE_CSV")
    csv_path = th_utils.path_or_url(csv_path)
    tabledef_path = os.getenv("TABLEAU_SOURCE_TABLEDEF")

    if tabledef_path is None:
        raise EnvVarNotSet("TABLEAU_SOURCE_TABLEDEF")
    tabledef_path = Path(tabledef_path)
    tableau_project_path = os.getenv("TABLEAU_DEST_PROJECT")
    tabledef = hyper.load_table_def(tabledef_path)
    tabledef_name = tabledef_path.name.split(".", 1)[0]

    if tableau_project_path is None:
        raise EnvVarNotSet("TABLEAU_DEST_PROJECT")

    csv_delimiter = os.getenv("TABLEAU_SOURCE_CSV_DELIMITER", ",")
    csv_delimiter = literal(csv_delimiter)

    with TemporaryDirectory() as tempdir:
        hyperfile_path = Path(tempdir, tabledef_name + ".hyper")
        hyper.copy_csv_to_hyper(
            save_path=hyperfile_path,
            csv=csv_path,
            schema=tabledef,
            delimiter="\t",
            header=True,
            null="NA",
        )
        server.create_or_replace_hyper_file(
            hyperfile_path=hyperfile_path, project=tableau_project_path
        )


if __name__ == "__main__":
    main()
