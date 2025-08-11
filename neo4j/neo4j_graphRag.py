============================================================================================================================================
Neo4j databases types
============================================================================================================================================
1) Neo4j Community Edition 
-- includes the full Cypher query language, a powerful graph data model, and the ability to run on a single instance
-- runs on a single node. There is no clustering or high-availability support
-- no read replicas to scale out read performance
-- lacks role-based access control (RBAC), multi-tenancy, and advanced security features
-- doesn't include some of the enterprise-grade tools like advanced management console or certain GDS (Graph Data Science) algorithms
-- free, open-source version for non-commercial use or basic commercial use where enterprise features are not required


2) Neo4j Enterprise Edition 
-- supports CAUSAL Clustering: allows you to run a highly available, fault-tolerant cluster of Neo4j nodes. The cluster consists of "core" 
servers (for writes) and "read replica" servers (for scaling reads)
-- fine-grained Role-Based Access Control (RBAC), LDAP/Active Directory integration, and encrypted communication
-- live backup of the database without taking it offline
-- Paid license. Pricing is typically based on factors like the number of cores, memory, and support level


3) Neo4j AuraDB
-- fully managed, serverless, cloud-native graph database without having to manage the infrastructure
-- Neo4j manages all the infrastructure, patching, backups, and scaling
-- database is on-demand and can scale automatically based on workload
-- built on a highly reliable cloud platform, providing built-in fault tolerance and backups. 
-- essentially offers the features of an Enterprise cluster but as a service



4) Neo4j Desktop 
-- desktop application for developers. It's not a different type of database core, but rather a user-friendly way to manage and interact with 
local Neo4j databases
-- allows you to create and manage multiple local databases (both Community and Enterprise editions), install and manage plugins (like the 
Graph Data Science library), and easily launch a local Neo4j Browser.



5) Neo4j Graph Data Science Library (GDS)
-- specialized library that runs on top of a Neo4j database. It contains highly optimized implementations of common graph algorithms
-- includes algorithms for things like community detection (e.g., Louvain, Label Propagation), centrality analysis (e.g., PageRank, Betweenness 
Centrality), pathfinding (e.g., A*, Dijkstra), and link prediction
-- GDS is a key selling point for Neo4j in analytics and machine learning


6) Neo4j Bloom 
-- sophisticated data visualization and exploration tool built specifically for Neo4j
-- used by business analysts, investigators, and data scientists
-- allows users to visually query the graph without writing Cypher code. You can search for patterns, create "scenes" or visualizations, 
and interact with the data in an intuitive, visual way.



7) Neo4j Sandbox
-- free, temporary, cloud-based instance of a Neo4j database, pre-loaded with sample data for specific use cases (e.g.,fraud, social networks)
-- No setup required. You get a fully functional Neo4j database in the cloud for a limited time (e.g., a few days)
-- Excellent for learning, trying out a quick concept, or giving a demonstration without needing to install anything



8) Neo4j Fabric 
-- specialized feature of Neo4j Enterprise that allows you to manage multiple separate Neo4j databases (or "shards") as a single logical database
-- provides a unified Cypher query interface that can route queries to the correct underlying database or even query across multiple databases. 
This is a very advanced scaling technique
-- to handle scenarios where a single graph is too large to fit on one machine or when you need to combine data from multiple, separate graph 
databases. This is a complex, Enterprise-only feature for highly distributed data



============================================================================================================================================
PROPERTY GRAPH VS RDF
============================================================================================================================================
RDF (Resource Description Framework)
-- Data Model: Triple-based — subject, predicate, object

<Sankar> <worksAt> <EPAM>


-- Uses ontologies (RDFS, OWL) to define classes & relationships.
-- Query Language: SPARQL


Property Graph - 
-- Nodes and relationships, both can have key-value properties.

Node: Person {name: "Sankar"}
Relationship: WORKS_AT {since: 2024}

