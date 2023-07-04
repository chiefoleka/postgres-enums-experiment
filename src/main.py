import enums.migrations as enums_migrations
import ints.migrations as ints_migrations
import tables.migrations as tables_migrations

from decouple import config
from enums.model import Model as EnumsModel
from ints.model import Model as IntsModel
from tables.model import Model as TablesModel

stage = config("STAGE", None)
migrate = config("MIGRATE", False, cast=bool)
record_size = config("RECORD_SIZE", 1000, cast=int)
chunk_size = config("CHUNK_SIZE", 1000, cast=int)

if stage == "enums":
    migrations = enums_migrations
    model = EnumsModel()
elif stage == "ints":
    migrations = ints_migrations
    model = IntsModel()
elif stage == "tables":
    migrations = tables_migrations
    model = TablesModel()
else:
    raise ValueError("No stage defined")

if migrate:
    migrations.run(record_size, chunk_size)

# Define what to run
