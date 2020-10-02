from typing import Optional, Union

from pydantic import BaseModel


class Attributes(BaseModel):
    is_blacklisted: bool
    blacklist_flag: Optional[str]
    blacklist_reason: Optional[str]
    original_private_id: Optional[str]
    is_potential_spammer: bool
    is_operator: bool
    is_agent: bool
    is_whitelisted: bool
    intellivoid_accounts_verified: bool
    is_official: bool


class LanguagePrediction(BaseModel):
    language: Optional[str]
    probability: Optional[Union[float, int]]


class SpamPrediction(BaseModel):
    ham_prediction: Optional[Union[float, int]]
    spam_prediction: Optional[Union[float, int]]


class User(BaseModel):
    private_telegram_id: str
    entity_type: str
    attributes: Attributes
    language_prediction: LanguagePrediction
    spam_prediction: SpamPrediction
    last_updated: int
