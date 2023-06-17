from neo4j import GraphDatabase

# Conexão com o servidor Neo4j
driver = GraphDatabase.driver("bolt://localhost:3000", auth=("neo4j", "teste"))

# Criação do banco de dados
def create_database():
    with driver.session() as session:
        session.run("CREATE DATABASE neo4j")

# Verifica se o banco de dados já existe
def check_database_exists():
    with driver.session() as session:
        result = session.run("SHOW DATABASES")
        databases = [record["name"] for record in result]
        return "neo4j" in databases

# Verifica se o banco de dados existe e cria-o, se necessário
def setup_database():
    if not check_database_exists():
        create_database()

# Operação CREATE: Cria um novo nó no banco de dados
def create_node(name):
    with driver.session() as session:
        session.run("CREATE (:Person {name: $name})", name=name)

# Operação READ: Retorna todos os nós do tipo "Person"
def get_all_nodes():
    with driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p")
        return result

# Operação UPDATE: Atualiza o nome de um nó
def update_node(node_id, new_name):
    with driver.session() as session:
        session.run("MATCH (p:Person {name: $node_id}) SET p.name = $new_name", node_id=node_id, new_name=new_name)

# Operação DELETE: Remove um nó do banco de dados
def delete_node(node_id):
    with driver.session() as session:
        session.run("MATCH (p:Person {name: $node_id}) DELETE p", node_id=node_id)

# Exemplo de uso
setup_database()

create_node("Alice")
create_node("Bob")

nodes = get_all_nodes()
for node in nodes:
    print(node["p"]["name"])

update_node("Alice", "Alice Smith")

delete_node("Bob")
