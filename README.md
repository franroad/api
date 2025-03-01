# API PROJECT

1. Create the virtual environment, ``python3 -m venv venv1``
2. view-->command palet --> python select interpreter select the env we have installed
3. ``source venv1/bin/activate`` // deactivaste // venv1/Scripts/Activate.ps1
    - pip install fastapi[all]// pip install 'fastapi[all]'
4. Instalar FastApi
5. levantar el server ``fastapi dev app/main.py``

# POSTMAN
Used in test section for testing purposes but there are no schema.

Example call:
```json

{
"title":"hello from yakutia" ,
"content":"this is a test",
"published": "true",
"rating": "1"

}
```
# Pydantic
- for validating , for defining an schema that the user must accomplish. Thanks to Pydantic we make sure that the field ``rating`` for example, is an integer.


# NOTES
- Iterating to get index and content

```python
for i, p in enumerate(my_posts):
    print(f"Index: {i}, ID: {p['id']}, Title: {p['title']}, Content: {p['content']}")

```
**OUTPUT**
```python
Index: 0, ID: 1, Title: Post 1, Content: Content of post 1
Index: 1, ID: 2, Title: Post 2, Content: Content of post 2
Index: 2, ID: 3, Title: Post 3, Content: Content of post 3
```

# Documentation
When you create an API , you would normally add documentation, hence the uers know how to use it.

**FastApi**
 Generates the documentation by default

 [docs](http://localhost:8000/docs)


 # Database

 - Netx Step is to store the data in Database not in avariable until now.

  ## 1.1 Installing Postgres

  **Different components will be installed**
  - PosgreSQL server [The ddbb itself]
  - PgAdmin 4 [GUI]
  - Command line tool (psql)

- Insatalling psql
``brew install libpq``

``brew link --force libpq``

1.  Start postgre service ``brew services start postgresql@15``
2.  Start postgre terminal``psql postgres``

3. Create new user and data base
```SQL
CREATE USER postgres SUPERUSER;

CREATE USER your_user WITH PASSWORD 'your_password';
CREATE DATABASE your_database;
GRANT ALL PRIVILEGES ON DATABASE your_database TO your_user;

```
4. Install PgAdmin4
``brew install pgadmin4``

5. start psql with a given user in a given ddbb

``psql -U <user> -d <database>``

# WORKING WITH db

## PGadmin GUI
 - UNDER DATABASE --> SCHEMAS --> TABLES is where we are gonnna define our TABLES


 **QUERIES EXAMPLES**

*selecting a column with an alias*
 ```SQL
select id AS product_id , is_sale as on_sale FROM products;
 ```

*select with filter where* (<> MEANS NOT )
```SQL
SELECT id, name FROM products WHERE id=3;

SELECT id, name FROM products WHERE name='TV';

SELECT * FROM products WHERE price<=80;

SELECT * FROM products WHERE price<>80;

SELECT * FROM products where inventory >0 AND price >20
 ```
 *select with in operator*

```SQL
-- Select the employee ID, employee name, and department columns
SELECT employee_id, employee_name, department
FROM employees
-- Filter the results to include only employees whose department is 'Sales' and 'HR'
WHERE department IN ('Sales', 'HR');

select * from products where id in (1,2,3);
 ```
 
 
*LIKE OPERATOR*

```SQL
-- Select all from table products where the name starts with tv
SELECT * FROM products WHERE name LIKE 'TV%';

-- select names that does not have 'en' in the middle

SELECT * FROM products WHERE name NOT LIKE '%en%';
 ```
 
 

### inserting values

```SQL
-- inserting the required vaklues, the other are optionals
insert into products (name, price, inventory) VALUES ('tortilla',4,1000);

--returning the created items

insert into products (name, price, inventory) VALUES ('tortilla',4,1000) returning *;


 ```


```SQL
-- inserting the required vaklues, the other are optionals
UPDATE products name = 'flour',price 0 40 WHERE id=25 RETURNING *;

-


 ```

 # Creating DB for PYTHON/ API

 1. Creating the table posts in the public schema:

 ```SQL
 CREATE TABLE public.post (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content VARCHAR(200) NOT NULL,
    published boolean NOT NULL DEFAULT  TRUE,
    created_at TIMESTAMP  WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);


 ```

 2. Connecting to an existing db USING PYTHON
Install package: ``pip install psycopg2-binary ``