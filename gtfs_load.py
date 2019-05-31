
import csv
import os


from config import Config
from gtfs_model import init as db_init, get_class_by_gtfs_filename
from gtfs_model import get_class_by_gtfs_filename
from gtfs_model import list_gtfs_model_tablenames


def run():
    LIMIT_BEFORE_COMMIT = 151
    DbSession = db_init(Config.DB_URI, Config.DEBUG)

    model_tablenames = list_gtfs_model_tablenames()
    print(model_tablenames)

    for gtfs_filename in os.listdir(Config.GTFS_DIR):
        filename, ext = os.path.splitext(gtfs_filename)
        if 'txt' not in ext:
            continue

        GTFSModel = get_class_by_gtfs_filename(filename)
        if(GTFSModel == None):
            continue

        # The GTFS feeds can be huuge, thus contains plenty of lines
        # At the date of this script : May 31th 2019
        #   The stop_time.txt has :
        #       size: 158.1 Mb     # Lines: 3,332,540
        #   The trips.txt has :
        #       size: 10 Mb        # Lines: 154,883
        # Reduce the number of commits- to exec by increasing the number of
        # INSERT statements to hold before  commit

        if filename == 'trips':
            limit = LIMIT_BEFORE_COMMIT * 10  # 1510
        elif filename == 'stop_times':
            limit = LIMIT_BEFORE_COMMIT ** 2  # 151²
        else:
            limit = LIMIT_BEFORE_COMMIT

        # TODO Threadify the reading and insert gtfs feed to reduce the app running time

        feed_filename = os.path.join(Config.GTFS_DIR, gtfs_filename)

        process_gtfs_feed(feed_filename, GTFSModel, DbSession, limit)

        if DbSession.is_active:
            DbSession.commit()


def _read_gtfs_feed(feed_file_name):
    with open(feed_file_name, "r") as gtfs_file:
        gtfs_reader = csv.reader(gtfs_file)
        head = next(gtfs_reader)

        for row in gtfs_reader:
            new_line = dict(zip(head, row))
            new_line = dict((k, v)
                            for k, v in new_line.items() if v != '')
            yield new_line


def process_gtfs_feed(feed_filename, model, session, limit=0):
    for counter, feed in enumerate(_read_gtfs_feed(feed_filename)):

        if 'stop_times' in feed_filename:
            q = session.query(model).filter_by(
                trip_id=feed['trip_id'],
                stop_id=feed['stop_id'])

            exists = session.query(
                model.id).filter(q.exists()).scalar()
            print(exists)
            if not exists:
                gtfs_feed = model(**feed)
                session.add(gtfs_feed)
                session.commit()
            continue

        gtfs_feed = model(**feed)
        session.add(gtfs_feed)

        if counter % limit == 0:
            session.commit()


if __name__ == '__main__':
    run()
    print("Done")
