"""
Methods to execute SQL scripts in order. This is useful for database migrations.
"""
import os

import peewee

from crawler.models.base import BaseModel, DATABASE as db
from crawler.utils.log import get_logger

LOG = get_logger(__name__)

# SQL scripts directory path
SCRIPTS_DIRECTORY = 'scripts'


# Create a model to represent the migration table
class Migration(BaseModel):
    """
    Model to represent the migration table.
    """
    name = peewee.CharField(unique=True)


def main():
    """
    Executes SQL scripts in order. This is useful for database migrations.
    """
    # Sort the SQL files based on their filename
    sql_files = sorted([f for f in os.listdir(SCRIPTS_DIRECTORY) if f.endswith('.sql')])

    db.create_tables([Migration])
    # Execute each SQL script in order
    for sql_file in sql_files:
        LOG.info(f'Executing migration: {sql_file}')
        with open(os.path.join(SCRIPTS_DIRECTORY, sql_file), 'r', encoding='utf-8') as file:
            script = file.read()
            migration_name = os.path.splitext(sql_file)[0]

            # Check if the migration has already been executed
            if Migration.select().where(Migration.name == migration_name).exists():
                LOG.info(f'Migration {migration_name} already executed')
                continue

            # Execute the SQL script
            db.execute_sql(script)

            # Add the migration to the migration table
            Migration.create(name=migration_name)

            LOG.info(f'Migration {migration_name} executed successfully')
    # Close the database connection
    db.close()


if __name__ == '__main__':
    main()
