import random
import math
from faker import Faker
from shared.demographics import Demographics
from shared.database import Database
import shared.migrations as base_migrations

faker = Faker()
db = Database()
demographics = Demographics()


def create_model_table():
    table_sql = [
        "id SERIAL PRIMARY KEY",
        "first_name VARCHAR(100)",
        "last_name VARCHAR(100)",
        "email VARCHAR(255)",
        "phone VARCHAR(100)",
        "date_of_birth DATE",
        "country_id INT REFERENCES countries(id)",
        "state_id INT REFERENCES states(id)",
        "city_id INT REFERENCES cities(id)",
    ]

    for name in demographics.get_names_only():
        table_sql.append(f"{name} SMALLINT")

    sql = f"""
        CREATE TABLE IF NOT EXISTS profiles (
            {','.join(table_sql)}
        )
    """

    db.query(sql)


def seed_model(record_size: int, chunk_size: int):
    cities = db.select_many("SELECT * FROM cities")

    batch_size = math.ceil(record_size / chunk_size)

    for i in range(0, batch_size):
        profiles = []
        for _ in range(chunk_size):
            city = random.choice(cities)
            profile = {
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": faker.email(),
                "phone": faker.phone_number(),
                "date_of_birth": faker.date_of_birth(),
                "country_id": city["country_id"],
                "state_id": city["state_id"],
                "city_id": city["id"],
            }

            for key in demographics.get_names_only():
                profile[key] = demographics.get_value_translation(
                    key, random.choice(demographics.get_values(key))
                )

            profiles.append(profile)

        print(f"Done generating profiles batch {i + 1} of {batch_size}")

        columns = tuple(profiles[0].keys())
        db.insert_batch(
            table="profiles",
            columns=columns,
            data=list(map(lambda x: list(x.values()), profiles)),
        )

        print(f"Done inserting batch {i + 1} of {batch_size}")


def run(record_size: int, chunk_size=100000):
    base_migrations.migrate()
    base_migrations.seed()
    create_model_table()
    seed_model(record_size, chunk_size)
