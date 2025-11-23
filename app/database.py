from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import config
from app.tools.redis_client import RedisClient

engine = create_async_engine(config.mysql_url, pool_size=100,pool_pre_ping=True,pool_recycle=1800, max_overflow=20,echo=False,isolation_level="READ COMMITTED")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False,autoflush=False,autocommit=False)

async def get_db():
    async with AsyncSessionLocal(autobegin=False) as session:
        yield session

Base = declarative_base()

from redis.asyncio import Redis 
redisClient = RedisClient(host=config.REDIS_HOST, port=config.REDIS_PORT,password=config.REDIS_PASSWORD,db=config.REDIS_DB)
def get_redis_client()->Redis:
    return redisClient.client