from pathlib import Path
import sys
import shutil
import os
from threading import Thread, RLock
import logging
from time import time


def path_check():
    if len(sys.argv) == 1:
        try_input = input("Please, input path to 'UNSORTED' directory::::")
        if os.path.exists(try_input) and Path(try_input).is_dir():
            returned_path = Path(fr"{try_input}")
            print(returned_path, '>>>>argument were taken from "INPUT 1"<<<<')
        else:
            print("Recursive check completed.")
            returned_path = path_check()
    elif len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]) and Path(sys.argv[1]).is_dir():
            returned_path = Path(fr"{sys.argv[1]}")
            print('>>>>argument were taken from "TERMINAL ARGS"<<<<')
        else:
            print("Paht not exists")
            while True:
                try_input = input("Please, input path to 'UNSORTED' directory::::")
                if os.path.exists(try_input) and Path(try_input).is_dir():
                    returned_path = Path(fr"{try_input}")
                    print(returned_path, '>>>>argument were taken from "INPUT 2"<<<<')
                    break
    return returned_path


def cleaner(directory):
    for trash in directory.iterdir():
        try:
            if trash.is_dir():
                cleaner(trash)
                trash.rmdir()
        except OSError:
            continue
    return  # print("Directory was cleaned.")


def translate(name_file):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n",
        "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "",
        "e", "yu", "ya", "je", "i", "ji", "g"
    )
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
        translated = name_file.translate(TRANS)
    return translated


def normalize(name_file):
    import re
    normalize = re.sub(r"[^\w]", "_", translate(name_file))
    return normalize.strip()


def sort_this_dir(lock, PATH):
    logging.debug('Insider ON!!!!!!!!')

    list_pictures = []
    list_video = []
    list_documents = []
    list_music = []
    list_archives = []
    list_directory = []
    list_unknown_type = []

    categories = {
        "Pictures": list_pictures,
        "Video": list_video,
        "Documents": list_documents,
        "Music": list_music,
        "Archives": list_archives,
        "UNKNOWN file type": list_unknown_type,
        "Was found directory(es)": list_directory
    }

    pic_type = [".jpeg", ".png", ".jpg", ".svg", ".bmp"]
    vid_type = [".avi", ".mp4", ".mov", ".mkv"]
    doc_type = [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"]
    mus_type = [".mp3", ".ogg", ".wav", ".amr"]
    arc_type = [".zip", ".gz", ".tar"]  # NO RAR TYPE FILES

    pic_dir = Path(PATH_TO_UNSORTED.joinpath("pictures"))
    vid_dir = Path(PATH_TO_UNSORTED.joinpath("video"))
    doc_dir = Path(PATH_TO_UNSORTED.joinpath("documents"))
    mus_dir = Path(PATH_TO_UNSORTED.joinpath("audio"))
    arc_dir = Path(PATH_TO_UNSORTED.joinpath("archives"))
    nft_dir = Path(PATH_TO_UNSORTED.joinpath("unknown_type_files"))

    if PATH.is_dir():

        for item in PATH.iterdir():
            with lock:
                if item.suffix in pic_type:
                    list_pictures.append(item.name)
                    logging.debug('Insider on duty')
                    if not pic_dir.is_dir():
                        pic_dir.mkdir(parents=True, exist_ok=True)
                        logging.debug('Insider on duty')
                    item = item.replace(pic_dir.joinpath(item.name))
                    normalized_item = (normalize(item.stem)) + item.suffix
                    item = item.rename((item.parent).joinpath(normalized_item))
                    logging.debug('Insider on duty')
                elif item.suffix in vid_type:
                    list_video.append(item.name)
                    logging.debug('Insider on duty')
                    if not vid_dir.is_dir():
                        vid_dir.mkdir(parents=True, exist_ok=True)
                        logging.debug('Insider on duty')
                    item = item.replace(vid_dir.joinpath(item.name))
                    normalized_item = (normalize(item.stem)) + item.suffix
                    item = item.rename((item.parent).joinpath(normalized_item))
                    logging.debug('Insider on duty')
                elif item.suffix in doc_type:
                    list_documents.append(item.name)
                    logging.debug('Insider on duty')
                    if not doc_dir.is_dir():
                        doc_dir.mkdir(parents=True, exist_ok=True)
                        logging.debug('Insider on duty')
                    item = item.replace(doc_dir.joinpath(item.name))
                    normalized_item = (normalize(item.stem)) + item.suffix
                    item = item.rename((item.parent).joinpath(normalized_item))
                    logging.debug('Insider on duty')
                elif item.suffix in mus_type:
                    logging.debug('Insider on duty')
                    list_music.append(item.name)
                    if not mus_dir.is_dir():
                        mus_dir.mkdir(parents=True, exist_ok=True)
                        logging.debug('Insider on duty')
                    item = item.replace(mus_dir.joinpath(item.name))
                    normalized_item = (normalize(item.stem)) + item.suffix
                    item = item.rename((item.parent).joinpath(normalized_item))
                    logging.debug('Insider on duty')
                elif item.suffix in arc_type:
                    list_archives.append(item.name)
                    logging.debug('Insider on duty')
                    if not arc_dir.is_dir():
                        arc_dir.mkdir(parents=True, exist_ok=True)
                        logging.debug('Insider on duty')
                    item = item.replace(arc_dir.joinpath(item.name))
                    normalized_item = (normalize(item.stem)) + item.suffix
                    item = item.rename((item.parent).joinpath(normalized_item))
                    unpuck_arc_dir = arc_dir.joinpath(item.stem)
                    unpuck_arc_dir.mkdir(parents=True, exist_ok=True)
                    shutil.unpack_archive(item, unpuck_arc_dir)
                    logging.debug('Insider on duty')
                    for unpucked in unpuck_arc_dir.iterdir():
                        normalized_unpucked = (normalize(unpucked.stem)) + unpucked.suffix
                        unpucked = unpucked.rename((unpucked.parent).joinpath(normalized_unpucked))
                        logging.debug('Insider on duty')
                elif item.is_dir():
                    logging.debug('Insider on duty')
                    if item.is_dir() != pic_dir or vid_dir or doc_dir or mus_dir or arc_dir or nft_dir:
                        list_directory.append(item.name)
                        sort_this_dir(lock, item)
                    else:
                        continue
                else:
                    list_unknown_type.append(item.name)
                    logging.debug('Insider on duty')
                    if not nft_dir.is_dir():
                        nft_dir.mkdir(parents=True, exist_ok=True)
                        logging.debug('Insider on duty')
                    item = item.replace(nft_dir.joinpath(item.name))
                    normalized_item = (normalize(item.stem)) + item.suffix
                    item = item.rename((item.parent).joinpath(normalized_item))
                    logging.debug('Insider on duty')

    else:
        return print("..........Sorry, you specified a non-existent path. Please try again...........")
        logging.debug('Insider on duty')


if __name__ == '__main__':
    timer = time()
    logging.basicConfig(level=logging.DEBUG, format='%(msecs)d %(threadName)s %(message)s %(lineno)d')
    threads = []
    locker = RLock()
    PATH_TO_UNSORTED = path_check()

    for i in range(10):
        thread = Thread(target=sort_this_dir, args=(locker, PATH_TO_UNSORTED,))
        thread.start()
        threads.append(thread)
        logging.debug('Started!!!!!')

    [el.join() for el in threads]
    [logging.debug(f'{el.is_alive()}') for el in threads]
    cleaner(PATH_TO_UNSORTED)
    logging.debug(f'Done {time() - timer}')

    exit()
