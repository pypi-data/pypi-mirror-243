from locale import currency
from math import e
from re import T, escape

from numpy import cross
from .spotON_Areas import Currency, spotON_Area,Area_details
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, Dict,Any

from typing import List
from .countries import *
from .bidding_zones import bidding_zones
from ...data_helpers import get_today_midnight,add_day_to_timestamp

from .customBaseModel import CustomBaseModel

from pydantic import Field, root_validator,validate_model




class Market(CustomBaseModel):
    area: Area_details
    country: Country
    alias: Optional[str] = None
    cities: str = Field(default="")
    name: str = Field(default= "",init = False)

    @root_validator(pre=True)
    def set_codes(cls, values):
        country = values.get('country')
        if country and 'country_name' in country:
            values["name"] = country['country_name']
        return values
    
    @root_validator(pre=True)
    def set_name(cls, values):
        country :Country= values.get('country')
        area = values.get('area')
        if country and area:
            values["name"] = f"{country.emoji} {country.country_name} {area.name}"
        return values
    
    def get_start_end_hours_in_UTC(self) -> tuple[pd.Timestamp,pd.Timestamp]:
        starthour_local_tz = get_today_midnight(self.area.tz)
        endhour_local_tz= add_day_to_timestamp(starthour_local_tz)

        #convert to UTC
        starthour_utc = starthour_local_tz.tz_convert('UTC')
        endhour_utc = endhour_local_tz.tz_convert('UTC')
        endhour_utc = endhour_utc - pd.Timedelta(hours=1)
    
        return starthour_utc,endhour_utc

class MarketNotFoundError(ValueError):
    pass



class Markets():

    austria = Market(area=spotON_Area.AT.value,country=all_Countries.Austria)
    belgium = Market(area=spotON_Area.BE.value,country=all_Countries.Belgium)
    bulgaria = Market(area=spotON_Area.BG.value,country=all_Countries.Bulgaria)
    croatia = Market(area=spotON_Area.HR.value,country=all_Countries.Croatia)
    czech_republic = Market(area=spotON_Area.CZ.value,country=all_Countries.Czech_republic)
    #denmark = Market(area=spotON_Area.DK.value,country=all_Countries.Denmark)
    estoonia = Market(area=spotON_Area.EE.value,country=all_Countries.Estonia)
    finland = Market(area=spotON_Area.FI.value,country=all_Countries.Finland)
    france = Market(area=spotON_Area.FR.value,country=all_Countries.France)
    germany = Market(area=spotON_Area.DE_LU.value,country=all_Countries.Germany,alias="DE_LU")
    greece = Market(area=spotON_Area.GR.value,country=all_Countries.Greece)
    hungary = Market(area=spotON_Area.HU.value,country=all_Countries.Hungary)
    #ireland = Market(area=spotON_Area.IE_SEM.value,country=all_Countries.Ireland)
    #italy = Market(area=spotON_Area.IT.value,country=all_Countries.Italy)
    latvia = Market(area=spotON_Area.LV.value,country=all_Countries.Latvia)
    lithuania = Market(area=spotON_Area.LT.value,country=all_Countries.Lithuania)
    luxembourg = Market(area=spotON_Area.DE_LU.value,country=all_Countries.Luxembourg,alias="DE_LU")
    netherlands = Market(area=spotON_Area.NL.value,country=all_Countries.Netherlands)
    poland = Market(area=spotON_Area.PL.value,country=all_Countries.Poland)
    portugal = Market(area=spotON_Area.PT.value,country=all_Countries.Portugal)
    romania = Market(area=spotON_Area.RO.value,country=all_Countries.Romania)
    slovakia = Market(area=spotON_Area.SK.value,country=all_Countries.Slovakia)
    slovenia = Market(area=spotON_Area.SI.value,country=all_Countries.Slovenia)
    spain = Market(area=spotON_Area.ES.value,country=all_Countries.Spain)
    #sweden1 = Market(area=spotON_Area.SE_1.value,country=all_Countries.Sweden)
    #luxembourg = Market(Area.DE_LU,Luxembourg)

    #sweden2 = Market(Area.SE_2,Sweden)
    #sweden3 = Market(Area.SE_3,Sweden)
    #sweden4 = Market(Area.SE_4,Sweden)
    markets_List = [value for key, value in vars().items() if isinstance(value, Market)]
    def __init__(self,debug = True):

        if debug:
            self.markets_List = [self.austria,self.germany]        

    @staticmethod
    def get_market_by_name(name: str) -> Optional[Market]:
        for market in Markets.markets_List:
            if market.name == name: # type: ignore
                return market

        raise MarketNotFoundError

    @staticmethod
    def get_market_by_code(area_code: str) -> Optional[Market]:
        for market in Markets.markets_List:
            #print (f"Try to find {area_code =} in {market}")
            if market.country.country_code == area_code or market.alias == area_code:
                return market

        raise MarketNotFoundError





