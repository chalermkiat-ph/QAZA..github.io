from pydantic.schema import Optional
from pydantic import BaseModel


class PersonalDto(BaseModel):
    name: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    height: Optional[str] = None
    skin_color: Optional[str] = None
    ethnicity: Optional[str] = None
    hair: Optional[str] = None
    profession: Optional[str] = None
    body_type: Optional[str] = None
    lifestyle: Optional[str] = None
    free_text: Optional[str] = None
    profile_picture: Optional[str] = None
