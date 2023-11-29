# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import requests

from ovos_plugin_manager.templates.stt import STT
from ovos_utils.log import LOG
from speech_recognition import AudioData


class NemoRemoteSTT(STT):
    default_lang = "en"
    public_servers = ["https://nemo.neonaialpha.com"]

    def __init__(self, config: dict = None):
        super().__init__(config)
        self.lang = self.config.get('lang') or self.default_lang
        self.url = self.config.get('url')
        self.api_path = "/stt"
        self.transcriptions = []

    @staticmethod
    def _get_response(audio: AudioData, lang: str, url: str):
        return requests.post(url, data=audio.get_wav_data(),
                             headers={"Content-Type": "audio/wav"},
                             params={"lang": lang})

    def _get_from_public_servers(self, audio: AudioData, lang: str) -> str:
        for url in self.public_servers:
            try:
                r = self._get_response(audio, lang, f"{url}{self.api_path}")
                if r.ok:
                    return r.text.strip('"')
            except:
                continue
        raise RuntimeError(f"All Nemo public servers are down.")

    def execute(self, audio: AudioData, language: str = None) -> str:
        """
        Get STT for the given audio data in the specified language
        @param audio: Input audio data to process
        @param language: Language of input audio
        """
        lang = language or self.lang

        # Check configured endpoint
        if self.url:
            if self.url.endswith(self.api_path):
                url = self.url
            else:
                url = f"{self.url}{self.api_path}"
            resp = self._get_response(audio, lang, url)
            if resp.ok:
                tx = resp.text.strip('"')
                LOG.info(f"Transcribed: {tx}")
                return tx

        try:
            LOG.debug("Get STT from public servers")
            tx = self._get_from_public_servers(audio, lang)
            LOG.info(f"Transcribed: {tx}")
            return tx
        except Exception as e:
            LOG.exception(e)
            return ""

    @property
    def available_languages(self) -> set:
        # TODO: Read from remote API
        return {"en", "es", "fr", "de", "it", "uk", "nl", "pt", "ca"}
