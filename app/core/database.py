import logging
from supabase import create_client, Client
from app.core.config import settings

logger = logging.getLogger(__name__)

supabase: Client | None = None


def get_supabase() -> Client:
    """Get the Supabase client singleton"""
    global supabase
    if supabase is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_KEY must be set in .env"
            )
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        logger.info("Supabase client initialized")
    return supabase


async def init_db() -> None:
    """Initialize database - verify Supabase connection"""
    client = get_supabase()
    try:
        client.table("users").select("id", count="exact").limit(1).execute()
        logger.info("Supabase connection verified successfully")
    except Exception as e:
        logger.error("Supabase connection failed: %s", e)
        raise


async def close_db() -> None:
    """Close Supabase client (no-op, httpx sessions are managed internally)"""
    global supabase
    supabase = None
    logger.info("Supabase client closed")
