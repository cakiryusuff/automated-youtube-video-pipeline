from pydantic_ai import Agent
import asyncio
from src.logger import get_logger

logger = get_logger(__name__)

editor_agent = Agent(
    "gpt-4o-mini",
    output_type=str,
    system_prompt=(
        "You are a professional editor."
        "Make the news explanatory and concise:"
        "remove unnecessary details, summarize the article, and produce a clear, fluent news piece without unnecessary elaboration."
    )
)

check_agent = Agent(
    "gpt-4o-mini",
    output_type=bool,
    system_prompt=(
        "You are a professional editor."
        "Determine whether the text has news value. Return only True if it does, or False if it does not."
    )
)

async def text_editor(news_list: list[str]) -> str:
    for text in news_list:
        is_news = await check_agent.run(text)
        if is_news.output:
            edited_text = await editor_agent.run(text)
            return edited_text.output

if __name__ == "__main__":
    text = ["Bugün hava çok güzel. Market alışverişi yapmam lazım ve biraz yürüyüşe çıkacağım.","""
    Hatırlanacağı üzere geçtiğimiz yıl Mehta, Google’ın arama pazarında yasa dışı yollarla tekel oluşturduğuna karar vermişti. 
    Bunun üzerine Adalet Bakanlığı, şirketin Chrome’u elden çıkarmasını talep etmişti.
    Ancak yargıç, 230 sayfalık kararında bu talebi “aşırıya kaçmak” olarak niteledi.
    “Google'ın Chrome'u satması gerekmeyecek” diyen Mehta, Android için de aynı yaklaşımı sergiledi.
    Bilindiği üzere Perplexity, Chrome için 34 milyar doları aşan bir teklifte bulunmuştu. - Kaynak: donanimhaber.com"""]

    asyncio.run(text_editor(text))