-- Schema: Optional — flexible and schema-less by default.
-- Storage: Stored in graph databases like Neo4j, JanusGraph, Cosmos DB (Gremlin API)
-- Query Languages: Cypher, Gremlin, GSQL, openCypher.
-- Focus: Operational graph analytics, fast traversals, pattern queries.


============================================================================================================================================
Migration from a SQL database to Neo4j graph database
============================================================================================================================================
1️⃣ Understand the Existing Relational Model
-- Review ER diagrams (tables, columns, PKs, FKs).
-- Identify entities (candidates for nodes) and relationships (candidates for edges).

2️⃣ Design the Graph Model
-- decide labels 
-- relationship types 

3️⃣ Prepare the Data (ETL)
Use SSIS or Python scripts to export relational data into CSV files:
-- One CSV for each node label.
-- One CSV for each relationship type.

4️⃣ Load into the Graph Database
Option 1: Use Neo4j Bulk Import Tool (best for large datasets, offline import).
Option 2: Use Cypher LOAD CSV:

5️⃣ Validate Data Integrity
Check node counts vs original tables.
Check relationship counts vs original foreign key counts.
Run test queries to ensure data correctness.

7️⃣ Optimize & Index


============================================================================================================================================
Neo4j Read, Write, High Availability
============================================================================================================================================
Read:
Read requests can be served by any core server (follower) or read replica


Writes:
All write transactions are sent to the leader. The leader then uses the Raft protocol to replicate the transaction to the followers. 
A write is considered committed only after a quorum (a majority of core servers) has acknowledged the change. This guarantees data durability.


High Availability:
If the leader fails, the remaining core servers will elect a new leader from among the followers, ensuring continuous write availability. 
Read replicas are independent of this and continue to serve reads



============================================================================================================================================
Neo4j concepts
============================================================================================================================================
1) Property Graph Model: This is the heart of Neo4j. Be prepared to define it with its four key components:

Nodes: 
-- Represent entities (e.g., Person, Product). 
-- They can have labels (like a class or a table) and properties (key-value pairs, like attributes).

Relationships: 
-- Connect two nodes, giving the graph its structure. 
-- They are typed (e.g., FRIENDS_WITH, PURCHASED), directed, and can also have properties.

Properties: 
-- Key-value pairs on nodes and relationships.

Labels: 
-- Group nodes together for easy querying and indexing.

-- Neo4j follows ACID transaction.


2) Sharding =>
Sharding is a method of distributing data across multiple machines (shards) to scale horizontally. Each shard contains only a subset of the data,
and queries may need to access multiple shards.

Example: A user graph is split into 10 million-user subgraphs, each living on a different server.
Sharding is common in RDBMS and NoSQL (MongoDB, Cassandra), but in graph databases it introduces complexity in traversals across shards.

In graph databases, relationships are first-class citizens. Traversals depend on fast pointer hops between nodes.
If Node A is on Server 1 and its connected Node B is on Server 2, traversal becomes network-bound → slow.
Graphs tend to be highly connected, making clean sharding difficult.



3) Neo4j Fabric =>
Neo4j Fabric is Neo4j’s federation/sharding approach.
It allows you to query across multiple Neo4j databases (sharded or not) as if they were one.

Key Features:
-- Think of Fabric as a query router and coordinator.
-- You can split data across databases by region, tenant, time, etc.
-- Supports cypher queries that span databases.
-- Good for multi-tenancy, large datasets, or archiving.

Example use case:
>>> USE europe.customer1_db
MATCH (n:User)-[:BOUGHT]->(p:Product) RETURN n, p



3) Causal clustering 
-- Neo4j Causal Cluster is an architecture for high availability and read scaling. It's a group of Neo4j instances that work together as 
a single logical database
-- A minimum of three instances that form a quorum. They are responsible for handling all write operations and ensuring data durability 
using the Raft Protocol. One core server is the Leader (handles writes), and the others are Followers (replicate the data)


