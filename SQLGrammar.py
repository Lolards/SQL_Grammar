import nltk
from nltk import CFG

sql_grammar = CFG.fromstring("""
    S      -> SELECT
    SELECT -> 'SELECT' COLS 'FROM' T TAIL
    TAIL   -> W O
    TAIL   -> W
    TAIL   -> O
    TAIL   ->
    COLS   -> COL COLS_A
    COLS_A -> ',' COL COLS_A
    COLS_A ->
    COL    -> 'name' | 'age' | 'id' | 'email' | '*'
    T      -> 'users' | 'orders' | 'products' | 'employees'
    W      -> 'WHERE' C
    C      -> CA C_A
    C_A    -> 'OR' CA C_A
    C_A    ->
    CA     -> CATOM CA_A
    CA_A   -> 'AND' CATOM CA_A
    CA_A   ->
    CATOM  -> F OP V
    F      -> 'age' | 'id' | 'name' | 'email'
    OP     -> '=' | '>' | '<' | '>=' | '<='
    V      -> 'NULL' | '0' | '1' | '18' | '25' | '100' | '1000'
    O      -> 'ORDER' 'BY' COL
    O      -> 'ORDER' 'BY' COL 'ASC'
    O      -> 'ORDER' 'BY' COL 'DESC'
""")

parser = nltk.ChartParser(sql_grammar)

# Tokenize: 
def tokenize(sentence):
    return sentence.strip().split()

# Recognize a sentence
def recognize(sentence):
    tokens = tokenize(sentence)
    try:
        trees = list(parser.parse(tokens))
        if trees:
            print(f"VALID: '{sentence}'")
            trees[0].pretty_print()
        else:
            print(f"INVALID: '{sentence}'")
    except ValueError:
        print(f"INVALID: '{sentence}'")

# Test cases

test_cases = [
    # Basic SELECT
    ("SELECT * FROM users", True),
    ("SELECT name FROM users", True),
    ("SELECT name , age FROM employees", True),
    ("SELECT id , name , email FROM products", True),
    ("SELECT * FROM orders", True),
    # WHERE
    ("SELECT * FROM users WHERE age > 18", True),
    ("SELECT name FROM employees WHERE id = 1", True),
    ("SELECT * FROM products WHERE age >= 25", True),
    ("SELECT email FROM users WHERE name = NULL", True),
    ("SELECT * FROM orders WHERE id < 100", True),
    ("SELECT name FROM products WHERE id = 1 AND age >= 18", True),
    ("SELECT * FROM users WHERE age > 0 AND id < 1000", True),
    ("SELECT id FROM employees WHERE age >= 18 AND age <= 100", True),
    ("SELECT * FROM users WHERE age > 0 OR id = 1", True),
    ("SELECT name FROM orders WHERE id = 0 OR id = 1", True),
    # WHERE with AND and OR combined
    ("SELECT * FROM products WHERE age >= 18 AND id < 1000 OR name = NULL", True),
    ("SELECT id FROM users WHERE age > 18 AND id = 1 OR name = NULL", True),
    # ORDER BY
    ("SELECT name FROM employees ORDER BY age ASC", True),
    ("SELECT * FROM users ORDER BY id DESC", True),
    ("SELECT * FROM orders ORDER BY name", True),
    # WHERE + ORDER BY
    ("SELECT id , email FROM users WHERE id = 100 ORDER BY name DESC", True),
    ("SELECT * FROM products WHERE age >= 18 ORDER BY id ASC", True),
    ("SELECT name FROM employees WHERE age > 25 AND id < 100 ORDER BY age DESC", True),
    # Invalid: missing parts
    ("SELECT FROM users", False),
    ("SELECT * FROM", False),
    ("SELECT * FROM users WHERE", False),
    ("SELECT * FROM users ORDER age", False),
    ("FROM users", False),
    # Invalid: vocabulary not in grammar
    ("SELECT * FROM accounts", False),
    ("SELECT salary FROM users", False),
    ("SELECT * FROM users WHERE age > 200", False),
    ("SELECT * FROM users WHERE city = 1", False),
    ("SELECT * FROM users WHERE age != 18", False),
]

# Run tests
passed = 0
for sentence, expected in test_cases:
    tokens = tokenize(sentence)
    try:
        result = len(list(parser.parse(tokens))) > 0
    except ValueError:
        result = False
    status = "PASS" if result == expected else "FAIL"
    if status == "PASS":
        passed += 1
    label = "VALID" if result else "INVALID"
    print(f"[{status}] ({label}) {sentence}")

# Show trees for valid sentences

print("\nParse trees for valid sentences:\n")
for sentence, expected in test_cases:
    if expected:
        recognize(sentence)
        print()
