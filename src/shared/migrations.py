import json
from faker import Faker
from shared.database import Database

faker = Faker()
db = Database()
countries = json.load(open("./data/countries.json", "r"))


def create_countries_table():
    sql = """
        CREATE TABLE IF NOT EXISTS countries (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            cca2 CHAR(2) NOT NULL
        )
    """
    db.query(sql)


def create_states_table():
    sql = """
        CREATE TABLE IF NOT EXISTS states (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            country_id INTEGER REFERENCES countries(id)
        )
    """
    db.query(sql)


def create_cities_table():
    sql = """
        CREATE TABLE IF NOT EXISTS cities (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            country_id INTEGER REFERENCES countries(id),
            state_id INTEGER REFERENCES cities(id)
        )
    """
    db.query(sql)


def migrate():
    create_countries_table()
    create_states_table()
    create_cities_table()


# modifies countries dict


def seed_countries():
    values = list(map(lambda x: [x["name"], x["cca2"]], list(countries.values())))

    rows = db.insert_many(table="countries", columns=("name", "cca2"), data=values)

    for row in rows:
        countries[row["cca2"]]["id"] = row["id"]


# modifies countries dict
def seed_states():
    for country in countries.values():
        values = list(map(lambda x: [x, country["id"]], country["states"]))

        rows = db.insert_many(
            table="states", columns=("name", "country_id"), data=values
        )

        states = []
        for row in rows:
            states.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "cities": [faker.city() for _ in range(50)],
                }
            )
        country["states_dict"] = states


# modifies countries dict
def seed_cities():
    values = []

    for country in countries.values():
        for state in country["states_dict"]:
            for city in state["cities"]:
                values.append([city, country["id"], state["id"]])

    db.insert_batch(
        table="cities", columns=("name", "country_id", "state_id"), data=values
    )


def seed():
    seed_countries()
    seed_states()
    seed_cities()
