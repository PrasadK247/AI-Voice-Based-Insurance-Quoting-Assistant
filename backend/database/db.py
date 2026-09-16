"""
UC189 - Database Connection and Session Management
Supports PostgreSQL with seamless SQLite local fallback.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import get_settings
from database.models import Base, Policy
from utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)

# Normalize database URL for async drivers
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
elif database_url.startswith("sqlite:///") and not database_url.startswith("sqlite+aiosqlite:///"):
    database_url = database_url.replace("sqlite:///", "sqlite+aiosqlite:///")

try:
    engine = create_async_engine(
        database_url,
        echo=False,
        future=True,
    )
except Exception as e:
    logger.warning(f"Failed to initialize engine with {database_url}: {e}. Falling back to SQLite.")
    database_url = "sqlite+aiosqlite:///./insurance_advisor.db"
    engine = create_async_engine(database_url, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables and seed sample policies."""
    global engine, AsyncSessionLocal

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(f"Database connected and tables initialized using: {engine.url.drivername}")
    except Exception as e:
        logger.warning(f"Primary database connection failed ({e}). Falling back to SQLite.")
        database_url_fallback = "sqlite+aiosqlite:///./insurance_advisor.db"
        engine = create_async_engine(database_url_fallback, echo=False, future=True)
        AsyncSessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("SQLite database fallback successfully initialized.")

    # Seed sample policies if empty
    async with AsyncSessionLocal() as session:
        try:
            from sqlalchemy import select
            result = await session.execute(select(Policy))
            existing = result.scalars().first()
            if not existing:
                await _seed_policies(session)
        except Exception as seed_err:
            logger.warning(f"Policy seeding check: {seed_err}")


async def _seed_policies(session: AsyncSession):
    """Seed predefined sample policies."""
    sample_policies = [
        Policy(
            policy_id="pol_001",
            policy_name="Premium Health Shield",
            provider="HealthGuard Insurance",
            tier="premium",
            insurance_type="health",
            base_premium=450.0,
            coverage_amount=500000.0,
            deductible=500.0,
            key_benefits=[
                "Comprehensive hospitalization",
                "Dental & vision included",
                "Global emergency coverage",
                "Zero deductible option",
            ],
            limitations=["12-month waiting period for pre-existing conditions"],
        ),
        Policy(
            policy_id="pol_002",
            policy_name="Essential Health Plan",
            provider="SafeLife Insurance",
            tier="standard",
            insurance_type="health",
            base_premium=250.0,
            coverage_amount=300000.0,
            deductible=1000.0,
            key_benefits=[
                "In-patient coverage",
                "Emergency services",
                "Prescription drug coverage",
                "Preventive care screenings",
            ],
            limitations=["No dental", "No vision", "Network restricted"],
        ),
        Policy(
            policy_id="pol_003",
            policy_name="Family Care Plus",
            provider="FamilyFirst Insurance",
            tier="family",
            insurance_type="health",
            base_premium=380.0,
            coverage_amount=400000.0,
            deductible=750.0,
            key_benefits=[
                "Family floater plan for up to 6 members",
                "Maternity & newborn coverage",
                "Child immunization schedule",
                "Annual wellness checkups",
            ],
            limitations=["Co-pay required for specialist visits"],
        ),
        Policy(
            policy_id="pol_004",
            policy_name="Budget Health Basic",
            provider="ValueInsure",
            tier="basic",
            insurance_type="health",
            base_premium=150.0,
            coverage_amount=150000.0,
            deductible=1500.0,
            key_benefits=[
                "Basic hospitalization",
                "Emergency room access",
                "Generic prescriptions",
            ],
            limitations=[
                "High deductible ($1,500)",
                "Limited doctor network",
                "No dental or vision",
                "Annual caps on surgical benefits",
            ],
        ),
        Policy(
            policy_id="pol_005",
            policy_name="Executive Health Elite",
            provider="EliteShield Insurance",
            tier="elite",
            insurance_type="health",
            base_premium=650.0,
            coverage_amount=1000000.0,
            deductible=0.0,
            key_benefits=[
                "Unlimited hospitalization coverage",
                "Full dental & vision included",
                "Worldwide coverage & air ambulance",
                "Annual executive health screenings",
                "Dedicated concierge doctor",
            ],
            limitations=["Premium pricing"],
        ),
    ]

    for p in sample_policies:
        session.add(p)
    await session.commit()
    logger.info(f"Seeded {len(sample_policies)} standard insurance policies.")