Read Replicas: 
Optional, but essential for read scaling. These are instances that connect to the core servers, receive a stream of data updates, 
and serve read requests. They cannot perform write operations




4) Bolt connection 
-- Bolt is a high-performance, binary, client-server protocol specifically designed by Neo4j for efficient communication.
-- much faster than using a generic HTTP REST API cause it's a lightweight binary protocol, reduces overhead of sending & parsing text-based data
-- designed for graph traversal and is state-aware, meaning it keeps the connection open and remembers the state of the session
-- Bolt is used to pass bookmarks, which are key to ensuring causal consistency in a clustered environment

-- When you connect to a Neo4j Causal Cluster, the Bolt protocol handles the routing of requests. It automatically directs writes to the 
leader and distributes read requests to the read replicas, simplifying client-side application logic



5) Causal Consistency (Bookmarks): 
-- This is a critical concept in a distributed system. 
-- It guarantees that an application will not read data older than the last data it wrote. 
-- An application gets a "bookmark" from the database after a successful write. It can then send this bookmark with its subsequent read request. 
The cluster's router will ensure that the read is served by an instance that has processed that specific transaction, preventing a stale read.



============================================================================================================================================
Neo4j MEMORY 
============================================================================================================================================
+-------------------------------------------------------------+
|                     Total Physical RAM                      |
+------------------+--------------------+--------------------+
| Heap (JVM)       | Page Cache (Neo4j) | OS & Other Memory   |
| - Query states   | - Graph store data | - FS cache          |
| - Plans          | - Index structures | - Logs & buffers    |
| - Transactions   | - Disk-mapped pages| - Native libs       |
+------------------+--------------------+--------------------+



2. Page Cache
-- Neo4j’s own native cache for storing graph data on disk (nodes, relationships, properties) in memory-mapped pages.
-- It does not store query plans or intermediate results — that’s the heap’s job.

Why it matters:
-- Every traversal (MATCH pattern) first hits the page cache to fetch graph data before doing any in-heap processing.
-- A large enough page cache means most queries avoid disk I/O entirely.

Controlled by:
>>> dbms.memory.pagecache.size
Usually set to ~50–75% of available RAM after heap is allocated.



1) Heap Memory
Controlled by:
dbms.memory.heap.initial_size and dbms.memory.heap.max_size (usually set equal for stability).
Tuning tip:
Heap should be big enough for concurrent query load, but not so big that GC pauses become long.




============================================================================================================================================
Neo4j Production Issues 
============================================================================================================================================
1) lack of distributed computing 


2) schema evolution requires significant effort, anbd brings challenges 


3) Enterprise features (clustering, Fabric) are expensive


4) Array properties become bottlenecks as they grow



============================================================================================================================================
Neo4j INDEX and CONSTRAINTS
============================================================================================================================================
*** INDEXES 

>>> SHOW INDEXES
>>> SHOW CONSTRAINTS

1) Single-property Index:
-- Creates an index on a single property of a label.

>>> CREATE INDEX property_index FOR (P:Person) ON (P.Property)


2) Composite Index:
-- Creates an index on multiple properties of a label

>>> CREATE INDEX composite_index FOR (P:Person) ON (P.property1, P.property2)


3) Text Index
-- Optimized for full-text search operations

>>> CREATE FULLTEXT INDEX full_index FOR (P:Person) ON EACH [p.name, p.location]



*** CONSTRAINTS
1) Uniqueness Constraint
-- Ensures that a property (or combination of properties) is unique across all nodes with a label.

>>> CREATE CONSTRAINT constraint1 FOR (P:Person) REQUIRED P.name is UNIQUE 


2) EXISTENCE Constraint 
-- Ensures a property exists on all nodes or relationships of a certain type.

>>> CREATE CONSTRAINT constraint2 FOR (P:Person) REQUIRE P.name is NOT NULL 


