import os

from datetime import datetime


class ToParamsConverter:
    keys: list

    # convert python data to xml strings for lxml
    def convert(self, value):

        if isinstance(value, datetime):
            value: datetime
            return value.strftime('%Y-%m-%d')

        if type(value) == int:
            return str(value)

        if type(value) == bool:
            return str(value).lower()

        return value

    # prepare params for lxml.etree.build
    def to_params(self):
        return {
            key: self.convert(getattr(
                self, key
            )) for key in self.keys if hasattr(
                self, key
            ) and getattr(self, key) is not None
        }


class Sound(ToParamsConverter):
    # spl fields
    id: int
    hash: str
    url: str
    artist: str
    title: str
    duration: int
    addedOn: datetime
    lastPlayedOn: datetime
    playCount: int

    #
    path: str

    def __init__(self, audio_path, id=None):
        if id is not None:
            self.id = id
            self.keys = ['id', ]
            return

        self.path = audio_path
        self.url = audio_path
        self.title = audio_path.split('/')[-1].replace(
            '.'+audio_path.split('.')[-1], ''
        )
        self.addedOn = datetime.now()
        self.keys = ['url', 'title', 'addedOn', ]

    def parse_id3(self):
        self.artist = ''
        self.duration = 1
        self.keys.extend(['artist', 'duration'])


class Category(ToParamsConverter):
    # spl fields
    type: int
    name: str
    icon: str
    hidden: bool = False

    #
    path: str
    sounds: list

    def __init__(self, directory_path, sounds, icon=None, type=None, hidden=None):

        self.path = directory_path
        self.type = type
        if directory_path:
            self.name = directory_path.split('/')[-1].split('\\')[-1]

        self.hidden = hidden
        self.sounds = sounds if sounds else []

        self.keys = ['type', 'name', 'hidden', ]
        self.get_icon(icon)

    # check icon inside folder and used it if exists
    def get_icon(self, icon):

        self.keys.append('icon')

        if icon:
            self.icon = icon
            return

        # if os.path.isfile('folder.ico'):
        #     return

        self.icon = f'gen_{self.name[0]}'


class Hotbar:
    # spl fields
    id: int
    soundId: int
    
