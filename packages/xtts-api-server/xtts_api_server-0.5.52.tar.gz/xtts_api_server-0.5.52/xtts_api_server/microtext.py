from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time
from RealtimeTTS import TextToAudioStream, CoquiEngine

app = FastAPI()

class SynthesisRequest(BaseModel):
    text: str

# Stopping occurs correctly, but when we start a new stream with new text, 
# we can't do anything with it, the stream stops playing and doesn't work anymore, 
# only restarting helps to fix it
@app.get("/tts_stop")
async def tts_stop():
    global stream
    stream.stop()

# Works great
@app.get("/tts_resume")
async def tts_resume():
    stream.resume()

# Works great
@app.get("/tts_pause")
async def tts_resume():
    stream.pause()

# It works fine, but after we do stream.stop() it crashes and doesn't work anymore.
@app.post("/tts_to_audio")
async def tts_to_audio(request: SynthesisRequest):
    global stream

    if stream.is_playing():
        stream.stop()
        time.sleep(2)

    stream = TextToAudioStream(engine)
    stream.feed(request.text)
    stream.play_async()
    return {"message": "stream"}


if __name__ == '__main__':
    engine = CoquiEngine()
    stream = TextToAudioStream(engine)

    uvicorn.run(app,port=8010)