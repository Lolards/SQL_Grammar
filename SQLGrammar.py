import nltk
from nltk import CFG

sql_grammar = CFG.fromstring("""
    S      -> SELECT
    SELECT -> 'SELECT' COLS 'FROM' T
    SELECT -> 'SELECT' COLS 'FROM' T W
    SELECT -> 'SELECT' COLS 'FROM' T O
    SELECT -> 'SELECT' COLS 'FROM' T W O
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

def tokenize(sentence):
    return sentence.strip().split()

def recognize(sentence):
    tokens = tokenize(sentence)
    trees = list(parser.parse(tokens))
    if trees:
        print(f"VALID: '{sentence}'")
        trees[0].pretty_print()
    else:
        print(f"INVALID: '{sentence}'")

# Example usage
recognize("SELECT name FROM users")