import os
import re

from collections import deque

from .fields import Sound, Category
from .xml import CATEGORY, SOUND_IN_CAT


# only work with this extensions
AUDIO_EXTENSIONS = [
    'mp3', 'wav', 'm4a', 'ogg'
]
# don't walk inside this dirs
SKIP_DIRECTORIES = ['app', ]
# and skip this files from being parsed
#SKIP_FILES = [, ]
# scan or not id3 tags from each file for grab artist and title
SCAN_ID3 = False
ADD_EMPTY_DIRS = True


class DirectoryData:

    sounds: list = []
    categories: list = []

    def dir_walk(self, path):

        for (
                directory_path, directory_names, file_names
        ) in os.walk(path):

            # skip current directory if its hided
            if not re.search('/', directory_path) and any(
                    [
                        directory_path.startswith(x) for x in ('.', '_',)
                        ]):
                return

            # also check if any directory in current path are hided an skip it
            if re.search('/', directory_path):
                for d in directory_path.split('/'):
                    if any(
                            [
                                d.startswith(x) for x in ('.', '_')
                                ]
                    ):
                        return

            # search for audio files in current directory
            audio_files = [
                x for x in file_names if any(
                    [x.endswith(f'.{y}') for y in AUDIO_EXTENSIONS]
                )
            ]

            # make Sound param for SoundList category
            sounds = []
            if audio_files:
                _sounds = [
                    Sound(
                        f'{directory_path}/{audio}'
                    ) for audio in audio_files
                ]

                self.sounds.extend(_sounds)
                sounds = [
                    SOUND_IN_CAT(
                        **Sound(None, id=self.sounds.index(snd)).to_params()
                    ) for snd in _sounds
                ]

            # if current directory in tree have another directory
            # then walk inside it
            # after prepare xml and append result
            # to current Categories data
            if directory_names:
                _directories = []
                for _dir in directory_names:
                    walk = self.dir_walk(
                        os.path.join(directory_path, _dir)
                    )
                    if walk:
                        _directories.append(walk)

                # append Category and Sounds for Category param
                if _directories and sounds:
                    return CATEGORY(
                        *_directories,
                        *sounds,
                        **Category(directory_path, None).to_params(),
                    )

                # only Category
                if _directories and not sounds:
                    return CATEGORY(
                        *_directories,
                        **Category(directory_path, None).to_params(),
                    )

            # only Sound if no more dirs in this folder
            if sounds:
                return CATEGORY(
                    *sounds,
                    **Category(directory_path, sounds).to_params(),
                )

        # return only Category path for get this name
        return CATEGORY(
            **Category(
                path, None,
            ).to_params()
        )

    # deep walk through all dirs and files in current folder
    def scan_files(self):

        for _dir in os.listdir():
            if os.path.isdir(_dir):
                back = self.dir_walk(
                    os.path.join(os.getcwd(), _dir)
                )
                # ignore if last directory in walk tree
                # didn't contain anything (None)
                if back:
                    self.categories.append(back)

    def get_data(self, categories: bool):
        if not self.sounds:
            self.scan_files()

        # return sounds data for SoundList category
        if not categories:
            return self.sounds

        # return data for Categories category
        return self.categories






