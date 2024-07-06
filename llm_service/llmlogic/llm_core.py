import os
from datetime import date, datetime
from operator import itemgetter
from typing import List, Optional, Type
import logging


from dotenv import load_dotenv

load_dotenv()


from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAI



# create a filehandler logger
log_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(log_dir, "llm_service.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(log_dir)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

def _log(res):
    """Log the input from RabbitMQ and the output from LLM (GPT 4.o)."""
    logger.debug(res)
    return res

class Receipt(BaseModel):
    """Information about a purchase receipt."""

    location: Optional[str] = Field(None, description="The location of the store")
    place: Optional[str] = Field(None, description="The name of the store")
    address: Optional[str] = Field(None, description="The address of the store")
    tax_id: Optional[str] = Field(None, description="The tax ID (CUIT) of the store")
    gross_income: Optional[str] = Field(
        None, description="The gross income (Ing. Brutos) number"
    )
    activity_start_date: Optional[str] = Field(
        None, description="The start date of activities"
    )
    invoice_type: Optional[str] = Field(None, description="The type of invoice")
    invoice_number: Optional[str] = Field(None, description="The number of the invoice")
    item_descriptions: Optional[List[str]] = Field(
        default_factory=list, description="A list of item descriptions"
    )
    subtotal: Optional[str] = Field(None, description="The subtotal amount")
    additional_charge: Optional[str] = Field(None, description="Any additional charges")
    total: Optional[str] = Field(None, description="The total amount")
    payment_method: Optional[str] = Field(None, description="The method of payment")
    cashier: Optional[str] = Field(
        None, description="The cashier who processed the transaction"
    )
    date: Optional[datetime] = Field(
        default_factory=date.today(), description="The date of the receipt"
    )


api_key = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, api_key=api_key)
llm_schema = llm.bind_tools([Receipt])



def _model_ingest(res):
    return res["input"]

def _tool_parser(res):
    return res.tool_calls

def _final_parser(res):
    return res["output"]


chain = (
    {
        "log": RunnableLambda(_log),
        "input": RunnablePassthrough()
    }
    | RunnableLambda(_model_ingest)
    | llm_schema
    | RunnableLambda(_tool_parser)
    | {
        "log": RunnableLambda(_log),
        "output": RunnablePassthrough()
    }
    | RunnableLambda(_final_parser)
)
