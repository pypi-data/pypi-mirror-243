
from html import escape
import json
import os
import base64
from .stylers import basic, cifka_advanced

class MIDIPlayer:
    """
    Jupyter-displayable MIDI player that also works on Colab, WandB.
    Supports local MIDI file and/or web-hosted MIDI file via url
    From some original code from Tony Hirsh: https://blog.ouseful.info/2021/11/24/fragment-embedding-srcdoc-iframes-in-jupyter-notebooks/
    Modified by Scott H. Hawley @drscotthawley
    """
    def __init__(self,
        url_or_file,            # url or local filename
        height,                 # Required arg because reasons
        width='100%',
        styler=basic,           # optional callback for generating player HTML
        player_html_maker=None, # backward-compatible duplicate of styler
        viz_type="piano-roll",  # piano-roll, waterfall, staff
        debug=False,):
        self.width, self.height, self.viz_type, self.debug = width, height, viz_type, debug
        if player_html_maker is not None: #backward compatibility, override styler
            styler = player_html_maker
        self.html = self.to_player_html(url_or_file, styler=styler)

    def _repr_html_(self, **kwargs):
        """The part that displays the MIDIPlayer in a Jupyter notebook."""
        return f'''<iframe srcdoc="{escape(self.html)}" width="{self.width}" height="{self.height}"
            style="border:none !important;"
            "allowfullscreen" "webkitallowfullscreen" "mozallowfullscreen">'
            </iframe>'''

    def to_player_html(self, url, styler=basic):
        if os.path.isfile(url): # if url points to local file, convert file to data url
            url = self.to_data_url(url)
        return styler(url, viz_type=self.viz_type)

    def to_data_url(self, midi_filename):  # this is crucial for Colab/WandB support
        with open(midi_filename, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        return 'data:audio/midi;base64,'+encoded_string.decode('utf-8')

    def toJson(self):  # some things want JSON
        return json.dumps(self, default=lambda o: o.__dict__)

    def __getitem__(self, idx, **kwargs): # probly not needed but here anyway
        return self.html[idx]

