# ks-tha
### Warning
Push update method requires Google Drive API and a domain name (for Let's Encrypt SSL).
### How to run
0. Turn on Google Sheets
1. Create .env file in project root
2. Add credentials.json file for Google API service account with read priveleges (to project root).
3. Run `docker compose up`
### .env example:
```
# spreadsheet name in google sheets file
sheet_name=Лист1
# spreadsheet id as extracted from link
spreadsheet_id=1oy13To3eyYlNDEs49TekBWFBKLycmoq0-wAjl2kEOdY
# pretty much any string, used to identify notification channels with "push" method
channel_id=bc127763-1ed4-4796-b7ea-c5ce9574fa93
# "push" for Google Drive notifications, "pull" for polling every 2 seconds
update_mode=pull
hostname=
POSTGRES_PASSWORD=pgpass
POSTGRES_USER=pguser
POSTGRES_DB=pgdb
```
