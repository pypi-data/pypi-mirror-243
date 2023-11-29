import openai
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.memory import ConversationBufferMemory

from mmon.config import load_config
from mmon.langchain_callback import LangChainCallbackHandler
from mmon.tools import load_tools


def get_llm():
    config = load_config()
    common_openai_params = {
        "temperature": 0,
        "api_type": config.llm.openai_api_type,
        "api_key": config.llm.openai_api_key,
        "api_version": config.llm.openai_api_version,
        "base_url": config.llm.openai_api_base,
    }
    if len(config.llm.deployment_id) > 0:
        llm = ChatOpenAI(deployment_id=config.llm.deployment_id, **common_openai_params)
    else:
        llm = ChatOpenAI(model=config.llm.model, **common_openai_params)
    return llm


class Engine:
    def __init__(self, llm=None, verbose_level=0):
        if llm is None:
            llm = get_llm()
        tools = load_tools(llm, verbose_level)
        if verbose_level >= 3:
            openai.log = "debug"

        self.executor = create_conversational_retrieval_agent(
            llm=llm,
            tools=tools,
            max_token_limit=2000,
            remember_intermediate_steps=False,
            verbose=verbose_level > 1,
        )
        self.callbacks = [LangChainCallbackHandler()]

    def run(self, prompt: str) -> str:
        response = self.executor.run(prompt, callbacks=self.callbacks)
        return response

    def stream(self, prompt: str) -> str:
        response = self.executor.stream(prompt)
        return response
