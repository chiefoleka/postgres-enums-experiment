from faker import Faker
from shared.demographics import Demographics
from shared.database import Database
import shared.migrations as base_migrations

faker = Faker()
db = Database()
demographics = Demographics()


def create_model_table():
    demos_sql = []
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
        demos_sql.append(
            f"""
            CREATE TABLE IF NOT EXISTS {name} (
                id SMALLINT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
                name VARCHAR(100),
                PRIMARY KEY (id)
            )
        """
        )

        values = demographics.get_values(name)
        quoted_values = [f"('{x}')" for x in values]
        demos_sql.append(
            f"""
            INSERT INTO {name} (name) VALUES
            {','.join(quoted_values)}
        """
        )

        table_sql.append(f"{name}_id SMALLINT REFERENCES {name}(id)")

    sql = f"""
        CREATE TABLE IF NOT EXISTS profiles (
            {','.join(table_sql)}
        )
    """
    db.query("; ".join(demos_sql))
    db.query(sql)


def seed_model(record_size: int):
    profiles = []

    bio_columns = ["first_name", "last_name", "email", "phone", "date_of_birth"]
    location_colums = ["country_id", "state_id", "city_id"]
    demo_columns = []

    join_sql = [
        """
        (
            SELECT 
                id as city_id,
                country_id,
                state_id 
            FROM cities 
            ORDER BY RANDOM()
            LIMIT 1
        ) cities_t
        """
    ]
    for name in demographics.get_names_only():
        demo_key = f"{name}_id"
        join_sql.append(
            f"""
            (SELECT id as {demo_key} FROM {name} ORDER BY RANDOM() LIMIT 1) as {name}_t
        """
        )
        demo_columns.append(demo_key)

    columns = bio_columns + location_colums + demo_columns
    for _ in range(record_size):
        profile_data = [
            faker.first_name(),
            faker.last_name(),
            faker.email(),
            faker.phone_number(),
            faker.date_of_birth(),
        ]
        select_sql = [f"'{x}'" for x in profile_data] + location_colums + demo_columns

        profiles.append(
            f"""
            INSERT INTO profiles ({','.join(columns)})
            SELECT {','.join(select_sql)}
            FROM {','.join(join_sql)}
        """
        )

    chunk_size = 1000
    for i in range(0, len(profiles), chunk_size):
        chunk = profiles[i : i + chunk_size]

        db.query("; ".join(chunk))


def run(record_size: int):
    base_migrations.migrate()
    base_migrations.seed()
    create_model_table()
    seed_model(record_size)
