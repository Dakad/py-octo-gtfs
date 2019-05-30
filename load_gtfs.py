
import csv


from config import Config


def _read_gtfs_feed(feed_file_name):
    with open(feed_file_name, "r") as gtfs:
        gtfs_reader = csv.reader(gtfs)
        head = next(gtfs_reader)

        for row in gtfs_reader:
            new_line = dict(zip(head, row))
            new_line = dict((k, v)
                            for k, v in new_line.items() if v != '')
            yield new_line


def run():
    pass


if __name__ == '__main__':
    run()
