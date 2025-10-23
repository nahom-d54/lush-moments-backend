from pydantic import BaseModel


class TranslationBase(BaseModel):
    content_type: str
    object_id: int
    language_code: str
    field_name: str
    translated_text: str


class TranslationCreate(TranslationBase):
    pass


class Translation(TranslationBase):
    id: int

    class Config:
        from_attributes = True