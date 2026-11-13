from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news

# 创建实例
# prefix路由前缀（API接口规范文档）
# tags 分组标签
router = APIRouter(prefix="/api/news", tags =["news"])


# 接口实现流程
# 1. 模块化路由
# 2. 定义模型类 → 数据库表
# 3. 在 crud 文件夹里创建文件，封装操作数据库的方法
# 4. 在路由处理函数里调用 crud 封装好的方法，响应结果

@router.get("/categories")
async def get_categories(skip: int=0, limit: int=100, db: AsyncSession = Depends(get_db)):
    catagories = await news.get_categories(db, skip, limit)
    return {
        "code":200,
        "message":"获取新闻分类成功",
        "data":catagories
    }


@router.get("/list")
async def get_news_list(
    category_id:int = Query(..., alias="categoryId"),
    page: int = 1,
    page_size:int = Query(10, alias="pageSize", le=100),
    db: AsyncSession = Depends(get_db)
):
    # 处理分页规则 → 查询新闻列表 → 计算总量 → 计算是否还有更多
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id) 
    hasMore = offset + len(news_list) < total

    return {
        "code":200,
        "message":"获取新闻列表",
        "data":{
            "list": news_list,
            "total": total,
            "hasMore":hasMore
        }
    } 

@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    # 1.获取新闻详情  2.每次浏览后使浏览量+1 3. 相关新闻

    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    await news.increase_news_view(db, news_detail.id)

    related_news = await news.get_related_news(db, news_detail.id, news_detail.category_id)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    }