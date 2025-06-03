# connecting to and clearing the database
source .env
sqlcmd -S $DB_HOST -U $DB_USER -P $DB_PASSWORD -d $DB_NAME -i schema.sql