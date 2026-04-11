# SQL Grammar Recognizer
**Evidence 2**: Evidence Generating and Cleaning a Restricted Context Free Grammar

**Course**: Implementation of Computational Methods


## Context

SQL (Structured Query Language) is a standardized, domain-specific programming language that is used to interact with relational database management systems (RDBMS) such as MySQL, SQL Server, IBM Db2, PostgreSQL, and Oracle Database. It was first developed at IBM in the 1970s by Donald D. Chamberlin and Raymond F. Boyce, and has since become the most widely used database language in the world (Chamberlin & Boyce, 1974). SQL is formally defined as a context-free language, which means its syntax can be fully described using a Context-Free Grammar (CFG).

For this evidence, a restricted subset of SQL `SELECT` queries was chosen. The grammar covers the most common and essential parts of a SQL query: selecting columns, specifying a table, optionally filtering with `WHERE`, and optionally ordering results with `ORDER BY`.

## SQL Structure

A basic SQL SELECT query follows this structure:

```
SELECT <columns> FROM <table>
```

It can optionally include a `WHERE` clause to filter rows:

```
SELECT <columns> FROM <table> WHERE <condition>
```

And an `ORDER BY` clause to sort the results:

```
SELECT <columns> FROM <table> WHERE <condition> ORDER BY <column> ASC|DESC
```

Conditions inside `WHERE` can be combined using `AND` and `OR`, for example:

- `SELECT * FROM users WHERE age > 18` — selects all users older than 18
- `SELECT name, email FROM employees WHERE id = 1 AND age >= 25` — selects name and email from employees where two conditions are met
- `SELECT id FROM orders WHERE age < 100 OR id = 0 ORDER BY name ASC` — selects with a combined condition and sorts the result

## Context Free Grammar

*Vocabulary and grammar rules:*

**Columns (COL):** `name`, `age`, `id`, `email`, `*`

**Tables (T):** `users`, `orders`, `products`, `employees`

**Condition fields (F):** `age`, `id`, `name`, `email`

**Operators (OP):** `=`, `>`, `<`, `>=`, `<=`

**Values (V):** `NULL`, `0`, `1`, `18`, `25`, `100`, `1000`

*With those terminals defined, here is the initial Context-Free Grammar:*

```
S       ->  SELECT
SELECT  ->  'SELECT' COLS 'FROM' T
          | 'SELECT' COLS 'FROM' T W
          | 'SELECT' COLS 'FROM' T O
          | 'SELECT' COLS 'FROM' T W O
COLS    ->  COL | COLS ',' COL
COL     ->  'name' | 'age' | 'id' | 'email' | '*'
T       ->  'users' | 'orders' | 'products' | 'employees'
W       ->  'WHERE' C
C       ->  F OP V | C 'AND' C | C 'OR' C
F       ->  'age' | 'id' | 'name' | 'email'
OP      ->  '=' | '>' | '<' | '>=' | '<='
V       ->  'NULL' | '0' | '1' | '18' | '25' | '100' | '1000'
O       ->  'ORDER' 'BY' COL | 'ORDER' 'BY' COL 'ASC' | 'ORDER' 'BY' COL 'DESC'
```

*Explanation of grammar:*

1. `S -> SELECT`: The start symbol, a sentence is a SELECT statement.

2. `SELECT -> 'SELECT' COLS 'FROM' T | ...`: A SELECT statement must have a column list and a table. It may optionally have a WHERE clause (W), an ORDER BY clause (O), or both.

3. `COLS -> COL | COLS ',' COL`: The column list can be a single column or multiple columns separated by commas.

4. `COL -> 'name' | 'age' | 'id' | 'email' | '*'`: The valid column names. The `*` means "all columns".

5. `T -> 'users' | 'orders' | 'products' | 'employees'`: The valid table names in this restricted grammar.

6. `W -> 'WHERE' C`: A WHERE clause is the keyword `WHERE` followed by a condition C.

7. `C -> F OP V | C 'AND' C | C 'OR' C`: A condition can be a simple comparison (field, operator, value), or two conditions joined by AND or OR.

8. `F`: Define the valid fields.

9. `OP`: Comparison operators.

10. `V`: Values for conditions.

11. `O -> 'ORDER' 'BY' COL | ...`: An ORDER BY clause sorts results by a column, optionally specifying ASC or DESC direction.
