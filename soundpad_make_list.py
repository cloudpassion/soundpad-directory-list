import lxml.etree

from app.fields import Category
from app.files import DirectoryData
from app.xml import (
    SOUND_LIST, SOUND_IN_LIST, CATEGORIES, CATEGORY
)

SPL_ENCODING = 'UTF-8'
SPL_FILE = 'output.spl'

directory_database = DirectoryData()

spl_data = SOUND_LIST(
    *[
        SOUND_IN_LIST(
            **snd.to_params()
        ) for snd in directory_database.get_data(categories=False)
    ],
    CATEGORIES(
        CATEGORY(
            **Category(
                None, None, type=1, icon='stock_icon_cat_list',
                hidden=False
            ).to_params(),
        ),
        *directory_database.get_data(categories=True)
    ),
    # HOT_BAR(),
)

with open(SPL_FILE, 'wb') as sw:
    sw.write(
        lxml.etree.tostring(
                spl_data,
                encoding=SPL_ENCODING,
                pretty_print=True, 
                xml_declaration=True
            )
    )

