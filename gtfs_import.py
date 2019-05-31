import subprocess

from config import Config


def run(tablenames_by_gtfs_file):
    proc_args = [
        "sqlite3",
        Config.DB_DIR,
    ]

    proc_args.append(".mode csv")
    for (table_name, file_name) in tablenames_by_gtfs_file:
        proc_args.append(".import '{}' {}".format(file_name, table_name))

    subprocess.run(proc_args)
