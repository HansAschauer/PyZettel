import openai
from dataclasses import dataclass, field
import json
from pydantic import BaseModel
from ...cli.plugins import get_llm_factory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
import logging

logger = logging.getLogger(__name__)


@dataclass
class Conversation:
    #base_url: str
    #api_key: str
    #engine: str
    developer_prompt: str = "you are a helpful assistant"
    llm: BaseChatModel = field(init=False)
    messages: list[BaseMessage] = field(init=False, default_factory=list)  
    def __post_init__(self):
        self.llm = get_llm_factory()()
    def ask(self, message: str, **kw_args) -> str:
        self.messages.append(HumanMessage(message))
        response = self.llm.invoke(message, **kw_args)
        self.messages.append(response)
        return response.text()
    
    def ask_json(self, message: str, model: type, **kw_args) -> dict:
        self.messages.append(HumanMessage(message))
        llm = self.llm.with_structured_output(model)
        response = llm.invoke(message, **kw_args)
        assert isinstance(response, BaseModel)
        response_dict = response.model_dump()
        self.messages.append(AIMessage([response_dict]))
        return response_dict

@dataclass
class Conversation_old:
    base_url: str
    api_key: str
    engine: str
    developer_prompt: str = "you are a helpful assistant"
    messages: list[dict[str, str]] = field(init=False, default_factory=list)
    client: openai.OpenAI | None = None

    def __post_init__(self):
        self.messages = [
            dict(role="system", content=self.developer_prompt),
        ]
        if self.client is None:
            self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def ask(self, message: str, **kw_args) -> str:
        assert self.client is not None
        self.messages.append(dict(role="user", content=message)) 
        if self.engine is not None:
            kw_args["model"] = self.engine
        response = self.client.chat.completions.create( 
            messages=self.messages,         # type: ignore
            **kw_args
        )                                   # type: ignore
        result = str(response.choices[0].message.content)
        self.messages.append(dict(role="assistant", content=result))
        return result
    
    def ask_json(self, message: str, model: type, **kw_args) -> dict:
        assert self.client is not None
        self.messages.append(dict(role="user", content=message)) 
        if self.engine is not None:
            kw_args["model"] = self.engine
        response = self.client.beta.chat.completions.parse( 
            messages=self.messages,         # type: ignore
            #tool_choice="auto",
            response_format=model,
            **kw_args
        )                                   # type: ignore
        result = str(response.choices[0].message.content)
        self.messages.append( {"role": "assistant", "content": response.model_dump_json()})
        return json.loads(result)
    