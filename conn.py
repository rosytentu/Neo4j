from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"

URI = "bolt://localhost:7687"
AUTH = ("user", "pwd")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")


###To create a new node:
##
##summary = driver.execute_query(
##    "CREATE (:Person {name: $name, age: $age, city: $city})",
##    name="Alice",
##    age=30,
##    city="New York",
##    database_="neo4j",
##).summary
##
##print("Created {nodes_created} nodes in {time} ms.".format(
##    nodes_created=summary.counters.nodes_created,
##    time=summary.result_available_after
##))



# merge nodes
people = [
    {"name": "Bob", "age": 25, "city": "Los Angeles"},
    {"name": "Charlie", "age": 35, "city": "Chicago"},
]

for person in people:
    summary = driver.execute_query(
        "MERGE (p:Person {name: $name}) "
        "ON CREATE SET p.age = $age, p.city = $city "
        "ON MATCH SET p.age = $age, p.city = $city",  # Optional: Update properties if node already exists
        name=person["name"],
        age=person["age"],
        city=person["city"],
        database_="neo4j"
    ).summary

    print("Created {nodes_created} nodes in {time} ms for {name}.".format(
        nodes_created=summary.counters.nodes_created,
        time=summary.result_available_after,
        name=person["name"]
    ))

records, summary, keys = driver.execute_query(
    "MATCH (p:Person) RETURN p.name AS name",
    database_="neo4j",
)



# Loop through results and do something with them
for record in records:
    print(record.data())  # obtain record as dict

# Summary information
print("The query {query} returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after
))


##update
records, summary, keys = driver.execute_query("""
    MATCH (p:Person {name: $name})
    SET p.age = $age
    """, name="Bob", age=42,
    database_="neo4j",
)
print(f"Query counters: {summary.counters}.")

##delete
##records, summary, keys = driver.execute_query("""
##    MATCH (p:Person {name: $name})
##    DETACH DELETE p
##    """, name="Alice",
##    database_="neo4j",
##)
##print(f"Query counters: {summary.counters}.")



#to add relations
records, summary, keys = driver.execute_query("""
    MATCH (alice:Person {name: $name})
    MATCH (bob:Person {name: $friend})
    CREATE (alice)-[:KNOWS]->(bob)
    """, name="Alice", friend="Bob",
    database_="neo4j",
)
print(f"Query counters: {summary.counters}.")



###delete relations
##records, summary, keys = driver.execute_query("""
##    MATCH (alice:Person {name: $name})-[r:KNOWS]->(bob:Person {name: $friend})
##    DELETE r
##    """, name="Alice", friend="Bob",
##    database_="neo4j",
##)
##print(f"Query counters: {summary.counters}.")
##



"""
#retriever

records, summary, keys = driver.execute_query(
    "MATCH (p:Person {age: $age}) RETURN p.name AS name",
    age=30,
    database_="neo4j",
)

# Loop through results and do something with them
for person in records:
    print(person)

# Summary information
print("The query {query} returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after,
))
"""

# Close the driver when done
driver.close()
