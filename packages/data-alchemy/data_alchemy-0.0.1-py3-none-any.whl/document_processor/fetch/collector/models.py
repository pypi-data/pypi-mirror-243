from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


# class URLmetadata(BaseModel):
#     url: str
#     document_URL: str
#     title: Optional[str] = None
#     description: Optional[str] = None
#     keywords: Optional[str] = None


class CollectorOptions(BaseModel):
    url: str
    max_depth: int = 1
    include_html: bool = False
    file_extensions: List[str] = [".pdf"]
    process_static_pages: bool = True


class CollectorConfiguration(BaseModel):
    options: Optional[CollectorOptions] = Field(default=None)
    options_file: Optional[str] = Field(default=None)

    # check if options or options_file is provided
    @model_validator(mode="after")
    def check_options(self):
        if self.options is None and self.options_file is None:
            raise ValueError("options or options_file must be provided")
        return self
