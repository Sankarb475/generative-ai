Graph Data Science (GDS) in Neo4j enables you to run powerful algorithms to analyze the structure and behavior of your graph. Below are **core concepts** and **common examples** using the GDS library in Neo4j:

---

### ✅ **Setup (Install GDS Plugin)**

Make sure the GDS plugin is installed:

* In Neo4j Desktop: Go to “Plugins” → Add "Graph Data Science"
* APOC and GDS should not be mixed in the same namespace (i.e., `apoc.` vs. `gds.`)

---

### ✅ **Core Concepts**

| Concept                 | Description                                                |
| ----------------------- | ---------------------------------------------------------- |
| **Projection**          | Creates an in-memory graph from stored data                |
| **Algorithm Execution** | Run the desired graph algorithm on the projected graph     |
| **Write-back**          | Persist results (e.g., centrality score) to database       |
| **Mutate**              | Add properties to in-memory graph instead of writing to DB |
| **Drop**                | Clean up memory after use                                  |

---

✅ **Example 1: PageRank (Influence)**
-- Purpose: Measures the influence or importance of a node within the network.
-- How it Works: It's an iterative algorithm that gives a node a high score if it is pointed to by many other nodes, especially if those 
other nodes also have high scores. It's like a democratic election where influential nodes "vote" for other nodes they are connected to.
-- Use Case: Identifying central or influential entities like popular websites, key opinion leaders in a social network, or critical nodes 
in a knowledge graph.
  


// Step 1: Create in-memory projection
CALL gds.graph.project(
  'pagerank-graph',
  'Person',
  'FRIEND'
);

// Step 2: Run PageRank and write back score
CALL gds.pageRank.write('pagerank-graph', {
  writeProperty: 'pagerank'
});


---

✅ **Example 2: Community Detection (Louvain)**
-- Purpose: A community detection algorithm that finds densely connected groups (communities) of nodes in a graph.
-- How it Works: It iteratively assigns nodes to communities to maximize a value called "modularity." Modularity measures how much more 
connected nodes are within a community than they would be in a random network.
-- Use Case: Finding customer segments with similar behaviors, detecting social circles in a network, or identifying fraud rings where bad 
actors are unusually interconnected.


```cypher
CALL gds.graph.project(
  'louvain-graph',
  'User',
  {
    RELATES_TO: {
      type: 'RELATES_TO',
      orientation: 'UNDIRECTED'
    }
  }
);

CALL gds.louvain.write('louvain-graph', {
  writeProperty: 'community'
});
```

---

✅ **Example 3: Similarity (Node Similarity)**
-- Purpose: Measures the similarity between pairs of nodes based on their shared connections.
-- How it Works: It compares the neighbors of two nodes to determine how much they have in common. Common metrics include Jaccard Similarity 
(the ratio of shared neighbors to total neighbors) or Cosine Similarity.
-- Use Case: Generating "people you may know" suggestions, building a collaborative filtering-based recommendation engine ("users who liked X 
also liked Y"), or finding similar documents in a knowledge graph.


```cypher
CALL gds.nodeSimilarity.write('louvain-graph', {
  writeRelationshipType: 'SIMILAR',
  writeProperty: 'score'
});
```

---

### ✅ **Example 4: Shortest Path (Dijkstra)**

```cypher
CALL gds.graph.project(
  'shortestpath-graph',
  'Location',
  {
    CONNECTED_TO: {
      properties: 'distance'
    }
  }
);

CALL gds.shortestPath.dijkstra.stream('shortestpath-graph', {
  sourceNode: gds.util.asNode(1),
  targetNode: gds.util.asNode(5),
  relationshipWeightProperty: 'distance'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds;
```

---

### ✅ **Example 5: Node Embeddings (FastRP)**
-- Purpose: A graph embedding algorithm that represents each node as a fixed-size numerical vector.
-- How it Works: It uses a series of random projections to capture a node's topological position and its neighborhood structure, creating a 
vector representation that can be used by machine learning models.
-- Use Case: This is the bridge between a graph and machine learning. The resulting vectors can be fed into models for tasks like link prediction,
node classification (e.g., is this user a fraudster?), or recommendation systems.


```cypher
CALL gds.fastRP.write('pagerank-graph', {
  embeddingDimension: 128,
  writeProperty: 'embedding'
});
```

---

### ✅ **Example 6: K-Nearest Neighbors (KNN)**

```cypher
CALL gds.knn.write('pagerank-graph', {
  nodeProperties: ['embedding'],
  topK: 5,
  writeRelationshipType: 'SIMILAR',
  writeProperty: 'score'
});
```

---

### 🔁 **Memory Cleanup**

```cypher
CALL gds.graph.drop('pagerank-graph');
```

---

### 📚 Additional Notes:

* GDS algorithms are **streaming**, **write**, or **mutate** modes.
* You must always **project** a graph before running GDS algorithms.
* You can **filter nodes/relationships** using `nodeProperties`, `relationshipProperties`.

---
