from os import environ

from langchain.agents import Tool, initialize_agent
from langchain.chains import LLMMathChain
from langchain.utilities import BingSearchAPIWrapper
from loguru import logger

from mmon.config import load_config


def load_tools(llm, verbose_level=0):
    config = load_config()
    tools = [
        Tool(
            name="Calculator",
            func=LLMMathChain.from_llm(llm=llm, verbose=verbose_level >= 3).run,
            description="useful for when you need to answer questions about math",
        ),
    ]

    if len(config.bing.key) > 0:
        search = BingSearchAPIWrapper(
            bing_subscription_key=config.bing.key, bing_search_url=config.bing.url
        )
        tools.append(
            Tool(
                name="BingSearch",
                description="Search Bing for recent results.",
                func=search.run,
            )
        )

    logger.info("Loaded tools: {}", [tool.name for tool in tools])
    return tools
