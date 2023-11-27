import asyncio
import os

from fastapi.staticfiles import StaticFiles
from loguru import logger
from sona.core.inferencer import InferencerBase
from sona.core.messages import Context
from sona.core.messages.result import Result
from sona.settings import settings

from .messages import RPCOfferRequest, SonaResponse
from .rpc.handlers import MediaInferencerHandler

try:
    from aiortc import (
        RTCConfiguration,
        RTCIceServer,
        RTCPeerConnection,
        RTCSessionDescription,
    )
    from fastapi import FastAPI, Request
    from fastapi.exceptions import RequestValidationError
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
except ImportError:
    pass


INFERENCER_CLASS = settings.SONA_INFERENCER_CLASS
STREAM_INFERENCER_CLASS = settings.SONA_STREAM_INFERENCER_CLASS
STATIC_ROOT = os.path.dirname(__file__)

RTC_TURN_FDQN = settings.SONA_STREAM_RTC_TURN_FDQN
RTC_USER = settings.SONA_STREAM_RTC_USER
RTC_PASS = settings.SONA_STREAM_RTC_PASS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.on_event("startup")
async def startup():
    app.peers = set()
    if INFERENCER_CLASS:
        app.inferencer = InferencerBase.load_class(INFERENCER_CLASS)()
        app.inferencer.setup()
        app.inferencer.on_load()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, err: RequestValidationError):
    logger.warning(f"Client Error: {request}, {err.errors()}")
    resp = SonaResponse(code="400", message=str(err.errors()))
    return JSONResponse(status_code=400, content=resp.model_dump())


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, err: Exception):
    logger.exception(f"Server Error: {request}")
    resp = SonaResponse(code="500", message=str(err))
    return JSONResponse(status_code=500, content=resp.model_dump())


@app.get("/ping")
async def ping():
    return SonaResponse(message="pong")


if INFERENCER_CLASS:

    @app.post("/inference")
    async def inference(ctx: Context):
        inferencer: InferencerBase = app.inferencer
        loop = asyncio.get_running_loop()
        next_ctx: Context = await loop.run_in_executor(None, inferencer.on_context, ctx)
        if next_ctx.is_failed:
            raise Exception("Internal Server Error")
        return SonaResponse(result=list(next_ctx.results.values())[0])


if STREAM_INFERENCER_CLASS:
    app.mount("/static", StaticFiles(directory=f"{STATIC_ROOT}/static"), name="static")

    @app.post("/offer")
    async def offer(req: RPCOfferRequest):
        offer = RTCSessionDescription(sdp=req.sdp, type=req.type)
        peer = RTCPeerConnection(
            configuration=RTCConfiguration(
                [
                    RTCIceServer("stun:stun.l.google:19302"),
                    RTCIceServer(RTC_TURN_FDQN, RTC_USER, RTC_PASS),
                ]
            )
        )
        handler = MediaInferencerHandler()

        @peer.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(message):
                if isinstance(message, str) and message.startswith("ping"):
                    channel.send("pong" + message[4:])

        @peer.on("connectionstatechange")
        async def on_connectionstatechange():
            logger.info(f"Connection state is {peer.connectionState}")
            if peer.connectionState == "failed":
                await peer.close()
                app.peers.discard(peer)

        @peer.on("track")
        def on_track(track):
            logger.info(f"Track {track.kind} received")
            if track.kind == "audio":
                handler.addTrack(track, peer)
            elif track.kind == "video":
                peer.addTrack(track)

            @track.on("ended")
            async def on_ended():
                logger.info(f"Track {track.kind} ended")
                await handler.stop(track)

        await peer.setRemoteDescription(offer)
        answer = await peer.createAnswer()
        await peer.setLocalDescription(answer)

        app.peers.add(peer)
        await handler.start()

        return SonaResponse(
            result=Result(
                data={
                    "sdp": peer.localDescription.sdp,
                    "type": peer.localDescription.type,
                }
            )
        )
