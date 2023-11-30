import os
import shutil
from pathlib import Path
import re
import zipfile

images = []
documents = []
musics = []
videos = []
archives = []

def normalize(directory):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g"
    )

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    p = Path(directory)
    for k in p.glob('**/*'):
        if k.is_file():
            filename = k.name
            m = re.sub('[@#!+~`№$:^&?*()]', '_', filename)
            my_dest = m
            my_source = str(k)
            my_dest = str(k.with_name(my_dest))
            os.rename(my_source, my_dest)
            # print(filename)
            j = m.translate(TRANS)
            my_dest = j
            my_source = str(k.with_name(m))
            my_dest = str(k.with_name(my_dest))
            os.rename(my_source, my_dest)


def sort_files(directory):
    normalize(directory)
    image_extensions = ('jpeg', 'jpg', 'png', 'svg')
    video_extensions = ('avi', 'mp4', 'mov', 'mkv')
    document_extensions = ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx')
    music_extensions = ('mp3', 'ogg', 'wav', 'amr')
    archive_extensions = ('zip', 'gz', 'tar')

    known_extensions = set()
    unknown_extensions = set()

    p = Path(directory)
    for file_path in p.glob('**/*'):
        if file_path.is_file():
            filename = file_path.name
            file_extension = file_path.suffix[1:].lower()

            if file_extension in image_extensions:
                images.append(filename)
                destination = 'images'
                known_extensions.add(file_extension)
            elif file_extension in video_extensions:
                videos.append(filename)
                destination = 'videos'
                known_extensions.add(file_extension)
            elif file_extension in document_extensions:
                documents.append(filename)
                destination = 'documents'
                known_extensions.add(file_extension)
            elif file_extension in music_extensions:
                musics.append(filename)
                destination = 'audio'
                known_extensions.add(file_extension)

            elif file_extension in archive_extensions:
                archives.append(filename)
                destination = 'archives'
                archive_path = str(file_path)
                archive_folder = str(file_path.parent)

            else:
                destination = 'unknown'
                unknown_extensions.add(file_extension)

            destination_directory = p.joinpath(destination)
           # print(destination_directory)
            destination_directory.mkdir(parents=True, exist_ok=True)

            new_file_path = destination_directory.joinpath(filename)
           # print(new_file_path)
            shutil.move(str(file_path), str(new_file_path))
    #print(directory)
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            full_path = os.path.join(root, dir)
            if not os.listdir(full_path):
                os.rmdir(full_path)
    arhive_directory = p.joinpath('archives')
    print(arhive_directory)
    for files in os.walk(arhive_directory):
        for file in files[2]:
            #print(file)
            file_without_ext = os.path.splitext(file)[0]
            pate = os.path.join(arhive_directory, file)
            #print(pate)
            patne = os.path.join(arhive_directory, file_without_ext)
            #print(patne)

            try:
                with zipfile.ZipFile(pate) as zip_file :
                    zip_file.testzip()
                    zip_file.extractall(patne)
            except zipfile.BadZipfile:
                continue



    print("Known file extensions:", ', '.join(known_extensions))
    print("Unknown file extensions:", ', '.join(unknown_extensions))
    print('Documents:', documents)
    print('Music:', musics)
    print('Videos:', videos)
    print('Images:', images)
	

def main():
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)
    directory = sys.argv[1]
    sort_files(directory)

if __name__ == '__main__':
    main()  