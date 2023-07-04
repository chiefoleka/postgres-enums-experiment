# Some technical notes

It is import to understand how Postgres handles `tables` and `ENUMs` in the DB, as that would help us tick boxes on which solution will meet our needs the quickest.

## Tables
Postgres stores tables as a collection of flat files (called Data files) on the disk. It stores the table definition in the `system catalog tables` maintained by Postgres. The flat files are usually around 8KB in size and there can be many of them as your table grows. Within the flat file, the actual data is stored something called Pages which then hold multiple rows stored as tuples. 

If we had the following table:
```sql
CREATE TYPE enum_gender AS ENUM ('Male', 'Female', 'Other');
CREATE TYPE enum_ethnicity AS ENUM ('Caucasian', 'African American', 'Asian', 'Hispanic', 'Other');
CREATE TYPE enum_nationality AS ENUM ('American', 'British', 'Canadian', 'Australian', 'Other');
CREATE TYPE enum_marital_status AS ENUM ('Single', 'Married', 'Divorced', 'Widowed', 'Other');

CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    date_of_birth DATE,
    gender enum_gender,
    ethnicity enum_ethnicity,
    nationality enum_nationality,
    marital_status marital_status
);
```
So, it can look something like this:
```bash
# Table structure

├── /table_a
│   ├── table_a.0100.dat
│   ├── table_a.0101.dat
│   ├── table_a.0110.dat
│   ├── table_a.0111.dat
├── /table_b
│   ├── table_b.0100.dat
│   ├── table_b.0101.dat
│   ├── table_b.0110.dat
├── /table_c
└── /table_d
```

```bash
# Data file structure (table_a.0100.dat)
------------------------------------------------------------------------
| Page 1:                                                              |
------------------------------------------------------------------------
| Tuple 1:                                                              |
------------------------------------------------------------------------
| Tuple Header | Null Bitmap | id  | fullname    | date_of_birth | ... |
------------------------------------------------------------------------
| Fixed-Size   | Null Bitmap | 1   | John Smith  | 1985-03-12    | ... |
| Header       | 110000      |     |             |               |     |
------------------------------------------------------------------------
| Tuple 2:                                                              |
------------------------------------------------------------------------
| Tuple Header | Null Bitmap | id  | fullname       | date_of_birth | ... |
------------------------------------------------------------------------
| Fixed-Size   | Null Bitmap | 2   | Jane Doe       | 1990-09-25    | ... |
| Header       |             |     |                |               |     |
------------------------------------------------------------------------
| Tuple 3:                                                              |
------------------------------------------------------------------------
| Tuple Header | Null Bitmap | id  | fullname       | date_of_birth | ... |
------------------------------------------------------------------------
| Fixed-Size   | Null Bitmap | 3   | David Johnson  | 1987-06-10    | ... |
| Header       |             |     |                |               |     |
------------------------------------------------------------------------
| Tuple 4:                                                              |
------------------------------------------------------------------------
| Tuple Header | Null Bitmap | id  | fullname       | date_of_birth | ... |
------------------------------------------------------------------------
| Fixed-Size   | Null Bitmap | 4   | Sarah Wilson   | 1995-01-18    | ... |
| Header       |             |     |                |               |     |
------------------------------------------------------------------------

------------------------------------------------------------------------
| Page 2:                                                              |
------------------------------------------------------------------------
| Tuple 5:                                                              |
------------------------------------------------------------------------
| Tuple Header | Null Bitmap | id  | fullname       | date_of_birth | ... |
------------------------------------------------------------------------
| Fixed-Size   | Null Bitmap | 5   | Michael Brown  | 1987-06-10    | ... |
| Header       | 010000      |     |                |               |     |
------------------------------------------------------------------------
| Tuple 6:                                                              |
------------------------------------------------------------------------
| Tuple Header | Null Bitmap | id  | fullname       | date_of_birth | ... |
------------------------------------------------------------------------
| Fixed-Size   | Null Bitmap | 6   | Laura Davis    | 1994-04-05    | ... |
| Header       |             |     |                |               |     |
------------------------------------------------------------------------
| Tuple 7:                                                              |
------------------------------------------------------------------------
| Tuple Header | Null Bitmap | id  | fullname          | date_of_birth | ... |
------------------------------------------------------------------------
| Fixed-Size   | Null Bitmap | 7   | Samantha Johnson  | 1992-11-15    | ... |
| Header       | 00100       |     |                   |               |     |
------------------------------------------------------------------------
| Tuple 8:                                                              |
------------------------------------------------------------------------
| Tuple Header | Null Bitmap | id  | fullname       | date_of_birth | ... |
------------------------------------------------------------------------
| Fixed-Size   | Null Bitmap | 8   | James Anderson | 1989-08-27    | ... |
| Header       |             |     |                |               |     |
------------------------------------------------------------------------

...
```

... in progress
