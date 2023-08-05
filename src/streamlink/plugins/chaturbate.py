"""
$description model live-streaming
$url chaturbate.com
$type live
"""

import codecs
import json
import re

from streamlink.plugin import Plugin, PluginError, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r'https?://(?:www\.)?chaturbate\.com/[\w-]+'
))
class Chaturbate(Plugin):
    _video_streaming_re = re.compile(
        r'initialRoomDossier\s*=\s*(["\'])(?P<value>(?:(?!\1).)+)\1'
    )
    
    _json_data_schema = validate.Schema({
        'hls_source': validate.any('', validate.url())
    })

    def _lowercase_escape(self, str):
        unicode_escape = codecs.getdecoder('unicode_escape')
        return re.sub(r'\\u[0-9a-fA-F]{4}', lambda m: unicode_escape(m.group(0))[0], str)

    def _get_streams(self):
        page = self.session.http.get(self.url)
        match = self._video_streaming_re.search(page.text)
        
        if match:
            dossier = match.group('value')
            dossier = self._lowercase_escape(dossier)
            data = json.loads(dossier)
            
            try:
                data = self._json_data_schema.validate(data)
            except PluginError:
                return

            hls_url = data['hls_source']
            if hls_url == '':
                return
                
            yield from HLSStream.parse_variant_playlist(self.session, hls_url).items()


__plugin__ = Chaturbate
