import asyncio
import json

from src.redis_client import get_redis_client


# Получение новостей
async def get_news():
    try:
        redis_client = await get_redis_client()
        cache_key = 'news'

        if redis_client is not None:
            cached_news = await redis_client.get(cache_key)

            if cached_news:
                return json.loads(cached_news)

        # Имитация задержки при запросе данных
        await asyncio.sleep(2)

        # Данные
        news_array = [
            {'news_id': 1, 'title': 'Рост криптовалют в 2024 году', 'text': 'В этом году криптовалюты показывают невероятный рост, с биткойном и эфириумом, которые достигли новых рекордов. Эксперты предсказывают, что тренд продолжится в ближайшие месяцы.'},
            {'news_id': 2, 'title': 'Инфляция в США: что дальше?', 'text': 'После недавнего роста инфляции в США экономисты обсуждают возможные меры для её контроля. Ожидается, что ФРС примет новые решения, чтобы справиться с экономической нестабильностью.'},
            {'news_id': 3, 'title': 'Финансовые технологии: новые тренды', 'text': 'Технологии финансов продолжают развиваться, и новые стартапы привлекают внимание инвесторов. В этом месяце появились инновационные решения для автоматизации личных финансов.'},
            {'news_id': 4, 'title': 'Рынок недвижимости: как изменится ситуация?', 'text': 'Эксперты прогнозируют изменения на рынке недвижимости в связи с изменением процентных ставок. Это может привести к как росту, так и снижению цен на жилье в разных регионах.'},
            {'news_id': 5, 'title': 'Золото как инвестиционный актив', 'text': 'Золото снова становится популярным среди инвесторов, ищущих безопасные активы в условиях экономической неопределенности. Анализ рынка показывает, что золото сохраняет свою ценность как долгосрочная инвестиция.'}
        ]

        # Создание кэша на 30 секунд
        if redis_client is not None:
            await redis_client.setex(cache_key, 30, json.dumps(news_array))

        return news_array

    except Exception as error:
        raise error