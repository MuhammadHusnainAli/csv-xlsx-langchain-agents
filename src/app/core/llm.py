from langchain_openai import AzureChatOpenAI
from app.config import settings

llm: AzureChatOpenAI = None


def init_llm() -> None:
    global llm
    llm = AzureChatOpenAI(
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_version=settings.AZURE_OPENAI_CHAT_API_VERSION,
        azure_deployment=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME_4O,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
    )


def get_llm() -> AzureChatOpenAI:
    global llm
    if llm is None:
        init_llm()
    return llm
