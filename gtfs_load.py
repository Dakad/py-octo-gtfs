
import os

from config import Config
from gtfs_model import init as db_init
from gtfs_model import get_class_by_gtfs_filename
from gtfs_model import list_gtfs_model_tablenames
import gtfs_import


def run(by_import=False):

    if by_import is True:
        tablenames_by_gtfs_file = []
        model_tablenames = list_gtfs_model_tablenames()
        gtfs_filenames = os.listdir(Config.GTFS_DIR)

        for model in model_tablenames:
            def match(file_name): return model in file_name

            found = next(filter(match, gtfs_filenames), None)
            if found:
                file_full_path = os.path.join(Config.GTFS_DIR, found)
                tablenames_by_gtfs_file.append((model, file_full_path))

        gtfs_import.run(tablenames_by_gtfs_file)
    else:
        _prepare_insert_gtfs_feeds()


def _prepare_insert_gtfs_feeds():
    from gtfs_process import TaskQueue, insert_gtfs_feed

    LIMIT_BEFORE_COMMIT = 151
    DbSessionMaker = db_init(Config.DB_URI, Config.DEBUG)

    model_tablenames = list_gtfs_model_tablenames()

    tq = TaskQueue(len(model_tablenames))

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

        feed_filename = os.path.join(Config.GTFS_DIR, gtfs_filename)

        # DbSession = DbSessionMaker()
        tq.add_task(insert_gtfs_feed, feed_filename,
                    GTFSModel, DbSessionMaker, limit)

    tq.join()
    return True


if __name__ == '__main__':
    run(True)
    print("Done")
