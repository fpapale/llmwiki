**Designing Event‑Driven Systems with Apache Kafka**  
*Ben Stopford – Foreword by Sam Newman*  

---  

### 📖 Overview  
A practical guide to building scalable, loosely‑coupled architectures using **Kafka** as a streaming platform and event store. The book walks from fundamentals to advanced patterns, showing how to replace traditional databases and RPC‑centric microservices with **event‑driven, stream‑processing services**.

### 📚 Structure  

| Part | Focus | Key Chapters |
|------|-------|--------------|
| **I – Setting the Stage** | Kafka basics, streaming origins, broker internals | 1‑4 |
| **II – Designing Event‑Driven Systems** | Events, stateful functions, Event Sourcing, CQRS, patterns | 5‑7 |
| **III – Architecture at Company Scale** | Data sharing across teams, shared event streams, “database inside‑out” | 8‑9 |
| **IV – Consistency, Concurrency & Evolution** | Eventual consistency, single‑writer principle, Kafka transactions, schema evolution | 11‑13 |
| **V – Implementing Streaming Services** | Kafka Streams, KSQL, building real‑world services (order validation, inventory, email) | 14‑15 |

### 🔑 Core Concepts  

| Concept | What it is | Why it matters |
|---------|------------|----------------|
| **Event Collaboration** | Services react to and emit events instead of direct RPC calls. | Loose coupling, pluggability, easier evolution. |
| **Event Sourcing & CQRS** | Persist *events* as the source of truth; separate write (command) and read (query) models. | Immutable audit log, scalable reads, independent evolution of read/write sides. |
| **Database Inside‑Out** | Kafka’s log = commit log; stream processors build materialized views (tables, indexes) close to the consumer. | High‑performance local reads, flexible polyglot views, eliminates heavy DB queries. |
| **Single‑Writer Principle** | One service owns writes to a given topic/partition. | Prevents write collisions, simplifies concurrency control. |
| **Kafka Transactions** | Exactly‑once guarantees across multiple topics and state stores. | Removes duplicate handling, ties state updates to event emission atomically. |
| **Schema Registry & Evolution** | Central Avro/Protobuf schema store with compatibility checks. | Safe, versioned data contracts; supports additive and breaking changes via dual‑topic upgrades. |
| **Lean Data & Materialized Views** | Store only needed fields; rebuild views from the log when schemas change. | Small, fast caches; deterministic regeneration; avoids data divergence. |

### 🛠️ Practical Tooling  

| Tool | Role |
|------|------|
| **Kafka Streams API** | Stateful stream processing (joins, windows, tables, state stores). |
| **KSQL** | SQL‑like declarative stream processing; side‑car for non‑JVM languages. |
| **Kafka Connect** | CDC & sink connectors for moving data in/out of Kafka (e.g., DB → Kafka, Kafka → Elasticsearch). |
| **Schema Registry** | Centralized schema validation & versioning. |
| **Transactions API** | Exactly‑once processing, atomic state + event writes. |
| **Interactive Queries** | Expose state‑store data via HTTP for CQRS read side. |

### 📂 Example Application (Ch. 15)  

- **Order Validation Service** – receives HTTP POST, writes `OrderCreated` events.  
- **Validation Workers** (fraud, inventory, details) consume events, emit PASS/FAIL.  
- **Aggregator** merges results, updates order state (validated/failed).  
- **Event‑Sourced View** (Kafka Streams state store) serves GET requests via interactive queries.  
- **Inventory Service** – re‑keys by `productId`, uses a local state store and Kafka transactions to atomically reserve stock.  
- **Email Service** – joins orders, payments, customers; sends notification per confirmed order.

### 🚀 Benefits Highlighted  

- **Scalability** – linear scaling via partitioned logs and stateless workers.  
- **Resilience** – replayable logs, automatic fail‑over, standby replicas.  
- **Data Consistency** – single‑writer, transactions, versioned schemas.  
- **Operational Simplicity** – immutable event log replaces complex DB migrations; schema changes are additive or handled via dual‑topic upgrades.  
- **Organizational Alignment** – mirrors Conway’s law; teams own their data streams, reducing cross‑team coupling.

### 📝 Takeaways  

1. **Treat the log as the system of record** – all facts flow through Kafka, not a traditional DB.  
2. **Design services around events** – commands trigger events; events drive downstream processing.  
3. **Leverage Kafka’s built‑in guarantees** – ordering, durability, exactly‑once semantics.  
4. **Separate concerns** – use CQRS for read/write paths, keep schemas evolvable, and isolate ownership with the single‑writer rule.  
5. **Iterate fast** – start simple, evolve to richer stream processing (joins, windows, state stores) as needs grow.

---  

**Bottom line:** By “turning the database inside‑out” and using Kafka as both **messaging backbone** and **persistent event store**, you can build highly scalable, evolvable systems that keep data as a shared, immutable source of truth while allowing each team to own and evolve its own services.