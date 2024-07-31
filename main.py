from langchain_community.llms import GPT4All

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader

from typing import List

PDF_PATH = "C:\\DESK\\DOCS\\Rechnungen\\50_2302013_22720_20230217_122539.PDF"
MODEL_PATH = "/Users/rlm/Desktop/Code/gpt4all/models/nous-hermes-13b.ggmlv3.q4_0.bin"
loader = PyPDFLoader(PDF_PATH)
pages = loader.load_and_split()

text = " ".join(list(map(lambda page: page.page_content, pages)))


class CVDataExtraction(BaseModel):
    username: str = Field(description="candidate username")
    email: str = Field(description="candidate email")
    profile: str = Field(description="candidate profile description")
    skills: List[str] = Field(description="soft and technical skills")


model = GPT4All(
    model=MODEL_PATH,
    max_tokens=2048,
)

structured_llm = model.with_structured_output(CVDataExtraction)
structured_llm.invoke(text)
