
from app.common.helpers.helper import transcript_string_formation
from youtube_transcript_api import YouTubeTranscriptApi
from app.common.transcript.transcript_tokenizer import TranscriptsT5F
from app.schema.TransriptSchema import TransriptSchema
from fastapi.responses import JSONResponse


def transcriptController(vid_id: TransriptSchema) -> JSONResponse:
    try:
        response = YouTubeTranscriptApi.get_transcript(video_id=vid_id.vid, languages=['hn', 'en', 'bn'])
        script = transcript_string_formation(transcript_arr=response)
        transcript_res = TranscriptsT5F().token_handler(script=script)
        res = {"status": True, "type": "transcript", "data": transcript_res}
        return JSONResponse(content=res)
    except Exception as er:
        res = {"status": False, "type": "transcript", "data": f"{er}"}
        return JSONResponse(content=res)