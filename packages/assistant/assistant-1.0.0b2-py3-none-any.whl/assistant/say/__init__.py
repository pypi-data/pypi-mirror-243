import json
import websockets
import asyncio

from pydub import AudioSegment
from pydub.playback import play

class TTS:
    def __init__(self, host, port, language, speaker_idx="", style_wav=""):
        self.host = host
        self.port = port
        self.language = language
        self.speaker_idx = speaker_idx
        self.style_wav = style_wav
        self.queue = asyncio.Queue(1)
        self.wait = False

    async def pronounce(self):
        while True:
            wav = await self.queue.get()
            if wav:
                play(wav)
            self.queue.task_done()
    
    async def say(self, text: list[str]):
        while self.wait:
            await asyncio.sleep(0.1)
        self.wait = True
        async with websockets.connect(f"ws://{self.host}:{self.port}/api/v1/tts") as ws:
            try:
                j = {
                    'text': text,
                    'speaker_idx': self.speaker_idx,
                    'style_wav': self.style_wav,
                    'language': self.language
                    }
                await ws.send(json.dumps(j).encode('utf-8', 'ignore'))
                wav = await ws.recv()
                try:
                    _wav = AudioSegment(data=wav, sample_width=2, frame_rate=16000, channels=1)
                    await self.queue.put(_wav)
                except Exception as e:
                    raise Exception(e)
            except ConnectionRefusedError as e:
                pass
            except Exception as e:
                raise e
            finally:
                self.wait = False
                await ws.close()
