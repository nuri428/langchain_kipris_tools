from langchain_kipris_tools.kipris_api.abs_class import ABSKiprisAPI
from langchain_kipris_tools.kipris_api.utils import get_nested_key_value
import typing as t
import pandas as pd
from langchain_kipris_tools.kipris_api.foreign.code import count_dict, sort_field_dict
import urllib.parse
from logging import getLogger
logger = getLogger(__name__)

class ForeignPatentFreeSearchAPI(ABSKiprisAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        
        self.api_url = "http://plus.kipris.or.kr/openapi/rest/ForeignPatentAdvencedSearchService/freeSearch"

    def search(self, free:str,
                current_page:int=1,
                sort_field:str='AD',
                sort_state:bool=True,
                collection_values:str='US')->pd.DataFrame:
        """_summary_

        Args:
            free (str): 자유검색 키워드             
            current_page (int, optional): 페이지 번호. Defaults to 1.
            sort_field (str, optional): 정렬 기준. Defaults to "AD".
                (AD-출원일자, PD-공고일자, GD-등록일자, OPD-공개일자, FD-국제출원일자, FOD-국제공개일자, RD-우선권주장일자)
            sort_state (bool, optional): 내림차순 정렬. Defaults to True. other wise False
            collection_values (str, optional): 검색 대상 국가. Defaults to "US".  
                (미국-US, 유럽-EP, PCT-WO, 일본-JP, 일본영문초록-PJ, 중국-CP, 중국특허영문초록-CN, 대만영문초록-TW, 러시아-RU, 콜롬비아-CO, 스웨덴-SE, 스페인-ES, 이스라엘-IL)
                ※다중 국가 선택 불가          

        Returns:
            pd.DataFrame: _description_
        """
        if collection_values not in count_dict :
            raise ValueError(f"collection_values must be in {count_dict.keys()}")
        if sort_field not in sort_field_dict :
            raise ValueError(f"sort_field must be in {sort_field_dict.keys()}")
        logger.info(f"search word: {free}")
        free = urllib.parse.quote(free)
        response = self.common_call(api_url=self.api_url,
                                  api_key_field="accessKey",
                                  free=free,
                                  current_page=str(current_page),
                                  sort_field=str(sort_field),
                                  sort_state="true" if sort_state else "false",
                                  collection_values=str(collection_values))
        patents = get_nested_key_value(response, "response.body.items.searchResult")
        if patents is None:
            logger.info("patents is None")
            return pd.DataFrame()
        if isinstance(patents, t.Dict):
            patents = [patents]
        return pd.DataFrame(patents)