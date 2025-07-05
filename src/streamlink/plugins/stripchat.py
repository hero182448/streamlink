"""
$description model live-streaming
$url stripchat.com
$type live
"""

import codecs
import json
import re

from streamlink.plugin import Plugin, PluginError, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r'https?://(?:www\.)?stripchat\.com/[\w-]+'
))
class Stripchat(Plugin):
    # Regex to extract the text between
    # <script>window.__PRELOADED_STATE__= and </script>
    _video_streaming_re = re.compile(
        r'<script>\s*window\.__PRELOADED_STATE__\s*=\s*(?P<value>\{.*?\})\s*</script>'
    )

    # Schema to validate the JSON structure
    _json_data_schema = validate.Schema({
        'viewCamBase': {
            'model': {
                'id': int
            }
        }
    })

    # Decode unicode escape sequences to real characters
    def _lowercase_escape(self, str):
        unicode_escape = codecs.getdecoder('unicode_escape')
        return re.sub(r'\\u[0-9a-fA-F]{4}', lambda m: unicode_escape(m.group(0))[0], str)

    # Extract and yield available HLS streams
    def _get_streams(self):

        # Set a realistic User-Agent and Accept headers to simulate a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        # Fetch the HTML page
        page = self.session.http.get(self.url, headers=headers)
        match = self._video_streaming_re.search(page.text)

        if match:
            # Extract and decode the raw JSON string
            state = match.group('value')
            state = self._lowercase_escape(state)
            data = json.loads(state)
            
            # Validate structure using the schema
            try:
                data = self._json_data_schema.validate(data)
            except PluginError:
                return

            # Construct the HLS stream URL
            id = data['viewCamBase']['model']['id']
            hls_url = f'https://edge-hls.doppiocdn.com/hls/{id}/master/{id}_auto.m3u8?playlistType=lowLatency'
  
            # Parse and yield available HLS streams
            yield from HLSStream.parse_variant_playlist(self.session, hls_url).items()


__plugin__ = Stripchat
