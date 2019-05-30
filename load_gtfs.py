
import csv


from config import Config


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

    # TODO Init the db and get a DbSession

    # TODO Loop on the gtfs
        # TODO Read the gtfs file
        # TODO Insert each line
        # TODO Bulk add_all into the session
        # TODO Commit on each 50 % read

    pass


if __name__ == '__main__':
    run()
