from sqlalchemy.future import select
from .models import Event
import logging as log
from sqlalchemy.exc import SQLAlchemyError


async def get_events(session, start=None, end=None):
    """Fetch events with optional filtering by start and end time."""
    log.info(f"Fetching events with filters - start: {start}, end: {end}")
    
    query = select(Event)
    if start:
        query = query.where(Event.start_time >= start)
    if end:
        query = query.where(Event.end_time <= end)

    try:
        result = await session.execute(query)
        events = result.scalars().all()
        log.info(f"Successfully fetched {len(events)} events")
        return events
    except SQLAlchemyError as e:
        log.error(f"Database error while fetching events: {e}")
        raise
    except Exception as e:
        log.error(f"Unexpected error while fetching events: {e}")
        raise

async def add_event(session, event: Event):
    """Add a new event to the database."""
    log.info(f"Adding new event: {event.event_name} (ID: {event.id})")
    
    try:
        session.add(event)
        await session.commit()
        await session.refresh(event)  # Refresh to get any DB-generated values
        log.info(f"Event '{event.event_name}' added successfully")
        return event
    except SQLAlchemyError as e:
        log.error(f"Database error while adding event '{event.event_name}': {e}")
        await session.rollback()
        raise
    except Exception as e:
        log.error(f"Unexpected error while adding event '{event.event_name}': {e}")
        await session.rollback()
        raise
