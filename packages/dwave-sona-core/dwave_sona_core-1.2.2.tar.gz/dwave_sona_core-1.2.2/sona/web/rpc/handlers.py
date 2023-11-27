import asyncio
import json

from loguru import logger
from sona.core.stream.inferencer import StreamInferencerBase
from sona.core.stream.messages.context import EvtType, StreamContext
from sona.settings import settings
from sona.web.rpc.tracks import AudioInferencerTrack

try:
    from aiortc import MediaStreamTrack, RTCPeerConnection
    from aiortc.mediastreams import MediaStreamError
except ImportError:
    pass

STREAM_INFERENCER_CLASS = settings.SONA_STREAM_INFERENCER_CLASS


class MediaInferencerHandler:
    def __init__(self, inferencer_cls=STREAM_INFERENCER_CLASS) -> None:
        self.inferencer_cls = StreamInferencerBase.load_class(inferencer_cls)
        self.inferencers = {}
        self.tracks = []
        self.queue = asyncio.Queue()

    def addTrack(self, track: MediaStreamTrack, peer: RTCPeerConnection):
        inferencer: StreamInferencerBase = self.inferencer_cls()
        inferencer.setup()
        inferencer.on_load()
        inferencer.on_reply = lambda ctx: self.queue.put_nowait((inferencer, ctx))
        inferencer.reply_channel = peer.createDataChannel(f"reply_{track.id}")
        inferencer.audio_track = AudioInferencerTrack()
        peer.addTrack(inferencer.audio_track)

        self.tracks += [track]
        self.inferencers[track.id] = inferencer

    async def start(self):
        self.task = asyncio.create_task(self.on_reply())
        for track in self.tracks:
            inferencer = self.inferencers[track.id]
            inferencer.task = asyncio.create_task(self.run_track(track, inferencer))

    async def run_track(
        self, track: MediaStreamTrack, inferencer: StreamInferencerBase
    ):
        while True:
            try:
                frame = await track.recv()
                ctx = StreamContext(event_type=EvtType.AV_AUDIO, payload=frame)
                inferencer.on_context(ctx)
            except MediaStreamError:
                logger.warning("MediaStreamError")
                return
            except Exception as e:
                logger.exception(e)
                raise

    async def stop(self, track):
        inferencer = self.inferencers[track.id]
        inferencer.on_stop()
        inferencer.task.cancel()

    async def stop_all(self, track=None):
        for inferencer in self.inferencers.values():
            inferencer.on_stop()
            inferencer.task.cancel()

    async def on_reply(self):
        while True:
            inferencer, ctx = await self.queue.get()
            _type = ctx.event_type
            if _type == EvtType.AV_AUDIO.value:
                inferencer.audio_track.reply(ctx.payload)
            elif _type == EvtType.DICT.value:
                inferencer.reply_channel.send(json.dumps(ctx.payload))
            else:
                raise Exception(
                    "Only support AVAudioStreamData / DictStreamData for now"
                )
