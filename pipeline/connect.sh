# Script for connecting to the RDS SQL Server Database via the command-line.
source .env
sqlcmd -S $DB_HOST -U $DB_USER -P $DB_PASSWORD -d $DB_NAME