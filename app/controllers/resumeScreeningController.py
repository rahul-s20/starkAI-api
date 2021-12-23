from fastapi.responses import JSONResponse
from app.helpers.initiater import io_ResumeScreening


def saveResumeScreeningModel() -> JSONResponse:
    try:
        io_ResumeScreening()
        return JSONResponse(content={"status": True, "type": "Resume Screening", "data": "Working"})
    except Exception as er:
        return JSONResponse(content={"status": True, "type": "Resume Screening", "data": f'{er}'})
