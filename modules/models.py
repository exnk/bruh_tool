from pydantic import BaseModel, Field


class CVEModel(BaseModel):
    details: str = Field(default=None, alias='Details')
    exposure: str = Field(default=None, alias='Exposure')
    tags: str = Field(default=None, alias='Tags')
    download: str = Field(default=None, alias='Download URL')
    comments: str = Field(default=None, alias='Comments')


class CVE(BaseModel):
    cve_name: str = Field(default=None)
    name: str = Field(default=None)
    attributes: CVEModel
    compiled: str = Field(default=None)
    source: str = Field(default=None)
