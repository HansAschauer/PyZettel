from pydantic import BaseModel

# schema definition for tags

class Tags(BaseModel):
    tags: list[str]
