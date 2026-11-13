from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, update
from models.news import Category, News

async def get_categories(db: AsyncSession,skip: int = 0, limit: int=100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_list(db: AsyncSession,catagory_id: int, skip: int = 0, limit: int=10):
    # 查询指定分类下的所有新闻
    stmt = select(News).where(News.category_id == catagory_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_count(db: AsyncSession, catagory_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == catagory_id)
    result = await db.execute(stmt)
    return result.scalar_one() # 仅单个结果

async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_view(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    await db.execute(stmt)
    await db.commit()

async def get_related_news(db: AsyncSession, news_id: int, category_id: int , limit: int = 5):
    stmt = select(News).where(
        News.category_id == category_id, 
        News.id != news_id
    ).order_by(
        News.views.desc(), # 按浏览量降序排列
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()
    related_news = result.scalars().all()

    # 选择新闻核心数据展示
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views
    } for news_detail in related_news]
