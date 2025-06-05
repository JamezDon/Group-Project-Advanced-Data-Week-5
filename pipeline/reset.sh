# Shell script to connect to and reset the database using MS SQL Server CLI.
source .env
sqlcmd -S $DB_HOST -U $DB_USER -P $DB_PASSWORD -d $DB_NAME -i schema.sql