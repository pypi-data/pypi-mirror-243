from functools import cache
from os import environ, path

from loguru import logger
from pydantic import BaseModel, Field


class GerneralConfig(BaseModel):
    streaming: bool = Field(default_factory=lambda: False)
    use_readline: bool = Field(default_factory=lambda: True)
    color: bool = Field(default_factory=lambda: True)


class LLMConfig(BaseModel):
    openai_api_type: str
    openai_api_base: str
    openai_api_key: str
    openai_api_version: str
    deployment_id: str
    model: str


class BingConfig(BaseModel):
    key: str
    url: str


class AppConfig(BaseModel):
    general: GerneralConfig
    llm: LLMConfig
    bing: BingConfig


def generate_config(rcfile):
    logger.warning("Generating config file.")
    config = AppConfig(
        general=GerneralConfig(),
        llm=LLMConfig(
            openai_api_type=environ.get("OPENAI_API_TYPE", "openai"),
            openai_api_base=environ.get("OPENAI_API_BASE", "https://api.openai.com"),
            openai_api_key=environ.get("OPENAI_API_KEY", ""),
            openai_api_version=environ.get("OPENAI_API_VERSION", "2023-07-01-preview"),
            deployment_id=environ.get(
                "MMON_DEPLOYMENT", environ.get("OPENAI_DEPLOYMENT", "")
            ),
            model=environ.get("OPENAI_MODEL", "gpt-3.5-turbo"),
        ),
        bing=BingConfig(
            key=environ.get("BING_SUBSCRIPTION_KEY", ""),
            url=environ.get(
                "BING_SEARCH_ENDPOINT", "https://api.bing.microsoft.com/v7.0/search"
            ),
        ),
    )
    with open(rcfile, "w") as fd:
        print(config.model_dump_json(indent=4), file=fd)


@cache
def load_config(gen_cfg=False):
    rcfile = path.join(path.expanduser("~"), ".mmon_cfg.json")
    if not path.exists(rcfile) or gen_cfg:
        generate_config(rcfile)

    with open(rcfile, "r") as fd:
        content = fd.read().strip()
        config = AppConfig.model_validate_json(content)
    new_content = config.model_dump_json(indent=4)
    if content != new_content:
        logger.warning("Updating config file.")
        with open(rcfile, "w") as fd:
            print(new_content, file=fd)

    return config
