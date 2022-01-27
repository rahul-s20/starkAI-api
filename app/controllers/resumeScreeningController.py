from fastapi.responses import JSONResponse
from app.helpers.initiater import io_ResumeScreening
from app.common.makedecision.resume_decider import ResumeDecisionMaker, decider
from app.helpers.initiater import cleanDataset
from app.schema.ResumeScreeningSchema import ResumeScreeningSchema


def saveResumeScreeningModel() -> JSONResponse:
    try:
        cleaned_resume = io_ResumeScreening()
        rdm = ResumeDecisionMaker()
        res = rdm.save_resume_model(resume_df=cleaned_resume)
        return JSONResponse(content={"status": True, "type": "Resume Screening", "data": res})
    except Exception as er:
        return JSONResponse(content={"status": False, "type": "Resume Screening", "data": f'{er}'})


def resumeScreeningController(input_skills: ResumeScreeningSchema) -> JSONResponse:
    cleand_data_list = []
    try:
        if len(input_skills.skills) > 0:
            for i in input_skills.skills:
                clean_data = cleanDataset(i)
                cleand_data_list.append(clean_data)
            category = decider(input_data=cleand_data_list)
            return JSONResponse(content={"status": True, "type": "Resume Screening", "data": category})
    except Exception as er:
        return JSONResponse(content={"status": False, "type": "Resume Screening", "data": f'{er}'})


def resumeScreeningControllerForAnalysis(input_skills: list) -> list:
    cleand_data_list = []
    try:
        if len(input_skills) > 0:
            for i in input_skills:
                clean_data = cleanDataset(i)
                cleand_data_list.append(clean_data)
            category = decider(input_data=cleand_data_list)
            return category
    except Exception as er:
        cleand_data_list.append(er)
        return cleand_data_list
