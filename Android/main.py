import time
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.icon_definitions import md_icons
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.textfield import MDTextField

from kivy.utils import platform
from plyer import filechooser
import plyer

import pathlib
import os
import shutil
from cryptography.fernet import Fernet


class Tab(MDFloatLayout, MDTabsBase):
    pass


class Encrypter(MDApp):
    icons = list(md_icons.keys())[15:30]

    def open_filemanager1(self):
        self.filemanager1.show('/')

    def exit_manager1(self):
        self.filemanager1.close()

    def select_path1(self, path):
        print(path)
        self.dec_folder.text = str(path)

        self.exit_manager1()

    def open_filemanager2(self):
        self.filemanager2.show('/')

    def exit_manager2(self):
        self.filemanager2.close()

    def select_path2(self, path):
        print(path)
        self.text.text = str(path)

        self.exit_manager2()

    def open_filemanager(self):
        self.filemanager.show('/')

    def exit_manager(self):
        self.filemanager.close()

    def select_path(self, path):
        print(path)
        self.input.text = str(path)
        self.exit_manager()

    def build(self):

        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Red"

        self.m = MDBoxLayout(
            MDTopAppBar(title="SAT ENCRYPTOR"),
            MDTabs(id="tabs"), orientation="vertical",

        )
        self.filemanager = MDFileManager(select_path=self.select_path, exit_manager=self.exit_manager, preview=True,
                                         )
        self.filemanager1 = MDFileManager(select_path=self.select_path1, exit_manager=self.exit_manager1, preview=True,
                                          )
        self.filemanager2 = MDFileManager(select_path=self.select_path2, exit_manager=self.exit_manager2,
                                          )

        return self.m

    def choose(self, args):
        try:
            # filechooser.choose_dir(on_selection=self.selected)
            self.open_filemanager()

        except:
            pass

    def selected(self, selection):
        print(selection)
        self.input.text = selection
        print(self.input.text)

    def generate_encrypt(self, file):
        self.label1.icon = "lock"
        self.label1.icon_color = "green"
        try:
            path_file = os.path.abspath(file)
            print(path_file)
            with open(path_file, 'rb') as fite:
                original = fite.read()
                fite.close()

            with open(path_file, 'wb') as fi:
                encrypted = self.fernet.encrypt(original)
                fi.write(encrypted)
                print(fi)
                new_name = file + ".sat"
                os.rename(file, new_name)
                fi.close()
        except:
            pass

    def encrypt(self, args):
        key = Fernet.generate_key()
        downloads_path = ""
        try:
            downloads_path = plyer.storagepath.get_downloads_dir().replace("file://", '')
        except Exception as e:
            pass

        pathlib.Path(f"{downloads_path}/Keys").mkdir(exist_ok=True)

        os.chdir(f"{downloads_path}/Keys")
        key_name = str(time.asctime() + ".key")
        with open(key_name, 'wb') as f:
            f.write(key)

        with open(key_name, 'rb') as file_key:
            key = file_key.read()
        self.fernet = Fernet(key)

        try:
          path = str(self.input.text)
          os.chdir(path)
          for file in os.listdir(path):
            self.generate_encrypt(file)
        except:
            pass

    ###################################decrypt#####################################
    def choose_foll(self, args):
        try:

            self.open_filemanager1()
        except:
            pass

    def choose_key(self, args):
        try:
            self.open_filemanager2()
        except:
            pass

    def decrypt(self, args):
        try:
            key_dec = str(self.text.text)
            with open(key_dec, 'rb') as file_key:
                key = file_key.read()
            self.dec_fernet = Fernet(key)
            path = str(self.dec_folder.text)

            os.chdir(path)
            for file in os.listdir(path):
                self.generate_decrypt(file)
        except:
            pass

    def generate_decrypt(self, file):
        self.label2.icon = "lock-open-variant"
        self.label2.icon_color = "green"
        try:
            with open(file, 'rb') as fil:
                orig = fil.read()
                fil.close()

            with open(file, 'wb') as fit:
                decrypted = self.dec_fernet.decrypt(orig)
                fit.write(decrypted)
                curr_name = os.path.splitext(file)
                new_name = str(*curr_name[0:1])
                os.rename(file, new_name)
        except:
            self.label2.icon = "key-alert"
            self.label2.icon_color = "red"
            pass

    def on_start(self):

        if platform == "android":
            from android.permissions import request_permissions, Permission

            def callback(permission, result):
                if all([res for res in result]):
                    pass
                else:
                    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE], callback)

            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE], callback)

        self.label1 = MDIconButton(icon="lock-open-variant", icon_size="68sp",
                                   pos_hint={"center_x": 0.5, "center_y": 0.4}, theme_icon_color="Custom",
                                   icon_color="red")

        self.input = MDTextField(hint_text=" " + "Folder for Encrypt", mode="rectangle", size_hint=(0.8, 1),
                                 pos_hint={"center_x": 0.5, "center_y": 0.7})
        # self.input.text = " "
        self.root.ids.tabs.add_widget(Tab(self.label1, self.input, MDRectangleFlatButton(text="Encrypt", font_size=17,
                                                                                         pos_hint={"center_x": 0.5,
                                                                                                   "center_y": 0.1},
                                                                                         on_press=self.encrypt),
                                          MDIconButton(
                                              icon="folder-plus-outline",
                                              icon_size="48sp",
                                              theme_icon_color="Custom", icon_color="black",

                                              pos_hint={"center_x": .9, "center_y": .9}, on_press=self.choose
                                          ),
                                          title="LOCK",
                                          icon="lock",
                                          ))

        #################tabs2#################
        self.label2 = MDIconButton(icon="lock", icon_size="68sp",
                                   pos_hint={"center_x": 0.5, "center_y": 0.3}, theme_icon_color="Custom",
                                   icon_color="red")

        self.add_file = MDIconButton(
            icon="folder-plus-outline",
            icon_size="48sp",
            theme_icon_color="Custom", icon_color="black",

            pos_hint={"center_x": .7, "center_y": .9}, on_press=self.choose_key
        )

        self.add_decrypt_folder = MDIconButton(
            icon="folder-plus-outline",
            icon_size="48sp",
            theme_icon_color="Custom", icon_color="green",

            pos_hint={"center_x": .9, "center_y": .9}, on_press=self.choose_foll
        )

        self.text = MDTextField(hint_text=" " + "Key file", mode="rectangle",
                                size_hint=(0.8, 1), pos_hint={"center_x": 0.5, "center_y": 0.7})

        self.dec_folder = MDTextField(hint_text=" " + "Folder for Decrypt",
                                      mode="rectangle",
                                      size_hint=(0.8, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})

        # self.dec_folder.text = " "
        self.tab1 = Tab(self.label2, self.add_decrypt_folder, self.text, self.dec_folder, self.add_file,
                        MDRectangleFlatButton(text="Decrypt", font_size=17, pos_hint={"center_x": 0.5, "center_y": 0.1},
                                              on_press=self.decrypt),

                        title="UNLOCK",
                        icon="lock-open-variant",
                        )

        self.root.ids.tabs.add_widget(self.tab1)


if __name__ == "__main__":
    Encrypter().run()
