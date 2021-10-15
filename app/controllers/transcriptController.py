
from flask import jsonify
from app.common.helpers.helper import transcript_string_formation
from youtube_transcript_api import YouTubeTranscriptApi
from app.common.transcript.transcript_tokenizer import TranscriptsT5F


def transcriptController(vid_id: str) -> dict:
    try:
        response = YouTubeTranscriptApi.get_transcript(video_id=vid_id['vid'], languages=['hn', 'en', 'bn'])
        script = transcript_string_formation(transcript_arr=response)
        transcript_res = TranscriptsT5F().token_handler(script=script)
        return jsonify(status= True, type= "transcript", data= transcript_res)
    except Exception as er:
        return jsonify(status= False, type= "transcript", data= f"{er}")