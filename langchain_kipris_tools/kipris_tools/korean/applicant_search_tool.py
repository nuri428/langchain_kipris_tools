from langchain_kipris_tools.kipris_api.korean import PatentApplicantSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd
class PatentApplicantSearchArgs(BaseModel):
    applicant: str = Field(..., description="Applicant name is required")
    docs_start: int = Field(1, description="Start index for documents, default is 1")
    docs_count: int = Field(10, description="Number of documents to return, default is 10, range is 1-30")
    patent: bool = Field(True, description="Include patents, default is True")
    utility: bool = Field(True, description="Include utility models, default is True")
    lastvalue:  str = Field("", description="Patent registration status; leave empty for all, (A, C, F, G, I, J, R, or empty)")
    sort_spec: str = Field("AD", description="Field to sort by; default is 'AD'(PD-공고일자, AD-출원일자, GD-등록일자, OPD-공개일자, FD-국제출원일자, FOD-국제공개일자, RD-우선권주장일자)")
    desc_sort: bool = Field(True, description="Sort in descending order; default is True, when True, sort by descending order.it mean latest date first.")


class PatentApplicantSearchTool(BaseTool):
    name:str = "patent_applicant_search"
    description:str = "patent search by applicant name, this tool is for korean patent search"
    api:PatentApplicantSearchAPI = PatentApplicantSearchAPI()
    args_schema:t.Type[BaseModel] = PatentApplicantSearchArgs
    return_direct: bool = False

    def _run(self, applicant:str, docs_start:int=1, docs_count:int=10, patent:bool=True, utility:bool=True, lastvalue:str="", sort_spec:str="AD", desc_sort:bool=True)->pd.DataFrame:
        result = self.api.search(applicant, docs_start, docs_count, patent, utility, lastvalue, sort_spec, desc_sort)
        return result