Relationship existence constraint 
>>> CREATE CONSTRAINT constraint3 FOR () - [P:Rank] - () REQUIRE P.rank is NOT NULL


3) Node Key Constraint
-- Combination of composite uniqueness and existence constraint.

>>> CREATE CONSTRAINT user_identity_key FOR (u:User) REQUIRE (u.firstName, u.lastName) IS NODE KEY




============================================================================================================================================
Neo4j Import and Export
============================================================================================================================================
Import:
-- Requires Neo4j to have access to the import directory.
-- you can change the directory by changing the below property - 
>>> dbms.directories.import=import


Neo4j only supports CSV load natively.
APOC supports insertion of following file formats - 
-- JSON 
-- XML
-- CSV 
-- YAML 
-- XLSX
-- .properties 


1) CSV - 

LOAD CSV WITH HEADERS FROM "file:///data.csv" AS row
CREATE (:Person {name: row.name, age: toInteger(row.age)})


CALL apoc.load.csv("file:///data.csv") YIELD map AS row
RETURN row


with delimiter - 
LOAD CSV WITH HEADERS FROM 'file:///your-file.csv' 
AS row 
FIELDTERMINATOR '|'
RETURN row





2) JSON - 

CALL apoc.load.json("file:///data.json") YIELD value 
UNWIND value AS row 
CREATE (:Person {name: row.name})



3) XML - 

CALL apoc.load.xml("file:///data.xml") YIELD value 
RETURN value



4) XLSX - 

CALL apoc.load.xls("file:///data.xlsx", "sheet_1") YIELD map as row 
CREATE (:Person {name: row.name})



5) YAML - 

WITH "
- name: Alice
  age: 30
- name: Bob
  age: 40" AS yaml
CALL apoc.convert.fromYamlList(yaml) YIELD value
RETURN value



6) .PROPERTIES 
CALL apoc.load.properties("file:///settings.properties")
YIELD key, value
RETURN key, value



**** LOADING LARGE CSV Files In batches using APOC 

CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///your_file.csv' AS row",
  "
  MERGE (p:Person {id: row.id})
  SET p.name = row.name, p.age = toInteger(row.age)
  ",
  {batchSize: 1000, parallel: true}
)


CALL apoc.periodic.iterate(
  "CALL apoc.load.csv('file:///your_file.csv', {sep: '|'}) YIELD map AS row",
  "
  MERGE (n:Node {id: row.id})
  SET n.name = row.name
  ",
  {batchSize: 500, parallel: false}
)




============================================================================================================================================
APOC PROCEDURES
============================================================================================================================================
Here’s a list of the **most commonly used APOC procedures** in Neo4j, categorized by usage, with brief descriptions and examples:

---

## 🔄 **1. Data Loading**

