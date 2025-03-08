from app.settings import Settings

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

settings = Settings()

engine = create_async_engine(
    url=settings.db_url, future=True, echo=True, pool_pre_ping=True
)

AsyncSessionFactory = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False
)


async def get_db_session():
    async with AsyncSessionFactory() as session:
        yield session
