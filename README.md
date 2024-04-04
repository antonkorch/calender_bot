# Calender bot
Serves the agenda tracking. Needs the ready calender.db SQLite database with following structure:
```
    table name = 'cal'

    id = (Integer, primary_key=True)
    rdow = (Integer)
    rdom = (Integer)
    edate = (String)
    etime = (String)
    etext = (String)
```