| Procedure        | Description                                   | Example                                                |                               |
| ---------------- | --------------------------------------------- | ------------------------------------------------------ | ----------------------------- |
| `apoc.load.csv`  | Load CSV with custom delimiter, quotes, types | \`CALL apoc.load.csv('file:///data.csv', {sep:'        | ', header\:true}) YIELD map\` |
| `apoc.load.json` | Load JSON from URL or file                    | `CALL apoc.load.json('file:///data.json') YIELD value` |                               |
| `apoc.load.xml`  | Load and parse XML                            | `CALL apoc.load.xml('file:///data.xml')`               |                               |
| ---------------- | --------------------------------------------- | ------------------------------------------------------ | ----------------------------- |

---

## ⚙️ **2. Batch Processing**

| Procedure               | Description                                               | Example                                                                                |
| ----------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `apoc.periodic.iterate` | Process large datasets in batches                         | See previous example for batch loading                                                 |
| `apoc.periodic.commit`  | Similar to `iterate`, more flexible for standalone Cypher | `CALL apoc.periodic.commit("MATCH (n) RETURN n", "SET n.flag=true", {batchSize:1000})` |
| ----------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------- |

---

## 🔍 **3. Path & Graph Exploration**

| Procedure                | Description                          | Example                                                             |
| ------------------------ | ------------------------------------ | ------------------------------------------------------------------- |
| `apoc.path.expand`       | Expand path from a node with filters | `CALL apoc.path.expand(start, 'FRIEND', '', 1, 5)`                  |
| `apoc.path.spanningTree` | Build a spanning tree from node      | `CALL apoc.path.spanningTree(start, {relationshipFilter:'FRIEND'})` |
| ------------------------ | ------------------------------------ | ------------------------------------------------------------------- |

---

## 🔄 **4. Graph Refactoring & Maintenance**

| Procedure                  | Description                                | Example                                                          |
| -------------------------- | ------------------------------------------ | ---------------------------------------------------------------- |
| `apoc.refactor.mergeNodes` | Merge multiple nodes into one              | `CALL apoc.refactor.mergeNodes([n1,n2], {properties:'combine'})` |
| `apoc.refactor.to`         | Convert one node/rel to another label/type | `CALL apoc.refactor.to(n, 'NewLabel')`                           |
| -------------------------- | ------------------------------------------ | ---------------------------------------------------------------- |

---

## 📈 **5. Schema & Metadata**

| Procedure          | Description                                | Example                   |
| ------------------ | ------------------------------------------ | ------------------------- |
| `apoc.meta.schema` | Inspect graph schema                       | `CALL apoc.meta.schema()` |
| `apoc.meta.stats`  | Returns counts of labels, rels, properties | `CALL apoc.meta.stats()`  |

---

## 🛠️ **6. Utility & Conversion**

| Procedure                              | Description                  | Example                                                    |
| -------------------------------------- | ---------------------------- | ---------------------------------------------------------- |
| `apoc.convert.toMap()`                 | Convert a node/JSON to a map | `RETURN apoc.convert.toMap({name:'Neo', age:30})`          |
| `apoc.date.parse` / `format`           | Parse/format date strings    | `RETURN apoc.date.format(timestamp(), 'ms', 'yyyy-MM-dd')` |
| `apoc.text.clean` / `join` / `replace` | String manipulation          | `RETURN apoc.text.replace("hello world", " ", "-")`        |

---

## 📦 **7. Exporting**

| Procedure                | Description                 | Example                                                             |
| ------------------------ | --------------------------- | ------------------------------------------------------------------- |
| `apoc.export.csv.all`    | Export entire graph to CSV  | `CALL apoc.export.csv.all("all.csv", {})`                           |
| `apoc.export.json.query` | Export query result as JSON | `CALL apoc.export.json.query("MATCH (n) RETURN n", "out.json", {})` |
| ------------------------ | --------------------------- | ------------------------------------------------------------------- |

---

## 🔗 **8. Relationship Handling**

| Procedure                  | Description                        | Example                                                 |
| -------------------------- | ---------------------------------- | ------------------------------------------------------- |
| `apoc.create.relationship` | Create relationship dynamically    | `CALL apoc.create.relationship(n1, 'KNOWS', {}, n2)`    |
| `apoc.merge.relationship`  | Merge relationship with properties | `CALL apoc.merge.relationship(n1, 'KNOWS', {}, {}, n2)` |
| -------------------------- | ---------------------------------- | ------------------------------------------------------- |

---




============================================================================================================================================
Neo4j Graph Data Science (GDS)
============================================================================================================================================
1) PageRank => finds 










============================================================================================================================================
Neo4j Set up properties 
============================================================================================================================================
1) Cluster Member type: 
-- neo4j.conf
>>> dbms.mode=CORE
>>> dbms.mode=READ_REPLICA 


2) Cluster size and discovery:
-- This tells the cluster that it requires at least three core servers to be running before the initial formation process can complete

>>> causal_clustering.minimum_core_cluster_size_at_formation=3: 

-- This ensures that the cluster requires a quorum (a majority of core servers) of three to remain online to be able to accept write operations.
If the number of online core servers drops below this, the cluster will enter a read-only state

>>> causal_clustering.minimum_core_cluster_size_at_runtime=3: 


-- This is a critical setting. On each server, you must provide a comma-separated list of the discovery endpoints for all three core servers. 
This allows the servers to find each other and form the cluster. The host should be the public IP or hostname, and the port is the one used 
for the discovery service.

>>> causal_clustering.initial_discovery_members=host1:port1,host2:port2,host3:port3


4) Network Settings:
-- This allows the server to listen on all network interfaces. This is generally necessary for cluster members to communicate with each other 
over the network.

>>> dbms.default_listen_address=0.0.0.0

-- This is how other cluster members and clients know how to contact this specific server. It should be the public IP or hostname of the server. 
This value is unique for each of the three servers

>>> dbms.default_advertised_address=your_servers_ip



5) Cluster Communication ports:
-- Used by members to find each other and to announce their presence. The port must be unique for each server if running on the same host 
(e.g., :5000, :5001, :5002).

>>> causal_clustering.discovery_listen_address=:5000


-- Used for transaction replication between core members

>>> causal_clustering.transaction_listen_address=:6000


-- Used for the Raft protocol, which handles leader election and consensus
>>> causal_clustering.raft_listen_address=:7000



6) Client Connector Ports:
-- The primary port for the Bolt protocol, used by drivers and the Neo4j Browser for communication

>>> dbms.connector.bolt.listen_address=:7687

-- The HTTP port for the web interface
>>> dbms.connector.http.listen_address=:7474





============================================================================================================================================
Neo4j & GenAI integration
============================================================================================================================================
-- GraphRAG is a powerful retrieval mechanism that improves GenAI applications by taking advantage of the rich context in graph data structures

-- When user asks a question, the RAG system converts that question into an embedding & then finds the top-N closest-matching document fragments 
(based on vector similarity)

-- The fragments are treated as individual, independent pieces of information. They are retrieved based purely on how well they match the 
semantic meaning of the question, not on their relationship to other fragments.

-- A basic RAG system is great at finding a paragraph about "X" and another paragraph about "Y," but it has no understanding of how "X" and "Y" 
are related, or if they even come from the same document.


The "Context" that is missing:
-- Hierarchical Context: How does a specific fact relate to the broader topic of the document it came from?
-- Temporal Context: How does a change in policy from last year affect the current policy?
-- Causal Context: How did event "A" lead to event "B"?
-- Relational Context: How is a person or entity "A" connected to a person or entity "B"?

The vector database is essentially a giant bucket of context-free facts. It retrieves a handful of items from that bucket, but it can't 
perform any kind of high-level reasoning on them.


This is precisely where combining RAG with a graph database like Neo4j becomes powerful


============================================================================================================================================
Neo4j + GraphRAG
============================================================================================================================================
-- it combines 
Knowledge graph + Vector Search + Graph Data Science (GDS)

Knowledge graph 
-- a clear, explainable representation of your data with relationships and context intact

GDS 
-- analyses the data at scale to uncover hidden connections, improves vector search, and enrich your knowledge graph with deeper insights

GraphRAG integrates all these with vector search.

when you put your data in vector databases through embdeddings, you lose context and relationships.
which can be avoided with graph database - graphrag



============================================================================================================================================
Vector DB and Graph RAG 
============================================================================================================================================
GraphRAG augments retrieval-based systems using graphs instead of (or alongside) pure vector databases.
-- It constructs a knowledge graph from documents (e.g., nodes = entities/concepts, edges = relationships).
-- Retrieval is guided by structure and connections in the graph — not just cosine similarity in vector space.
-- Often uses Graph Neural Networks (GNNs) or knowledge traversal algorithms like Personalized PageRank or Node2Vec.







