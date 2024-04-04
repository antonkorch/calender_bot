# Description: This file contains the functions that interact with the database.
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from models import Cal


def add_event(engine, rdow, edate, etime, etext):
    Session = sessionmaker(bind=engine)
    session = Session()

    event = Cal(rdow=rdow, edate=edate, etime=etime, etext=etext)
    session.add(event)
    session.commit()


def list_events_from(engine, startdate, step=7):
    conn = engine.connect()
    command = text("""
    SELECT 
        CASE WHEN rdow IS NOT NULL
        THEN date("now", "weekday " || rdow)
        ELSE edate
        END AS cdate,
        etime, etext 
    FROM cal
    WHERE cdate BETWEEN :startdate AND date(:startdate, :step || " days")
    ORDER BY cdate, etime;
    """)
    result = conn.execute(command, {"startdate" : startdate, "step" : step})  
    return result.all()
