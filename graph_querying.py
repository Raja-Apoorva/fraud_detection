from neo4j import GraphDatabase

# Using Neo4j to store and query the graph
# Make sure Neo4j is running and you have the correct URI, user, and password

# Neo4j connection details
uri = "bolt://localhost:7687"
user = "neo4j"
password = "your_password"

# Create a Neo4j driver instance
driver = GraphDatabase.driver(uri, auth=(user, password))

def create_graph(tx, source, target, amount, date):
    tx.run(
        "MERGE (a:Account {name: $source}) "
        "MERGE (b:Account {name: $target}) "
        "MERGE (a)-[r:TRANSACTED {amount: $amount, date: $date}]->(b)",
        source=source, target=target, amount=amount, date=date)

# Insert data into Neo4j
with driver.session() as session:
    for idx, row in df.iterrows():
        session.write_transaction(
            create_graph,
            row['source_account'],
            row['target_account'],
            row['transaction_amount'],
            row['transaction_date'].strftime('%Y-%m-%d')
        )

# Query Neo4j for suspicious patterns
def find_fraudulent_patterns(tx):
    result = tx.run(
        "MATCH (a:Account)-[r:TRANSACTED]->(b:Account) "
        "RETURN a.name AS source, b.name AS target, r.amount AS amount"
    )
    return result.values()

with driver.session() as session:
    fraud_patterns = session.read_transaction(find_fraudulent_patterns)
    print("\nFraud Patterns from Neo4j:")
    for record in fraud_patterns:
        print(record)

driver.close()

