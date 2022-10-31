"""
adapted from https://github.com/abba23/beets-popularity/

this works!!!
"""

from beets.plugins import BeetsPlugin
from beets.dbcore import types
import beets.ui as ui
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError
import mediafile

class SeratoPlaycount(BeetsPlugin):
    def __init__(self):
        super(SeratoPlaycount, self).__init__()
        self.item_types = {'seratoplaycount': types.INTEGER}
        self.register_listener('write', self._on_write)

        field = mediafile.MediaField(
            mediafile.MP3DescStorageStyle("seratoplaycount"),
            mediafile.StorageStyle("seratoplaycount")
        )
        self.add_media_field("seratoplaycount", field)

    def commands(self):
        command = ui.Subcommand('seratoplaycount',
                                help='upadate serato play count',
                                aliases=['spc'])
        command.func = self._command
        command.parser.add_option(
            '-n', '--nowrite', action='store_true',
            dest='nowrite', default=False,
            help='print the serato play count values without storing them')
        return [command]

    def _command(self, lib, opts, args):
        # search library for items matching the query
        items = lib.items(ui.decargs(args))

        # query and set spc value for all matching items
        for item in items:
            self._set_spc(item, opts.nowrite)

    def _on_write(self, item, path, tags):
        # query and set serato playcount value for the item that is to be imported
        self._set_spc(item, False)

    def _set_spc(self, item, nowrite):
        try:
            path = item.path.decode()
            id3_tags = ID3(path)
            playcount = id3_tags.get('TXXX:SERATO_PLAYCOUNT')
            if playcount:
                if not nowrite:
                    item.seratoplaycount = playcount.text
                    item.store()

        except ID3NoHeaderError:
            print(f'no ID3 tags: {path}')
            pass
    
