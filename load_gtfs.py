
import csv
import os


from config import Config
from gtfs_model import init as db_init, get_class_by_gtfs_filename


def _read_gtfs_feed(feed_file_name):
    with open(feed_file_name, "r") as gtfs_file:
        gtfs_reader = csv.reader(gtfs_file)
        head = next(gtfs_reader)

        for row in gtfs_reader:
            new_line = dict(zip(head, row))
            new_line = dict((k, v)
                            for k, v in new_line.items() if v != '')
            yield new_line


def run():

    # TODO Get the DB_URI from Config
    DbSession = db_init(Config.DB_URI, Config.DEBUG)

    for gtfs_filename in os.listdir(Config.GTFS_DIR):
        filename, ext = os.path.splitext(gtfs_filename)
        if 'txt' not in ext:
            continue
        GTFSModel = get_class_by_gtfs_filename(filename)

        feed_filename = os.path.join(Config.GTFS_DIR, gtfs_filename)
        read_counter = 0
        for feed in _read_gtfs_feed(feed_filename):
            gtfs_feed = GTFSModel(**feed)
            DbSession.add(gtfs_feed)

        DbSession.commit()

    # TODO Insert each line
    # TODO Bulk add_all into the session
    # TODO Commit on each 50 % read

    pass


if __name__ == '__main__':
    run()
