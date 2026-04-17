from pydantic import BaseModel, Field
from typing import List

class ArticleEvaluationResult(BaseModel):
    is_valid: str = Field(description="Valid if the article passes all checks, Not Valid if it fails.")
    suggestions: str = Field(description="Suggestions to improve the article.")
