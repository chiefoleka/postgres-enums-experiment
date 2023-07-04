# Experiment playing with DB architecture choices

I decided to run this experiment out of curiostiy and in line with principles of true science 🤣. I mean, I'm trained as a computer scientist, so what other better way to validated a hypothesis than to prove it?

## The problem
I was discussing what looked like a simple problem - storing demographic data for a user on Postgres, and it presented interesting things to consider. We want to store things like marital status, parental status, family size and more that all have defined values or defined ranges. At first thought, you will say *"Just store it as an `ENUM` on the table"*, and you will not have said anything different from what the 5+ people I asked the same question said.

You see, I originally didn't even consider `ENUMs` for this because I have PTSD from working with them years ago (most PHP developers who have used any of the popular frameworks can understand). If you google *"Avoid ENUMs"*, you will get a lot of results with justifiable reasons for this. So, whch camp truly show we follow? Use `ENUMs` or create multiple small `table`s that hold that information?

## The expectation from the system
The system we want to design is expected to be fast, stable, scalable and available. It should also be efficent with resources and avoid bloats as much as possible. Yes, resources are cheap today, but it doesn't mean we should waste them 😄.

If we want to make requests to our DB fast (say milliseconds), we typically want to index the DB, especially if we have very large data (think 10s of millions of rows across multiple tables at the minimum). But indexes are not a silver bullet as they can get bloated really quickly. We do not want that either, even if it does some magic to make things faster.

> I've had an experience where we had many large database tables (growing at 10+GB a day) and one of our tables was at about 200GB. The indexes on the table were somewhere around 160GB and it was so crazy 🤯. This kept growing everyday and we had to prioritize optimization of the table / indexes.

We also want to filter our records based on any combination of the `ENUMs` (at least that is what the requirements say). It's impractical to index all the `ENUM` columns and hope that solves our issues. Even if it did, is that the best way to go? Is it efficient, stable, scalable, reliable?

This is where an experiment can help us answer these questions.

If you want to learn some technical details about how Postgres stores `ENUMs` and `tables` 👉🏽 [Click here](./technical-details.md).

## Run
First, bring up the databases
```bash
docker compose up test-tables-db test-ints-db test-enums-db -d
docker compose run --rm -e MIGRATE=True test-tables
```