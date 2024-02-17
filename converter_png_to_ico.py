import sys
import os
from PIL import Image
from colorama import Fore
from change_icon_folder import set_icon
import shutil


class Converter:
    def __init__(self, args):
        print(Fore.RED + "start")
        self.paths = []
        for i, arg in enumerate(args):
            if arg.lower().endswith('.ico'):
                self.paths.append({"id": i, "state": FileState.ICON, "path": arg})
            elif arg.lower().endswith(('.png', '.jpg', '.bmp', '.tiff')):
                self.paths.append({"id": i, "state": FileState.ANY_IMG, "path": arg})
            elif os.path.isdir(arg):
                self.paths.append({"id": i, "state": FileState.FILE, "path": arg})
            else:
                self.paths.append({"id": i, "state": FileState.NONE, "path": arg})
        self.to_check_paths()

    def to_check_paths(self):

        icons_count = sum(1 for p in self.paths if p["state"] == FileState.ICON)
        other_img = sum(1 for p in self.paths if p["state"] == FileState.ANY_IMG)
        file_count = sum(1 for p in self.paths if p["state"] == FileState.FILE)
        if icons_count + other_img > 1:
            end_script("To many icons")
        elif icons_count + other_img == 0:
            end_script("I didn't get any icon")
        elif file_count == 0:
            end_script("I didn't get any folder")
        self.set_icon_to_folders()

    def set_icon_to_folders(self):
        icon_path = ''
        folders_path = []
        for p in self.paths:
            if p["state"] == FileState.ICON:
                icon_path = p["path"]
                icon_path_reverse = icon_path[::-1]
                file_name = icon_path_reverse[:icon_path.find("\\")][::-1]
                start_path = icon_path[:icon_path.find(r'\Desktop') + 1]

                final_path = start_path + 'icon_res\\' + file_name
                icon_path = final_path
                shutil.copyfile(icon_path, final_path)
            if p["state"] == FileState.ANY_IMG:
                icon_path = p["path"]
                img = Image.open(icon_path)
                if img.format == 'PNG':
                    icon_path = icon_path.replace('.png', '.ico')
                elif img.format == 'JPEG':
                    icon_path = icon_path.replace('.jpg', '.ico')
                elif img.format == 'BMP':
                    icon_path = icon_path.replace('.bmp', '.ico')
                elif img.format == 'TIFF':
                    icon_path = icon_path.replace('.tiff', '.ico')
                icon_path_reverse = icon_path[::-1]
                file_name = icon_path_reverse[:icon_path_reverse.find("\\")][::-1]
                start_path = icon_path[:icon_path.find(r'\Desktop')+1]
                img = img.resize((256, 256))
                if not os.path.isdir(start_path+'icon_res\\'):
                    os.mkdir(start_path+'icon_res\\')
                final_path = start_path + 'icon_res\\' + file_name
                img.save(final_path)
                icon_path = final_path
            if p["state"] == FileState.FILE:
                folders_path.append(p["path"])

        for folder_path in folders_path:
            set_icon(folder_path, icon_path)


class FileState:
    FILE = 0
    ICON = 1
    ANY_IMG = 2
    NONE = -1


def end_script(mess):
    input(f'{mess} >>> PRESS ANY KEY TO END <<<')
    sys.exit(1)


if __name__ == "__main__":
    conv = Converter(sys.argv)
