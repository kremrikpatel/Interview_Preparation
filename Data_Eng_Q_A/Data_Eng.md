Here is a comprehensive bank of **300 interview questions with answers** organized by category, tailored to the Lead Data Engineer on GCP role.

🔴 100 Hard Technical Questions
===============================

BigQuery (Advanced)
-------------------

**Q1. How does BigQuery's columnar storage architecture affect query performance and cost?**BigQuery stores data in Dremel's columnar format (Capacitor), meaning only queried columns are scanned. This minimizes I/O, dramatically cutting costs (billed per bytes scanned) and improving performance vs. row-based systems. Always SELECT only needed columns and avoid SELECT \*.​

**Q2. Explain the difference between partitioned and clustered tables. When would you use both together?**Partitioning divides a table into segments (by date, integer range, or ingestion time), enabling partition pruning so only relevant segments are scanned. Clustering sorts data within partitions by specified columns (up to 4), further reducing scan size for high-cardinality filter columns. Use both when querying large tables filtered on a date range AND a high-cardinality column like user\_id or region.​

**Q3. What are BigQuery slots and how do reservations work?**Slots are units of BigQuery computational capacity (CPU, memory, I/O). On-demand pricing uses shared slots; reservations (via BigQuery Editions) guarantee dedicated slots to projects or folders. Use INFORMATION\_SCHEMA.JOBS and ASSIGNMENTS views to monitor slot utilization and right-size reservations for predictable workloads.​

**Q4. How do you handle schema evolution in BigQuery without breaking downstream consumers?**Use NULLABLE mode for new columns and avoid removing or renaming columns. For breaking changes, create a new versioned dataset (e.g., dataset\_v2), use authorized views to abstract schema, and maintain backward-compatible views on top of evolving base tables.​

**Q5. What is BI Engine and when should you use it?**BI Engine is an in-memory analysis service that accelerates SQL queries by caching frequently accessed table data. It's ideal for dashboarding tools like Looker Studio where sub-second latency is needed on repeated queries against relatively stable datasets. It complements but doesn't replace clustering/partitioning.

**Q6. How do you implement row-level security in BigQuery?**Use row-level access policies via CREATE ROW ACCESS POLICY statements, which filter rows based on a USING expression tied to SESSION\_USER() or group membership. Combine with column-level security via policy tags in Data Catalog for fine-grained PII control.

**Q7. Explain INFORMATION\_SCHEMA and how you use it for cost governance.**INFORMATION\_SCHEMA.JOBS logs every query's bytes processed, slot milliseconds, user, and duration. You can build a governance dashboard by querying this view to identify expensive queries, heavy users, and optimize or enforce quotas using Custom IAM conditions.

**Q8. What is the difference between standard and materialized views in BigQuery?**Standard views are virtual — they re-execute the underlying SQL on every query. Materialized views pre-compute and cache the results, refreshing automatically when base tables change. Use materialized views for aggregations accessed frequently to avoid repeated full-table scans.

**Q9. How does BigQuery handle late-arriving data in streaming inserts?**Streaming inserts via the Storage Write API are immediately queryable but not immediately deduplicated. Use insertId for best-effort deduplication within a time window. For guaranteed exactly-once semantics, use the Storage Write API in committed mode or Dataflow's exactly-once streaming.

**Q10. How do you optimize JOIN performance in BigQuery?**Put the largest table on the left side of the JOIN (BigQuery distributes the right-side table). Use broadcast joins for small dimension tables (<100MB). Pre-filter both sides before joining, and denormalize where appropriate using nested STRUCT and ARRAY types to avoid joins entirely.

Dataflow (Advanced)
-------------------

**Q11. Explain the difference between bounded and unbounded PCollections in Apache Beam.**Bounded PCollections represent finite datasets (batch); unbounded represent infinite streams (streaming). Dataflow auto-detects the runner mode but you can force it. The same pipeline code can handle both, which is the power of Beam's unified model.

**Q12. What is windowing in Dataflow and what are the window types?**Windowing groups elements of an unbounded stream into finite buckets for aggregation. Types include: Fixed (tumbling) windows (non-overlapping equal-size buckets), Sliding windows (overlapping), Session windows (activity-based, gaps trigger new windows), and Global windows (default, for batch).

**Q13. How do you handle late data in a Dataflow streaming pipeline?**Use withAllowedLateness() on your windowing strategy. Elements arriving after the watermark but within the allowed lateness are placed in the correct window. Use accumulation mode (ACCUMULATING vs. DISCARDING) to decide how late firings interact with earlier results.

**Q14. What is the difference between Dataflow Shuffle and Streaming Engine?**Dataflow Shuffle offloads shuffle operations (for batch) to Google's backend, reducing worker memory and improving performance/cost. Streaming Engine offloads window state and timers (for streaming) to backend, enabling auto-scaling without memory bottlenecks.

**Q15. How do you implement exactly-once processing in Dataflow?**For streaming, enable --experiments=enable\_exactly\_once\_streaming with the Streaming Engine. This uses a distributed commit protocol to ensure each record is processed exactly once end-to-end, at higher cost than at-least-once. For sinks, use idempotent writes or transactional APIs.

**Q16. Explain Dataflow FlexTemplates vs Classic Templates.**Classic Templates are pre-compiled JAR/Python files with static parameters. FlexTemplates package the pipeline in a Docker container, enabling dynamic parameter types, runtime dependencies, and Python packages not available at compile time. FlexTemplates are preferred for modern deployments.

**Q17. How do you debug a Dataflow pipeline with poor performance?**Check the Dataflow UI for hot keys (data skew), worker CPU/memory in Cloud Monitoring, and stage execution times. Use ParDo fusions and check if bottleneck stages are fused or separated. Profile with --experiments=use\_runner\_v2 and enable detailed logging per worker.

**Q18. What is a SideInput in Apache Beam and when do you use it?**A SideInput provides additional read-only data to a ParDo transform, such as a lookup table or configuration. Unlike joining two PCollections, SideInputs are broadcast to all workers. Use them when one dataset is small enough to hold in memory (e.g., dimension table lookups).

**Q19. How does watermarking work in streaming Dataflow pipelines?**A watermark estimates the current event-time progress. Dataflow tracks the oldest in-flight event timestamp and advances the watermark as data arrives. When the watermark passes a window's end, the window triggers. The accuracy of watermarks depends on source timestamps and withTimestampFn().

**Q20. How do you right-size Dataflow workers for cost efficiency?**Enable Horizontal Autoscaling (--autoscalingAlgorithm=THROUGHPUT\_BASED) and set --maxNumWorkers. Use n1-standard vs n1-highmem based on whether the bottleneck is CPU or memory. For streaming, prefer Streaming Engine to avoid over-provisioning for state storage.

Pub/Sub & Event-Driven Architecture
-----------------------------------

**Q21. What is the difference between Pub/Sub and Pub/Sub Lite?**Pub/Sub is fully managed, globally replicated, and serverless with at-least-once delivery. Pub/Sub Lite is zonal (or regional), cheaper, but requires capacity provisioning (throughput units) and has no global replication. Use Lite for high-throughput, cost-sensitive, single-region pipelines.

**Q22. How do you guarantee message ordering in Pub/Sub?**Enable message ordering on the topic and use an ordering key in the publish request. Subscribers must use enable\_message\_ordering=True. All messages with the same ordering key are delivered in order to a single subscriber, but this limits parallelism for that key.

**Q23. Explain the dead-letter queue pattern in Pub/Sub.**Configure a dead-letter topic on the subscription with a max\_delivery\_attempts threshold. Messages that fail processing beyond this limit are forwarded to the dead-letter topic for inspection and replay. This prevents poison-pill messages from blocking pipeline progress.

**Q24. How do you handle Pub/Sub message deduplication?**Pub/Sub guarantees at-least-once delivery, so deduplication must be done downstream. Use the message\_id (assigned by Pub/Sub) or a custom ordering\_key + timestamp as an idempotency key. Store processed IDs in Bigtable or Memorystore for fast lookup.

**Q25. What are Pub/Sub snapshots and when are they used?**Snapshots capture the state of a subscription at a point in time, retaining unacknowledged messages. They enable replay: you can seek a subscription back to a snapshot to reprocess messages after a bug fix. Retained for up to 7 days.

Cloud Composer / Airflow
------------------------

**Q26. How do you design idempotent DAGs in Airflow?**Each task should produce the same result regardless of how many times it runs. Use execution\_date as a partition key, implement upserts (MERGE) instead of inserts, check for existence before writing, and use catchup=False unless backfilling is explicitly needed.

**Q27. What is the XCom mechanism and what are its limitations?**XComs (cross-communications) allow tasks to share small amounts of data via Airflow's metadata database. They're suitable for IDs, status flags, or small strings — not large datasets. Storing large payloads via XCom causes metadata DB bloat; instead write to GCS and pass the path.

**Q28. How do you implement dynamic DAG generation in Airflow?**Generate DAGs programmatically in Python by iterating over a config (e.g., a JSON file in GCS or a DB query) at DAG file parse time. Use globals()\[dag\_id\] = dag to register each. Be cautious: excessive dynamic DAGs slow the scheduler; use DAG factories with caching.

**Q29. What is the difference between Airflow's Sequential, Local, and Celery executors?**Sequential runs one task at a time (dev only). Local executor runs tasks in parallel on the same machine. Celery distributes tasks across worker nodes using a message broker (Redis/RabbitMQ). Cloud Composer uses Celery (Composer 1) or Kubernetes (Composer 2) executors.

**Q30. How do you handle secrets management in Cloud Composer?**Use the Secret Manager backend for Airflow connections and variables. Configure \[secrets\] backend = airflow.providers.google.cloud.secrets.secret\_manager.CloudSecretManagerBackend in airflow.cfg. This avoids storing credentials in the Airflow metadata DB, which is less secure.

DataFusion & ETL
----------------

**Q31. When would you choose DataFusion over building a custom Dataflow pipeline?**DataFusion is better for teams needing a visual, low-code ETL tool with pre-built connectors (SAP, Salesforce, JDBC). Use it when development speed matters more than fine-grained control. For high-performance, complex transformations or custom business logic, Dataflow (Beam) is preferable.

**Q32. How does DataFusion handle lineage and metadata?**DataFusion integrates with Data Catalog to automatically push lineage metadata when pipelines run. Each pipeline execution records source-to-target field-level lineage, enabling impact analysis and data governance without manual documentation.

**Q33. What are Wrangler directives in DataFusion?**Wrangler is DataFusion's interactive data preparation tool. Directives are transformation instructions (e.g., parse-as-csv, mask-data, filter-rows-on) applied visually or programmatically. They generate a recipe that becomes a pipeline stage.

**Q34. How do you optimize DataFusion pipeline performance?**Partition source data before reading, push down filters to the source plugin, increase executor/driver memory for the Dataproc cluster, use native execution plugins (e.g., BigQuery Sink with direct write), and avoid unnecessary field mappings that add serialization overhead.

**Q35. Explain the DataFusion plugin architecture.**DataFusion uses a plugin framework (CDAP-based) where each pipeline stage is a plugin (Source, Transform, Sink, Action, Condition). Plugins are versioned, deployable as JARs, and configurable via JSON. Custom plugins can be built using the Java SDK for proprietary systems.

Cloud SQL, GCS & Storage
------------------------

**Q36. How do you migrate a large Cloud SQL database with minimal downtime?**Use Database Migration Service (DMS) for continuous replication. Set up DMS with a connection profile pointing to the source, run full dump + CDC replication, validate row counts and checksums, then perform a controlled cutover during a low-traffic window.

**Q37. What GCS storage classes would you choose for a data lake's different zones?**

*   **Raw/landing zone**: Standard (frequently accessed during ingestion)
    
*   **Archive zone** (data older than 90 days): Nearline or Coldline
    
*   **Long-term archive** (>1 year): Archive classUse Lifecycle Management policies to auto-transition objects between classes.
    

**Q38. How do you handle small-file problems in GCS-based data lakes?**Small files cause excessive metadata overhead and slow Dataflow/Dataproc reads. Compact them using Dataflow's WriteFiles with sharding hints, or run a periodic compaction job (using Dataflow or Spark) to combine small Parquet/Avro files into larger ones.

**Q39. What is the difference between GCS Uniform Bucket-Level Access and ACLs?**Uniform Bucket-Level Access disables object-level ACLs and enforces IAM only at the bucket/project level, simplifying governance. ACLs allow per-object permissions but are harder to audit. Uniform access is the recommended security posture for enterprise data lakes.

**Q40. How do you implement data retention policies in GCS?**Use Object Lifecycle Management rules to delete or transition objects based on age, creation date, or number of newer versions. For compliance (e.g., GDPR), use Object Lock (retention policies) to prevent deletion within a retention period, combined with DLP scans to identify PII.

CI/CD, IaC & DevOps for Data
----------------------------

**Q41. How do you implement CI/CD for BigQuery SQL transformations?**Use dbt or Dataform with a Git-based workflow. On PR, run dbt compile + dbt test in a CI pipeline (GitHub Actions/Cloud Build). On merge to main, deploy to a staging dataset, run integration tests, then promote to production using environment-specific profiles.

**Q42. How do you manage Terraform state for multi-environment GCP data infrastructure?**Use remote state in GCS with separate state files per environment (dev/staging/prod). Enable state locking with GCS. Use Terraform workspaces or separate directories per environment with a shared modules structure to avoid drift and enable code reuse.

**Q43. How do you implement blue-green deployments for data pipelines?**Deploy the new pipeline version in parallel (green) alongside the current (blue). Route a subset of traffic (e.g., Pub/Sub subscription) to green. Validate outputs by comparing BigQuery table checksums or row counts. Once validated, cut all traffic to green and decommission blue.

**Q44. What is your approach to testing data pipelines?**

*   **Unit tests**: Mock sources/sinks, test transformation logic (pytest + Apache Beam's TestPipeline)
    
*   **Integration tests**: Run against a sandbox GCP project with real services
    
*   **Data quality tests**: dbt tests, Great Expectations, or custom SQL assertions
    
*   **Contract tests**: Validate schema compatibility between producer/consumer
    

**Q45. How do you handle Airflow DAG versioning in CI/CD?**Store DAGs in a Git repo. CI pipeline runs pylint, flake8, and pytest on DAG files. Deployment uses gsutil rsync or Cloud Build to sync the DAG bucket. Use DAG tags for versioning and feature flags in DAG configs to enable/disable new logic without redeployment.

Security & Governance
---------------------

**Q46. How do you implement column-level security for PII in BigQuery?**Use BigQuery's policy tags (taxonomy defined in Data Catalog). Assign tags like PII.email, PII.phone to columns. Grant Fine-Grained Reader role only to authorized users. Unauthorized users see NULL when querying masked columns, without needing to change SQL.

**Q47. What is Cloud DLP and how do you integrate it into a data pipeline?**Cloud DLP (Data Loss Prevention) detects, classifies, and optionally de-identifies sensitive data. Integrate it as a Dataflow step using the DlpInspectTransform to scan streaming records for PII, route matches to a quarantine topic, and apply tokenization or masking before writing to BigQuery.

**Q48. How do you implement VPC Service Controls for a BigQuery data warehouse?**Define a VPC Service Controls perimeter around BigQuery, GCS, and Cloud KMS projects. Resources inside the perimeter can communicate freely; access from outside requires an access level (IP range or identity). This prevents data exfiltration even by privileged insiders.

**Q49. Explain the principle of least privilege in GCP IAM for data teams.**Assign the most restrictive role that allows the required actions. Use predefined roles (e.g., roles/bigquery.dataViewer) over primitive roles. For pipeline service accounts, grant only the specific resources they need access to (e.g., a single dataset, not the whole project). Use Conditions for time-bound access.

**Q50. How do you audit data access in BigQuery?**Enable Cloud Audit Logs (Data Access logs: DATA\_READ, DATA\_WRITE). Export audit logs to BigQuery via a log sink for analysis. Use INFORMATION\_SCHEMA.JOBS for query-level auditing. Set up alerts in Cloud Monitoring for unusual patterns (e.g., large exports or off-hours access).

Data Modelling (Advanced)
-------------------------

**Q51. When would you use a Data Vault model vs. a Kimball star schema in BigQuery?**Data Vault is better for ingesting raw data from many heterogeneous sources with full historization and auditability (Hub-Satellite-Link). Kimball star schemas are optimized for query performance and BI tool consumption. Many modern architectures use Data Vault in the raw/staging layer and star schemas in the presentation layer.

**Q52. How do you model slowly changing dimensions (SCD) in BigQuery?**

*   **SCD Type 1**: Overwrite (no history, simple MERGE)
    
*   **SCD Type 2**: Add rows with valid\_from/valid\_to dates and is\_current flag — best for audit trails
    
*   **SCD Type 4**: Use a separate history tableBigQuery's MERGE statement handles SCD Type 2 efficiently with partitioning on valid\_from.
    

**Q53. Explain dimensional modelling in the context of a data lakehouse.**A lakehouse combines raw storage (GCS) with query capability (BigQuery external tables or BQ native). Apply dimensional modelling in the curated/gold layer: fact tables hold measurable events, dimension tables hold descriptive attributes. Use BigQuery materialized views to pre-aggregate facts for BI tools.

**Q54. How do you handle many-to-many relationships in BigQuery models?**Use a bridge table (fact-less fact table) to resolve M:M relationships. In BigQuery, you can also use ARRAY of STRUCT for denormalized representations, which avoids JOINs and leverages BigQuery's nested data model for better query performance.

**Q55. What is the difference between a star schema and a snowflake schema, and which is better for BigQuery?**Star schema denormalizes dimensions into single wide tables; snowflake normalizes them into multiple related tables. BigQuery favors star schemas (denormalized) because JOIN costs are high at petabyte scale, storage is cheap, and nested/repeated fields handle hierarchy more efficiently than snowflake joins.

Streaming & Real-Time
---------------------

**Q56. How do you design a Lambda architecture on GCP?**Batch layer: GCS → Dataflow batch → BigQuery. Speed layer: Pub/Sub → Dataflow streaming → Bigtable/BigQuery streaming buffer. Serving layer: BigQuery views that UNION both layers. Modern trend is to replace Lambda with Kappa (streaming only, replaying for batch corrections).

**Q57. What is a Kappa architecture and why is it preferred for modern GCP designs?**Kappa uses a single streaming pipeline for both real-time and historical processing by replaying events from a durable log (Pub/Sub with retention or GCS). It's simpler to operate than Lambda (one codebase), and Dataflow's unified batch/streaming model makes it practical on GCP.

**Q58. How do you handle backpressure in a Pub/Sub → Dataflow pipeline?**Dataflow automatically applies backpressure by controlling the pull rate from Pub/Sub based on worker capacity. Monitor pubsub.googleapis.com/subscription/oldest\_unacked\_message\_age — if it grows, scale workers or optimize processing. Enable Streaming Engine for better flow control.

**Q59. What is Change Data Capture (CDC) and how do you implement it on GCP?**CDC captures row-level changes (INSERT/UPDATE/DELETE) from a transactional database in real time. On GCP: use Datastream to read CDC from Cloud SQL/AlloyDB/MySQL/PostgreSQL → write to GCS or BigQuery. Datastream uses log-based CDC (reads transaction logs) for minimal DB impact.​

**Q60. How do you implement exactly-once end-to-end from Pub/Sub to BigQuery?**Use Pub/Sub's exactly-once delivery (enabled on subscription) + Dataflow's exactly-once mode + BigQuery Storage Write API in committed mode. Each layer guarantees no duplicates. Without all three, use idempotency keys and MERGE in BigQuery to deduplicate on arrival.

Q61–Q70: Performance & Cost Optimization
========================================

Q61. Use APPROX\_COUNT\_DISTINCT and Approximate Functions
----------------------------------------------------------

**Q61. When and why should you use APPROX\_COUNT\_DISTINCT instead of COUNT(DISTINCT ...) in BigQuery?**

COUNT(DISTINCT col) requires a full shuffle of all values to compute exact uniqueness — at scale, this is extremely expensive. APPROX\_COUNT\_DISTINCT uses the **HyperLogLog++ (HLL) algorithm**, a probabilistic data structure that estimates distinct counts using a fraction of the memory and compute.​

The accuracy is typically within **~1% error**, which is acceptable for analytics, dashboards, and trend analysis. A real-world case study showed this reduced data scanning from **6.5TB to 16.25GB per query** and dropped query time from hours to 7 seconds, slashing slot usage from 2,000 to just 135.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Expensive — full shuffle required  SELECT COUNT(DISTINCT user_id) FROM events;  -- Cheap — HLL approximation, ~1% error  SELECT APPROX_COUNT_DISTINCT(user_id) FROM events;   `

Similarly, use APPROX\_QUANTILES(col, 100) for percentile calculations and APPROX\_TOP\_COUNT for top-N frequency analysis. **Rule of thumb**: use approximate functions in all exploratory analytics and dashboards; only use exact functions in financial reporting or compliance contexts where precision is mandatory.​

Q62. Cache Intermediate Results in GCS
--------------------------------------

**Q62. How do you use GCS caching to avoid recomputation in multi-stage pipelines?**

In complex pipelines with multiple downstream consumers reading the same intermediate dataset, recomputing the same transformation repeatedly wastes both time and money. The pattern is to **materialise expensive intermediate results** as Parquet files in GCS after the first computation.

**Implementation approach:**

*   After a heavy Dataflow transformation (e.g., joining 3 large tables, deduplication), write the result to gs://bucket/cache/date=YYYY-MM-DD/output.parquet
    
*   Downstream pipeline steps read from GCS instead of re-executing the transform
    
*   Use a metadata flag (a \_SUCCESS marker file or an Airflow XCom value) to signal cache availability
    
*   Implement a cache invalidation strategy: TTL-based (delete after N days via GCS lifecycle policy) or event-based (invalidate on source data change)
    

In Airflow, use a GCSObjectExistenceSensor to check for the cache file before deciding whether to run the expensive task or skip to the consumer step. This pattern is foundational in medallion architectures where Bronze → Silver transformations are expensive and Silver data is shared across multiple Gold pipelines.

Q63. Use BigQuery BI Engine for Dashboard Performance
-----------------------------------------------------

**Q63. What is BigQuery BI Engine and when should you use it for performance optimisation?**

BigQuery BI Engine is an **in-memory analysis service** that accelerates SQL queries by caching table data in a fast, columnar in-memory store. When a query is eligible, BI Engine serves it from memory rather than scanning GCS-backed storage, delivering **sub-second response times** even on large tables.​

**When to use it:**

*   Dashboards in Looker Studio, Looker, or Tableau hitting the same BigQuery tables repeatedly
    
*   Queries on tables that fit within your BI Engine reservation size (reservations from 1GB to 250GB+)
    
*   Read-heavy workloads with relatively stable data (e.g., daily-refreshed aggregations)
    

**When NOT to use it:**

*   Ad-hoc exploratory queries with unpredictable access patterns
    
*   Tables larger than your reservation size (only some queries will be accelerated)
    
*   Write-heavy streaming tables where data changes faster than BI Engine can re-cache
    

BI Engine works transparently — no SQL changes are needed. You purchase a reservation in a specific region and project, and eligible queries are automatically accelerated. Monitor the bi\_engine\_statistics field in INFORMATION\_SCHEMA.JOBS to confirm queries are hitting BI Engine.

Q64. Monitor Dataflow CPU Utilisation for Right-Sizing
------------------------------------------------------

**Q64. How do you right-size Dataflow workers to avoid over-provisioning?**

Dataflow's autoscaling is powerful but imperfect — pipelines can run with too many workers (wasting money) or too few (causing lag). The key is **continuous monitoring of worker-level metrics** in Cloud Monitoring.​​

**Key metrics to watch:**

*   dataflow.googleapis.com/job/per\_stage\_workers — actual worker count per stage
    
*   compute.googleapis.com/instance/cpu/utilization — per-worker CPU
    
*   dataflow.googleapis.com/job/elements\_produced\_count — throughput per stage
    

**Decision rules:**

*   CPU consistently **<50%** → reduce --maxNumWorkers or the machine type (e.g., switch from n1-standard-8 to n1-standard-4)
    
*   CPU consistently **\>85%** → increase --maxNumWorkers or upgrade machine type
    
*   Memory pressure (OOM errors) → switch from n1-standard to n1-highmem series
    

For streaming jobs, always enable **Streaming Engine** (--enable\_streaming\_engine) which offloads window state to Google's backend — this significantly reduces per-worker memory requirements and allows more aggressive downscaling. Set --autoscalingAlgorithm=THROUGHPUT\_BASED and a realistic --maxNumWorkers cap to prevent runaway cost during traffic spikes.​

Q65. Use Committed Use Discounts for Predictable BigQuery Slots
---------------------------------------------------------------

**Q65. When should you switch from BigQuery on-demand pricing to capacity-based pricing?**

On-demand pricing charges **$6.25 per TB scanned** (as of 2025), which is unpredictable and expensive at scale. BigQuery Editions (Standard, Enterprise, Enterprise Plus) offer **slot-based pricing** where you pay for compute capacity rather than data scanned.

**Decision framework:**

Workload TypeRecommended PricingUnpredictable, low-volumeOn-demandPredictable production workloadsStandard Edition + AutoscaleMission-critical, SLA-boundEnterprise Edition with baseline slotsReal-time dashboardsBaseline slots + BI Engine

Use INFORMATION\_SCHEMA.RESERVATION\_TIMELINE\_BY\_PROJECT to analyse your actual slot consumption over the past 30 days. If you're consistently using >400 slots for more than 50% of the day, Editions pricing is almost always cheaper. Purchase **baseline slots** for guaranteed minimum capacity and configure autoscale\_max\_slots to handle spikes without over-provisioning the baseline.​

Q66. Avoid SELECT \* — Column Pruning
-------------------------------------

**Q66. Why is SELECT \* harmful in BigQuery and how do you enforce column discipline at scale?**

BigQuery's columnar storage means **only queried columns are scanned** from disk. A SELECT \* forces every column to be read, multiplying bytes billed proportionally to the number of columns. On a 100-column, 1TB table, SELECT \* might scan 100x more data than a query selecting 5 relevant columns.

**Enforcement strategies:**

1.  **Linting in CI/CD**: Use sqlfluff with a rule that flags SELECT \* in production SQL files
    
2.  **dbt source freshness tests**: Add a dbt schema test that validates column lists
    
3.  **Dry-run cost gates**: Run bq --dry\_run in CI and fail if estimated bytes exceed a threshold
    
4.  **Education**: Show analysts their actual cost impact via INFORMATION\_SCHEMA.JOBS dashboards
    
5.  **Authorized views**: Expose only needed columns to analysts rather than raw tables
    

For nested data, avoid SELECT \* EXCEPT (nested\_col) patterns — they still materialise the full struct. Instead, explicitly select the nested fields you need using dot notation.

Q67. Use Dataflow Reshuffle to Break Fusion and Fix Data Skew
-------------------------------------------------------------

**Q67. What is stage fusion in Dataflow, when is it harmful, and how does Reshuffle fix it?**

Dataflow automatically **fuses** adjacent ParDo transforms into a single execution stage to reduce serialization overhead — this is usually beneficial. However, when a heavy GroupByKey is followed by another expensive ParDo, Dataflow may fuse them, creating a bottleneck where all the heavy work lands on the same set of workers.​

A real production case reported **3–5 second tail latency** on a streaming pipeline. Adding a single Reshuffle transform between the GroupByKey and the next ParDo broke the bad fusion, dropped latency to ~1.5 seconds.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Before: fused — all work on same worker set  data | 'GroupBy' >> beam.GroupByKey()       | 'HeavyTransform' >> beam.ParDo(HeavyFn())  # After: reshuffle breaks fusion, redistributes data  data | 'GroupBy' >> beam.GroupByKey()       | 'Reshuffle' >> beam.Reshuffle()  # forces redistribution       | 'HeavyTransform' >> beam.ParDo(HeavyFn())   `

Reshuffle also fixes **hot key skew**: if one key has 1M elements and others have 100, one worker is overwhelmed. After Reshuffle, elements are randomly redistributed. Use beam.Reshuffle.viaRandomKey() specifically for hot key mitigation. Monitor stage-level metrics (not just job-level) in the Dataflow UI to identify which stage is the bottleneck before adding Reshuffle blindly.

Q68. Right-Size Cloud Composer and Use Composer 2 for Autoscaling
-----------------------------------------------------------------

**Q68. How do you optimise Cloud Composer for performance and cost?**

Cloud Composer 2 (and Composer 3) uses a **GKE Autopilot-based architecture** with three autoscalers: Horizontal Pod Autoscaler (HPA), Cluster Autoscaler (CA), and Node Auto-Provisioning (NAP). This means workers scale in and out automatically within your configured min\_workers and max\_workers bounds — you only pay for what you use.​

**Right-sizing checklist:**

*   Monitor airflow.googleapis.com/environment/num\_queued\_tasks — if consistently >0, increase max\_workers
    
*   Monitor airflow.googleapis.com/environment/worker/pod\_eviction\_count — evictions signal memory pressure; increase worker memory
    
*   Monitor airflow.googleapis.com/environment/scheduler/heartbeat\_age — if >10 seconds, the scheduler is overloaded; increase scheduler CPU
    
*   Set max\_active\_runs\_per\_dag and max\_active\_tasks to prevent runaway parallelism
    
*   Use Composer 3 (latest) for the most granular resource control and lowest overhead
    

**Cost optimisation:**

*   Set min\_workers=1 for non-critical environments (dev/staging) to scale to near-zero
    
*   Use deferrable operators (Airflow 2.2+) which release workers while waiting for external events (e.g., waiting for a Dataflow job), dramatically reducing worker count during I/O-bound waits
    
*   Avoid storing large data in XCom — this bloats the Cloud SQL metadata database and slows the scheduler
    

Q69. Use BigQuery Flex Slots for Bursty Workloads
-------------------------------------------------

**Q69. What are Flex Slots and how do they differ from standard slot commitments?**

BigQuery Editions offer three commitment types: **on-demand** (per-TB, no commitment), **standard reservations** (monthly/annual commitment with 1-year minimum), and **Autoscale slots** which expand baseline capacity during peaks.​

Flex Slots (now part of BigQuery Editions Autoscale) allow you to:

*   Purchase burst capacity for as little as **60 seconds**
    
*   Automatically scale up when baseline slots are exhausted and scale back down when the burst ends
    
*   Avoid paying for peak capacity 24/7 when peak usage only occurs for a few hours per day
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Autoscale configuration within a reservation  CREATE RESERVATION `analytics_production`  OPTIONS (    slot_capacity = 200,           -- baseline, always available    autoscale_max_slots = 2000,    -- burst capacity, billed when used    edition = 'STANDARD'  );   ``

The practical pattern for a consulting environment is: **200 baseline slots** (covers normal ETL + light querying) + **autoscale to 2,000** for end-of-month reporting jobs or client demonstrations. This avoids both the cost of permanent 2,000-slot reservation and the unpredictability of pure on-demand pricing.​

Q70. Compress GCS Data as Snappy-Compressed Parquet
---------------------------------------------------

**Q70. What file format and compression should you use in a GCS data lake and why?**

The choice of file format has a compounding effect on storage cost, read performance, and pipeline throughput across every stage of your data lake.

**Format comparison:**

FormatStorageRead SpeedSchema EvolutionBest Use CaseCSV/JSONBaselineSlow (row scan)PoorRaw landing zone onlyAvro2–3x smallerGood (row-based)ExcellentPub/Sub serialization, KafkaParquet3–5x smallerFastest (columnar)GoodAnalytics, Dataflow, BigQueryORC3–5x smallerFastGoodHive/Spark ecosystems

**Recommendation for GCP data lakes:**

*   Use **Parquet with Snappy compression** for the refined/curated zones — Snappy offers fast decompression (better than Gzip for query performance) with good compression ratios (3–5x vs. raw)
    
*   Use **Avro** for Pub/Sub schema-registered topics and Dataflow pipeline intermediate data (row-oriented, fast for record-by-record streaming)
    
*   Target **Parquet file sizes of 128MB–1GB** — too small causes metadata overhead (the small-file problem), too large limits parallelism
    

In Dataflow, control output file size using WriteFiles.withNumShards() or withSharding(). In BigQuery exports, Parquet is the recommended format for downstream Dataflow or Dataproc consumption.​

Q71–Q100: Advanced Architecture (Full Answers)
==============================================

Q71. Medallion Architecture on GCS + BigQuery
---------------------------------------------

**Q71. Design a medallion (Bronze/Silver/Gold) architecture on GCP.**

The medallion architecture organises data into three quality tiers, each stored in GCS and queryable via BigQuery:​

**Bronze (Raw):** Exact copy of source data, never modified. Store in gs://datalake/bronze/{source}/{date}/ as raw JSON, CSV, or Avro. BigQuery external tables provide SQL access without loading. Retain indefinitely for auditability. No transformations — this is the "single source of truth" for replay.

**Silver (Refined):** Cleaned, validated, deduped, and schema-enforced data. Dataflow pipelines read from Bronze, apply DLP for PII detection/masking, enforce schemas (reject/quarantine invalid records), deduplicate, and write Snappy-compressed Parquet to gs://datalake/silver/. Load into BigQuery native partitioned/clustered tables for SQL access.

**Gold (Curated/Business):** Business-domain models built with dbt in BigQuery. Star schemas, aggregations, and KPI tables consumed by BI tools, APIs, and ML models. Access controlled via BigQuery authorized views per team/domain.

**CI/CD flow:** dbt runs in Cloud Build → tests gate promotion → Cloud Composer orchestrates Bronze→Silver Dataflow jobs → dbt Cloud handles Silver→Gold transformations on schedule.

Q72. Data Mesh on GCP
---------------------

**Q72. How do you implement a data mesh architecture on GCP?**

Data mesh distributes data ownership to domain teams rather than centralising it in a single data engineering team. On GCP, implement it using **project-per-domain** with a shared governance plane:​

**Structure:**

*   Each business domain (e.g., Sales, Logistics, Finance) owns a GCP project with their BigQuery datasets and Dataflow pipelines
    
*   Domain teams publish **data products** as authorised datasets (using BigQuery AUTHORIZED\_DATASET) accessible to other domains
    
*   A central **Data Platform team** provides shared tooling: Terraform modules, dbt project templates, CI/CD pipelines, and Cloud Data Catalog for discovery
    

**Governance:** Use a central Data Catalog taxonomy for tags (PII, SLA tier, domain owner). Implement cross-project BigQuery access via authorised datasets — consumers query the data product's view without needing project-level IAM on the producer's project. Billing is tracked per project, so domain teams see their own costs.

**Key challenge:** Avoiding duplication — use a data contract framework (Protobuf/Avro schemas registered in Pub/Sub Schema Registry) so consumers agree on the data product interface before production.

Q73. Multi-Region Disaster Recovery for BigQuery
------------------------------------------------

**Q73. How do you design DR for BigQuery with RTO and RPO targets?**

BigQuery itself is **multi-regionally replicated** within a multi-region location (e.g., US, EU) — data is stored across at least two regions with automatic failover. For stricter requirements:​

**Options by RPO/RTO:**

ApproachRPORTOCostMulti-region BigQuery datasetsNear-zeroMinutes (automatic)+~2x storageTable snapshots to secondary regionHours30–60 minLowGCS export + cross-region replicationDailyHoursVery lowCross-region dataset replica (BQ feature)MinutesMinutesMedium

**Recommended approach for critical workloads:**

1.  Use US or EU multi-region locations for BigQuery datasets
    
2.  Schedule daily table snapshots (CREATE SNAPSHOT TABLE) retained for 7 days
    
3.  Export critical tables to dual-region GCS buckets nightly as Parquet backup
    
4.  For Terraform/IaC: define the full data platform in code so it can be redeployed in a new region within hours
    
5.  Document and test the recovery runbook quarterly
    

Q74. Real-Time Fraud Detection Pipeline on GCP
----------------------------------------------

**Q74. Design a real-time fraud detection pipeline using GCP services.**

This is a classic streaming + ML integration architecture:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   textTransaction API        ↓     Pub/Sub (transactions topic)        ↓     Dataflow Streaming Pipeline     ├── Parse & validate transaction JSON     ├── Enrich with customer profile (Bigtable SideInput)     ├── Feature engineering (velocity checks, geo anomalies)     └── Call Vertex AI endpoint (online prediction)        ↓     ├── High-risk → Pub/Sub (fraud-alerts topic) → Cloud Run (block + notify)     └── Low-risk → BigQuery (transactions table, partitioned by date)        ↓     Firestore (real-time decision store for API lookups)   `

**Key design decisions:**

*   **Bigtable** for sub-millisecond customer profile lookups inside Dataflow (row key = customer\_id)
    
*   **Vertex AI online prediction endpoint** with <100ms p99 latency — call from within the Dataflow DoFn
    
*   **Firestore** stores the fraud decision so the transaction API can query "is this transaction blocked?" in real time
    
*   **BigQuery** stores all transactions + fraud scores for model retraining and analytics
    

For the ML model: train in Vertex AI using BigQuery ML feature store (point-in-time correct features), deploy as a Vertex AI endpoint, and version the endpoint so you can A/B test fraud models without pipeline changes.

Q75. Data Contract Framework with Protobuf + Schema Registry
------------------------------------------------------------

**Q75. How do you implement data contracts between producers and consumers in a GCP pipeline?**

A data contract is a formal agreement between a data producer and its consumers specifying schema, semantics, SLAs, and quality expectations. On GCP:

**Implementation:**

1.  **Schema definition**: Define schemas in Protobuf (.proto files) or Avro (.avsc files), stored in a Git repo under version control
    
2.  **Schema Registry**: Register schemas in **Pub/Sub Schema Registry** — the broker enforces schema validation on every published message, rejecting malformed data at the source
    
3.  **Contract versioning**: Use semantic versioning (v1.0.0, v1.1.0). Breaking changes (field removal, type change) require a major version bump and a deprecation notice to consumers
    
4.  **Quality SLAs**: Document in the contract: freshness SLA (data available by X time), completeness threshold (>99.5% non-null for key fields), and volume bounds (±20% of expected daily row count)
    
5.  **Enforcement in CI**: Use buf lint for Protobuf schema linting and buf breaking to detect breaking changes in PRs
    

**dbt contracts** (dbt 1.5+) enforce schema at the model level — if the dbt model changes column types or removes columns without updating the contract, the run fails. This is the most practical implementation for BigQuery-native pipelines.

Q76. Multi-Tenancy in BigQuery with Dataset-Level IAM
-----------------------------------------------------

**Q76. How do you architect a multi-tenant BigQuery platform where clients cannot access each other's data?**

**Option 1 — Dataset-per-tenant:** Each client gets a dedicated dataset (e.g., client\_acme\_prod, client\_globex\_prod). IAM bindings grant each client's service account roles/bigquery.dataViewer on only their dataset. Simple to implement, but with 100+ tenants it becomes difficult to manage.

**Option 2 — Row-level security:** All tenants share tables, with a tenant\_id column. Use BigQuery **Row Access Policies** to filter rows based on the querying user's identity:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sqlCREATE ROW ACCESS POLICY tenant_filter  ON dataset.events  GRANT TO ("serviceAccount:acme@project.iam.gserviceaccount.com")  FILTER USING (tenant_id = 'ACME');   `

**Option 3 — Authorized views per tenant:** Create a view per tenant with a hardcoded WHERE tenant\_id = 'X' filter. Authorise the view to access the base table. Grant clients access only to their view, never the base table.

**Recommended approach for consulting clients:** Use dataset-per-tenant for strong isolation + Terraform to automate provisioning. Each new client = terraform apply with a new tenant variable. Use a shared core dataset for non-tenant-specific reference data.

Q77. Data Quality SLAs with Cloud Monitoring and dbt
----------------------------------------------------

**Q77. How do you implement data quality SLAs with automated alerting?**

Define SLAs explicitly for each critical table: freshness (data must arrive by 06:00 AEST), completeness (≥99% non-null on key columns), volume (within ±20% of 30-day rolling average), and referential integrity (all foreign keys resolve). Then enforce them programmatically:

**Implementation stack:**

1.  **dbt tests** run after each pipeline completion: not\_null, unique, relationships, accepted\_values, plus custom SQL tests for business rules
    
2.  **dbt test results → BigQuery**: Use store\_failures=true to write failed rows to a dbt\_test\_failures dataset for investigation
    
3.  **Cloud Monitoring custom metrics**: After each dbt run, publish test pass/fail counts as custom metrics using the Cloud Monitoring API from a Cloud Function
    
4.  **Alerting policies**: Set up alerting policies in Cloud Monitoring that fire when dbt\_tests\_failed > 0 for severity-1 tables, routing to PagerDuty or Cloud Pub/Sub → Slack
    
5.  **SLA breach reporting**: A scheduled BigQuery query aggregates daily pass rates, surfaced in a Looker Studio SLA dashboard visible to stakeholders
    

Q78. Petabyte-Scale Joins Using Denormalisation and ARRAY
---------------------------------------------------------

**Q78. How do you handle petabyte-scale joins in BigQuery without performance degradation?**

Traditional normalised schemas require many JOINs that become expensive at petabyte scale. BigQuery's native support for **nested and repeated fields** (ARRAY\>) allows you to pre-join related entities at write time, embedding them within the parent record.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Instead of: orders JOIN order_items (separate tables, expensive join)  -- Pre-nest at ingestion time:  CREATE TABLE orders (    order_id STRING,    customer_id STRING,    order_date DATE,   `

  `line_items ARRAY    product_id STRING,      quantity INT64,      unit_price NUMERIC    >>  );  -- Query nested data efficiently (no join needed):  SELECT order_id, li.product_id, li.quantity  FROM orders, UNNEST(line_items) AS li  WHERE order_date = '2026-03-01';`

This eliminates the JOIN entirely — BigQuery reads the nested data as part of the parent row scan. For dimension lookups that cannot be pre-nested (e.g., a customer dimension accessed from many fact tables), denormalise the most frequently accessed dimension columns directly into the fact table (customer\_country, customer\_segment) to avoid runtime JOINs.

Q79. Cost Attribution with BigQuery Labels
------------------------------------------

**Q79. How do you implement cost attribution and chargeback for BigQuery usage across teams?**

Export the **GCP Billing dataset to BigQuery** (billing\_export table) and combine it with INFORMATION\_SCHEMA.JOBS for query-level attribution:​

**Labelling strategy:** Enforce labels on all BigQuery jobs at the pipeline level:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonjob_config = bigquery.QueryJobConfig(      labels={          "team": "data-engineering",          "project": "retail-analytics",          "environment": "production",          "cost-center": "cc-12345"      }  )   `

**Attribution query:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sqlSELECT    labels.value AS team,    SUM(total_bytes_billed) / POW(10,12) * 6.25 AS estimated_cost_usd,    COUNT(*) AS query_count,    DATE(creation_time) AS query_date  FROM `region-us.INFORMATION_SCHEMA.JOBS`,  UNNEST(labels) AS labels  WHERE labels.key = 'team'    AND DATE(creation_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)  GROUP BY 1, 4  ORDER BY 2 DESC;   ``

Automate label enforcement via a Cloud Build gate that rejects PRs where pipeline code lacks required labels. Publish a monthly cost report per team in Looker Studio.

Q80. Pipeline Circuit Breakers with Airflow
-------------------------------------------

**Q80. How do you implement circuit breakers in Airflow to prevent bad data from propagating?**

A circuit breaker pattern stops pipeline execution when a quality check fails, preventing corrupted data from flowing to downstream consumers. In Airflow, implement it using ShortCircuitOperator or BranchPythonOperator:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonfrom airflow.operators.python import ShortCircuitOperator  def check_row_count(**context):      client = bigquery.Client()      result = client.query("""          SELECT COUNT(*) AS cnt FROM staging.daily_events          WHERE DATE(event_date) = CURRENT_DATE()      """).result()      row_count = list(result)[0].cnt      # Circuit breaks (returns False) if row count is below threshold      return row_count >= 1_000_000  # minimum expected rows  quality_gate = ShortCircuitOperator(      task_id='quality_gate',      python_callable=check_row_count,      dag=dag  )  # Only runs if quality_gate returns True  load_to_production = BigQueryInsertJobOperator(...)  quality_gate >> load_to_production   `

When the circuit breaks (returns False), all downstream tasks are **skipped** (not failed), which prevents false alarms while stopping propagation. Combine with on\_failure\_callback to send Slack notifications when the gate triggers, and with a \_QUARANTINE table write to preserve the bad data for investigation without polluting production.

Q81. Hadoop to GCP Migration Strategy
-------------------------------------

**Q81. How do you migrate an on-premises Hadoop/Hive cluster to GCP?**

This is a 5-phase migration:​

**Phase 1 — Assessment:** Inventory all Hive tables, MapReduce/Spark jobs, and HDFS storage. Identify data volumes, job frequencies, dependencies, and SLAs. Use Google's Cloud Migration Assessment tools.

**Phase 2 — Storage migration:** Use gsutil -m rsync or **Storage Transfer Service** to copy HDFS data to GCS. Map HDFS paths to GCS paths (hdfs://cluster/data/ → gs://bucket/data/). Parquet/ORC files migrate as-is; convert text files to Parquet during migration.

**Phase 3 — Compute migration:**

*   **Hive SQL** → BigQuery (use BigQuery Migration Service for auto-translation)
    
*   **Spark jobs** → Dataflow (Beam) for complex pipelines, or Dataproc for lift-and-shift Spark
    
*   **MapReduce** → Dataflow (rewrite as Beam pipelines)
    
*   **Oozie/Azkaban** → Cloud Composer (Airflow)
    

**Phase 4 — Validation:** Run parallel for 2–4 weeks. Compare outputs using checksums and business metric reconciliation. Run regression tests for all critical jobs.

**Phase 5 — Cutover and decommission:** Migrate scheduling (crons → Composer), update data consumers' connection strings, monitor for 30 days, then decommission Hadoop cluster.

Q82. Apache Iceberg on GCS with BigQuery
----------------------------------------

**Q82. What is Apache Iceberg and how do you use it with BigQuery as a lakehouse?**

Apache Iceberg is an open **table format** that adds database-like features (ACID transactions, schema evolution, time travel, partitioning) to files stored in GCS. BigQuery Iceberg tables (GA in 2025) allow BigQuery to read and write Iceberg-format data stored in GCS natively.​

**Why Iceberg over plain Parquet:**

*   **ACID transactions**: Multiple writers can commit concurrently without conflicts
    
*   **Time travel**: Query historical snapshots (AS OF TIMESTAMP)
    
*   **Schema evolution**: Add/rename/drop columns without rewriting all files
    
*   **Partition evolution**: Change partition strategy without data migration
    
*   **Compaction**: Background service merges small files into large ones
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Create an Iceberg table in BigQuery  CREATE TABLE mydataset.events  OPTIONS (    file_format = 'PARQUET',    table_format = 'ICEBERG',    storage_uri = 'gs://my-bucket/iceberg/events'  );   `

**Use case**: Use Iceberg as the Silver/Gold layer of your data lake when you need cross-engine compatibility — the same Iceberg table can be read by BigQuery, Spark on Dataproc, and Flink, enabling a true open lakehouse without vendor lock-in.

Q83. Pipeline Observability with OpenTelemetry + Cloud Trace
------------------------------------------------------------

**Q83. How do you implement end-to-end observability for data pipelines on GCP?**

Observability goes beyond logging — it means correlating **traces** (what happened), **metrics** (how fast/how many), and **logs** (what went wrong) into a unified view.

**Implementation:**

1.  **Traces**: Instrument Python pipeline code with OpenTelemetry SDK. Each pipeline run gets a root trace\_id. Child spans cover each stage (read, transform, write). Export to Cloud Trace using opentelemetry-exporter-gcp-trace
    
2.  **Metrics**: Publish custom metrics (records processed, error rate, latency per stage) to Cloud Monitoring using the google-cloud-monitoring Python client
    
3.  **Logs**: Use structured JSON logging ({"severity": "INFO", "trace": "...", "pipeline": "...", "records\_processed": 1000}) which Cloud Logging auto-parses. Correlate with traces via the trace field
    
4.  **Dashboards**: Build a Cloud Monitoring dashboard showing pipeline health across all jobs. Use log-based metrics to count ERROR log entries per pipeline per day
    
5.  **Alerting**: Alert on error\_rate > 1%, pipeline\_duration > 2x SLA, or records\_processed < min\_expected
    

The key insight is passing the trace\_id through every stage and into the Airflow task logs, so when an incident occurs you can follow a single trace from source ingest through to BigQuery load.

Q84. GDPR Right-to-Erasure Using Crypto-Shredding
-------------------------------------------------

**Q84. How do you implement GDPR right-to-erasure in BigQuery when you cannot delete individual rows efficiently?**

BigQuery DML DELETE is expensive (full table scan) and doesn't work on streaming tables. The elegant solution is **crypto-shredding**:

**How it works:**

1.  At ingest time, encrypt all PII fields for each user with a **per-user encryption key** stored in Cloud KMS (or a Key Management table in Cloud SQL)
    
2.  Store only the **encrypted PII** values in BigQuery, never plaintext
    
3.  When a GDPR erasure request arrives, **delete the user's encryption key** from Cloud KMS
    
4.  All encrypted PII in BigQuery is now **cryptographically unreadable** — effectively erased without touching BigQuery data
    
5.  Optionally, run a periodic background job to physically NULL out columns where keys have been deleted
    

**Implementation:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# At ingest: encrypt before writing to BigQuery  from google.cloud import kms  def encrypt_pii(user_id: str, plaintext: str) -> str:      key_name = f"projects/.../cryptoKeyVersions/users/{user_id}/latest"      ciphertext = kms_client.encrypt(name=key_name, plaintext=plaintext.encode())      return base64.b64encode(ciphertext.ciphertext).decode()  # On erasure request: delete the key version  kms_client.destroy_crypto_key_version(name=f".../{user_id}/latest")   `

This approach scales to billions of records without any BigQuery writes during erasure, which is critical for high-volume consumer platforms.

Q85. Feature Store on GCP with Vertex AI
----------------------------------------

**Q85. How do you design a feature store for ML pipelines on GCP?**

A feature store provides **consistent, reusable, point-in-time correct features** for both model training (batch) and serving (online). On GCP, Vertex AI Feature Store is the managed solution:

**Architecture:**

*   **Offline store** (training): BigQuery tables containing historical feature values with timestamps
    
*   **Online store** (serving): Bigtable-backed low-latency serving (~10ms p99) for real-time inference
    
*   **Feature pipeline**: Dataflow or Dataproc job computes features from raw events and writes to BigQuery. Vertex AI Feature Store syncs from BigQuery to Bigtable on a schedule
    

**Point-in-time correctness:** When creating training datasets, use entityRows with historical timestamps — the feature store returns the feature values that were available AT that timestamp, preventing data leakage (using future data to train on past events).

**Feature versioning:** Register features with metadata (description, owner, data type, freshness SLA). Consumers discover features via the Feature Store registry API, preventing feature duplication across teams — a data mesh principle applied to ML.

Q86. Schema Registry with Pub/Sub and Avro/Protobuf
---------------------------------------------------

**Q86. How do you implement schema validation and versioning for Pub/Sub messages?**

Pub/Sub Schema Registry (GA since 2022) enforces schema compliance at the **broker level** — messages that don't conform to the registered schema are rejected before they reach consumers:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Register an Avro schema  gcloud pubsub schemas create user-events \    --type=AVRO \    --definition='{      "type": "record",      "name": "UserEvent",      "fields": [        {"name": "user_id", "type": "string"},        {"name": "event_type", "type": "string"},        {"name": "timestamp", "type": "long"}      ]    }'  # Attach schema to topic  gcloud pubsub topics create user-events-topic \    --schema=user-events \    --message-encoding=JSON   `

**Schema evolution rules:**

*   **Backward compatible** (safe): Add optional fields with defaults
    
*   **Forward compatible** (safe): Remove optional fields
    
*   **Breaking** (requires new topic + migration): Remove required fields, change types, rename fields
    

Use Protobuf over Avro when you need cross-language clients (Java microservices + Python data pipelines). Avro is better for pure Python/data-engineering workflows due to simpler tooling.

Q87. Self-Service Analytics with Data Catalog + Authorized Views
----------------------------------------------------------------

**Q87. How do you build a self-service analytics platform on GCP that maintains governance?**

The goal is enabling business analysts to discover and query data independently without data engineers as gatekeepers, while maintaining access control and quality standards:

**Components:**

1.  **Data Catalog**: Register all BigQuery tables with descriptions, column definitions, PII tags, and data owner contacts. Enable business users to search "what data exists about customer transactions?"
    
2.  **Authorized views (presentation layer)**: Create curated, business-friendly views that abstract raw table complexity. Name them in business terms (marketing.daily\_campaign\_performance not dw\_tbl\_cmpgn\_v2\_tmp)
    
3.  **IAM by role**: roles/bigquery.dataViewer on specific datasets per team. Analysts cannot access raw/Bronze data — only Silver and Gold layers
    
4.  **Column-level security**: Apply policy tags to sensitive columns. Analysts see NULLs for PII they're not authorised to view, without impacting their ability to run aggregations
    
5.  **Query cost governance**: Set per-user custom quotas via BigQuery IAM conditions. Dashboard showing each analyst's monthly spend
    
6.  **dbt docs**: Publish dbt documentation as a searchable data dictionary showing model lineage, column descriptions, and test results
    

Q88. BigQuery Time Travel and Table Snapshots
---------------------------------------------

**Q88. How do you use BigQuery time travel and snapshots for data recovery and auditing?**

BigQuery retains historical table states for **up to 7 days** (configurable via --time\_travel\_days). This enables querying past states and recovering from accidental mutations:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Query table as it was 24 hours ago (time travel)  SELECT * FROM `project.dataset.orders`  FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR);  -- Restore a table after accidental deletion/update  CREATE OR REPLACE TABLE dataset.orders AS  SELECT * FROM `project.dataset.orders`  FOR SYSTEM_TIME AS OF '2026-03-19 10:00:00 UTC';   ``

**Table snapshots** (distinct from time travel) are **point-in-time copies** stored as zero-copy references — they consume no storage until the base table changes (copy-on-write). Use them for:

*   Pre-deployment snapshots before running a risky migration
    
*   Month-end regulatory reporting (immutable snapshot of the reporting period data)
    
*   Cross-region DR (copy snapshot to a secondary region dataset)
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sqlCREATE SNAPSHOT TABLE dataset.orders_snapshot_20260320  CLONE dataset.orders  OPTIONS (expiration_timestamp = TIMESTAMP '2026-04-20 00:00:00 UTC');   `

Q89–Q100: Remaining Advanced Architecture (Detailed Summaries)
--------------------------------------------------------------

**Q89. Fan-out patterns in Pub/Sub:**One topic → multiple subscriptions, each with independent delivery and acknowledgement state. Create separate subscriptions for each consumer (Dataflow pipeline, Cloud Function, BigQuery subscription). Each consumer processes at its own pace; the topic retains messages until all subscriptions acknowledge. Use **topic filtering** on subscriptions to route only relevant message subsets to each consumer (e.g., subscription A only receives event\_type=purchase).

**Q90. Cross-project BigQuery access — Authorized Datasets vs. Authorized Views:**Authorised **views** grant a single view access to another dataset's tables; authorised **datasets** grant all views within a dataset access to another dataset. Use authorised datasets for data mesh architectures where an entire domain's presentation layer needs to read from a shared core dataset — avoids registering each view individually. Authorised views are preferable when only specific, curated views should access sensitive source data.

**Q91. Data SLA monitoring with INFORMATION\_SCHEMA:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Alert if any critical table hasn't received data in 2+ hours  SELECT table_id, TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_modified_time, HOUR) AS hours_stale  FROM `project.dataset.INFORMATION_SCHEMA.TABLE_STORAGE`  WHERE table_id IN ('orders', 'inventory', 'transactions')    AND TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_modified_time, HOUR) > 2;   ``

Schedule this query via Cloud Scheduler → Cloud Function → publish metric to Cloud Monitoring → alerting policy fires if any row returned.

**Q92. Incremental load using \_PARTITIONTIME:**Use BigQuery's \_PARTITIONTIME (for ingestion-time partitioned tables) or a custom event\_date partition column to load only new data. Store the high-watermark (max(event\_date) successfully loaded) in a Cloud SQL metadata table or Airflow Variable. Each pipeline run queries: WHERE event\_date > last\_watermark AND event\_date <= CURRENT\_DATE().

**Q93. Querying nested JSON with variable schema:**Use JSON\_VALUE(col, '$.field') for scalar extraction, JSON\_QUERY(col, '$.nested') for sub-objects, and JSON\_EXTRACT\_ARRAY(col, '$.items') + UNNEST for arrays. For truly schema-less JSON, store raw JSON as a JSON native type column (BigQuery GA 2023) and use LAX JSON path expressions that return NULL rather than erroring on missing keys.

**Q94. Pipeline idempotency with GCS marker files + Airflow sensors:**Write a \_SUCCESS marker file to GCS upon successful pipeline completion: gs://bucket/pipeline/date=2026-03-20/\_SUCCESS. In downstream DAGs, use GCSObjectExistenceSensor to wait for this marker before proceeding. This creates a loosely coupled dependency between pipelines without shared databases. If a pipeline reruns, it checks for the marker first and skips if already present.

**Q95. Event-driven orchestration with Eventarc + Cloud Run:**Configure an Eventarc trigger on GCS google.cloud.storage.object.v1.finalized events for a specific bucket/prefix. The trigger invokes a Cloud Run service that validates the file, registers metadata in Data Catalog, and uses the Dataflow API to launch a FlexTemplate job programmatically. This replaces time-based polling (Airflow sensors) with true event-driven instantaneous triggering — a better pattern for latency-sensitive data ingestion.

**Q96. Cross-region BigQuery dataset replicas:**Use BigQuery's **dataset replication** feature to maintain a read replica of a dataset in a secondary region. Configure via bq mk --dataset --replication\_config pointing to a source dataset. The replica stays in sync within minutes. Use for: (1) read-heavy analytics teams in a different region to avoid cross-region egress, (2) DR failover — promote the replica to primary if the source region fails. Note: replicas are read-only; writes must go to the primary.

**Q97. Automated PII tagging with DLP + Data Catalog:**Trigger Cloud DLP inspection jobs on new BigQuery tables via an Eventarc trigger on the Data Catalog TableCreated event → Cloud Function → DLP InspectContentRequest on a table sample → parse DLP findings (email, phone, SSN, etc.) → write policy tags to Data Catalog columns via the BigQuery Policy Tag API. This automates PII governance for every new table ingested, without manual review, and enforces column-level security automatically.

**Q98. Pub/Sub flow control for slow consumers:**Configure flow control on the subscriber client to prevent memory overflow:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonflow_control = pubsub_v1.types.FlowControl(      max_messages=100,           # max in-flight messages      max_bytes=10 * 1024 * 1024  # max 10MB in-flight  )  subscriber.subscribe(subscription_path, callback=callback,                       flow_control=flow_control)   `

The client will stop pulling new messages when limits are hit, applying natural backpressure. Also set ack\_deadline\_seconds high enough for your processing time — if processing takes 60s, set ack deadline to 120s to prevent redelivery of in-progress messages.

**Q99. BigQuery authorised views for multi-project data sharing:**Data owners grant a view (in a consumer project) access to source tables (in a producer project) via authorised views — no data is copied, no direct IAM on source tables is granted to consumers. This is the canonical pattern for cross-project data sharing: the producer controls access at the view level, consumers get SQL access without ever seeing raw data. Use this for selling data products externally or for inter-domain access in a data mesh.

**Q100. Ideal greenfield GCP data platform stack (2026):**

LayerTechnologyRationaleIngestion (streaming)Pub/Sub + Dataflow (Beam)Unified batch/streaming, auto-scaleIngestion (batch/CDC)Datastream + Cloud Storage TransferManaged CDC, minimal source impactStorageGCS (Parquet/Iceberg)Open format, lakehouse-readyTransformationdbt + BigQuerySQL-native, version-controlled, testedOrchestrationCloud Composer 3 (Airflow)GCP-native, deferrable operatorsServingBigQuery + BI EnginePetabyte-scale SQL + sub-second dashboardsML FeaturesVertex AI Feature StoreOnline/offline consistencyGovernanceData Catalog + DLP + Policy TagsAutomated PII tagging, lineageObservabilityCloud Monitoring + OpenTelemetry + dbt testsFull pipeline observabilityIaC/CI-CDTerraform + Cloud Build + GitHub ActionsGitOps-first deployments

This stack is **open** (Iceberg, Parquet, Protobuf), **governed** (DLP, Policy Tags, Data Catalog), **tested** (dbt contracts + Great Expectations), and **observable** (OpenTelemetry end-to-end) — aligned with enterprise requirements and Mantel Group's delivery standards.

🟡 100 Medium Technical Questions
=================================

BigQuery (Intermediate)
-----------------------

**Q1. What is the difference between ARRAY and STRUCT in BigQuery?**STRUCT is a container of named fields (like a row within a row). ARRAY is an ordered list of elements of the same type. Combined as ARRAY\>, they enable repeated nested records — useful for order line items within an order record, avoiding JOINs entirely.​

**Q2. How do you perform incremental loads in BigQuery?**Use partitioned tables with a load\_date or event timestamp partition. On each pipeline run, query only new records from the source (using a high-watermark stored in a metadata table or Airflow variable), then use MERGE to upsert into the target table.

**Q3. What is the purpose of BigQuery's MERGE statement?**MERGE performs upsert logic: INSERT new rows, UPDATE existing rows, and optionally DELETE rows in one atomic DML statement. It's the standard pattern for SCD Type 2 updates and incremental pipeline loads.

**Q4. How do you export BigQuery results to GCS?**Use EXPORT DATA OPTIONS (uri='gs://bucket/file\_\*.csv', format='CSV') in SQL, or the BigQuery API's extract job. Use wildcards for sharded output. Parquet or Avro formats are preferred for downstream processing pipelines.

**Q5. What are authorized views and why are they useful?**Authorized views allow a view in one dataset to access tables in another dataset without granting the end-user direct access to the source tables. This enables row/column-level filtering at the presentation layer while keeping raw data secure.

Q6. CTEs vs. Subqueries in BigQuery
-----------------------------------

**Q6. What is the difference between a CTE (WITH clause) and a subquery in BigQuery, and does a CTE improve performance?**

A **CTE (Common Table Expression)** is a named temporary result set defined using the WITH keyword, while a subquery is an inline SELECT nested inside another query.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- CTE: readable, reusable within the same query  WITH daily_sales AS (    SELECT DATE(order_time) AS sale_date, SUM(amount) AS total    FROM orders    GROUP BY 1  )  SELECT sale_date, total  FROM daily_sales  WHERE total > 10000;  -- Equivalent subquery (harder to read)  SELECT sale_date, total  FROM (    SELECT DATE(order_time) AS sale_date, SUM(amount) AS total    FROM orders    GROUP BY 1  ) WHERE total > 10000;   `

**Critical point for BigQuery**: Unlike some databases, **BigQuery does NOT materialise CTEs** — they are inlined at execution time, meaning a CTE referenced twice is executed twice. If you need true materialisation, write the intermediate result to a temp table or use a materialised view. CTEs improve **readability and maintainability**, not performance. For complex pipelines, use dbt models which write intermediate results to actual BigQuery tables.

Q7. How to Use UNNEST() to Query Arrays
---------------------------------------

**Q7. How does UNNEST() work in BigQuery and when do you use it?**

UNNEST() converts an ARRAY into a set of rows — it "flattens" the array so each element becomes its own row. It's essential for querying nested repeated fields, particularly in GA4/Firebase event data.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Table with nested line_items array  SELECT    order_id,    li.product_id,    li.quantity,    li.unit_price  FROM orders,  UNNEST(line_items) AS li   -- each element in the array becomes a row  WHERE li.quantity > 1;  -- UNNEST with OFFSET to preserve array index position  SELECT    order_id,    li,    idx  FROM orders,  UNNEST(line_items) AS li WITH OFFSET idx  ORDER BY order_id, idx;   `

Use UNNEST() when you need to **filter, aggregate, or join** on array elements. When you only need scalar values from an array without exploding rows, use ARRAY\_AGG, ARRAY\_LENGTH, or dot notation on STRUCT fields instead. Over-using UNNEST on large arrays can dramatically increase row counts — always pre-filter the parent table before unnesting.​

Q8. What Is a Wildcard Table?
-----------------------------

**Q8. What are BigQuery wildcard tables and when do you use them?**

Wildcard tables let you query multiple similarly named tables using a \* suffix pattern — a common pattern for date-sharded tables (a legacy partitioning method).

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Query all tables matching the pattern events_2026*  SELECT event_name, COUNT(*) AS cnt  FROM `project.dataset.events_2026*`  WHERE _TABLE_SUFFIX BETWEEN '0301' AND '0320'   -- filter specific date range  GROUP BY 1;   ``

**\_TABLE\_SUFFIX** is a pseudo-column containing the matched portion of the table name, used to filter which tables are actually scanned. Without a \_TABLE\_SUFFIX filter, BigQuery scans ALL matching tables — potentially very expensive.​

**When to use:** Date-sharded legacy tables (e.g., Google Analytics Universal export format like ga\_sessions\_YYYYMMDD). **When NOT to use:** For new table designs, use native partitioned tables instead — they are more efficient, cheaper to maintain, and support partition pruning without pseudo-column filtering.​

Q9. How to Schedule SQL Queries in BigQuery
-------------------------------------------

**Q9. What are the options for scheduling recurring SQL queries in BigQuery?**

BigQuery offers two native options, plus orchestration via Composer:

**Option 1 — BigQuery Scheduled Queries (native):**

*   Configure directly in BigQuery Console or via bq CLI
    
*   Runs on a cron schedule (e.g., daily at midnight)
    
*   Results append to or overwrite a destination table
    
*   Limited error handling, no complex dependencies
    

**Option 2 — Cloud Scheduler + Cloud Functions:**

*   Cloud Scheduler triggers a Cloud Function on a cron schedule
    
*   Cloud Function calls the BigQuery Jobs API to run a query
    
*   Suitable for lightweight, isolated jobs
    

**Option 3 — Cloud Composer (Airflow) — recommended for production:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonfrom airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator  run_query = BigQueryInsertJobOperator(      task_id='run_daily_aggregation',      configuration={          "query": {              "query": "SELECT ...",              "destinationTable": {"projectId": "...", "datasetId": "...", "tableId": "..."},              "writeDisposition": "WRITE_TRUNCATE",              "useLegacySql": False          }      }  )   `

Composer is preferred for anything with dependencies, error handling, retries, or multi-step pipelines.​

Q10. What Is the QUALIFY Clause?
--------------------------------

**Q10. What does the QUALIFY clause do in BigQuery and why is it useful?**

QUALIFY filters the results of a **window function** without requiring a subquery or CTE wrapper. It is applied after WINDOW function evaluation — analogous to HAVING for aggregate functions.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Without QUALIFY: needs a subquery  SELECT * FROM (    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time DESC) AS rn    FROM events  ) WHERE rn = 1;  -- With QUALIFY: much cleaner, same result  SELECT *  FROM events  QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time DESC) = 1;   `

This is particularly useful for **deduplication** (keep only the latest row per key), **top-N per group** queries, and **filtering to the first/last event per user/session**. BigQuery supports QUALIFY natively; not all SQL dialects do (check compatibility if using dbt or sqlfluff linting).

Q11. Handling NULL Values in BigQuery Aggregations
--------------------------------------------------

**Q11. How does BigQuery handle NULLs in aggregation functions and how do you control this behaviour?**

BigQuery (following SQL standard) **ignores NULL values** in aggregate functions like SUM, AVG, COUNT(col), MAX, MIN. COUNT(\*) counts all rows including NULLs; COUNT(col) counts only non-NULL values.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- NULL behaviour examples  SELECT    COUNT(*) AS total_rows,           -- counts all rows, including NULLs    COUNT(revenue) AS non_null_rows,  -- excludes NULL revenue rows    SUM(revenue) AS total_revenue,    -- NULLs ignored, not treated as 0    AVG(revenue) AS avg_revenue,      -- average of non-NULL values only    COALESCE(SUM(revenue), 0) AS safe_sum,   -- replace NULL result with 0    IFNULL(revenue, 0) AS revenue_cleaned    -- replace NULL input with 0  FROM transactions;   `

**Common pitfalls:**

*   SUM(revenue) returns NULL if ALL rows have NULL revenue — wrap in COALESCE(SUM(revenue), 0) for safe totals
    
*   AVG() can be misleading if NULLs represent "zero" in your business logic — explicitly COALESCE(col, 0) before averaging
    
*   GROUP BY treats NULL as its own group — two rows with NULL in the group key are grouped together
    

Q12. What Is TABLESAMPLE?
-------------------------

**Q12. What is TABLESAMPLE in BigQuery and when should you use it?**

TABLESAMPLE returns a random sample of a table, scanning only a fraction of the data — dramatically reducing cost for exploratory analysis on large tables.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Sample approximately 1% of the events table  SELECT *  FROM `project.dataset.events`  TABLESAMPLE SYSTEM (1 PERCENT);  -- Useful for quick profiling on a 10TB table  SELECT    event_type,    COUNT(*) AS sample_count  FROM `project.dataset.events`  TABLESAMPLE SYSTEM (0.1 PERCENT)  GROUP BY 1;   ``

**Important caveats:**

*   Results are **not deterministic** — rerunning returns a different random sample
    
*   The sample percentage is approximate, not exact
    
*   TABLESAMPLE SYSTEM samples at the storage block level, not row level — fast but less uniform than row-level sampling
    
*   For **reproducible sampling**, use a deterministic hash filter instead: WHERE MOD(FARM\_FINGERPRINT(user\_id), 100) < 1 (deterministic 1% sample)
    

Q13. BigQuery ML: In-Warehouse Predictions
------------------------------------------

**Q13. How does BigQuery ML work and what model types does it support?**

BigQuery ML (BQML) allows you to **train, evaluate, and score ML models directly in BigQuery using SQL**, without moving data to a separate ML platform.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Step 1: Train a logistic regression model  CREATE OR REPLACE MODEL `dataset.churn_model`  OPTIONS (model_type='LOGISTIC_REG', input_label_cols=['churned']) AS  SELECT age, tenure_days, monthly_spend, churned  FROM `dataset.customer_features`  WHERE DATE(snapshot_date) < '2026-01-01';  -- Step 2: Evaluate  SELECT * FROM ML.EVALUATE(MODEL `dataset.churn_model`);  -- Step 3: Predict  SELECT customer_id, predicted_churned, predicted_churned_probs  FROM ML.PREDICT(MODEL `dataset.churn_model`,    (SELECT * FROM `dataset.customer_features`     WHERE DATE(snapshot_date) = CURRENT_DATE()));   ``

**Supported model types**: Linear/Logistic Regression, K-Means clustering, Matrix Factorisation, Time Series forecasting (ARIMA+), XGBoost, Deep Neural Networks, Imported TensorFlow/ONNX models, and remote Vertex AI models. BQML is ideal for **feature engineering → model training → batch scoring** within a single BigQuery context, keeping data transfer costs to zero.

Q14. BigQuery Dataset vs. Project vs. Table Hierarchy
-----------------------------------------------------

**Q14. Explain the BigQuery resource hierarchy and its implications for IAM and billing.**

BigQuery follows a three-level hierarchy nested within GCP's resource hierarchy:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   textGCP Organisation    └── GCP Project (billing unit, IAM boundary)          └── BigQuery Dataset (access control unit, regional location)                └── BigQuery Table / View / Model / Routine   `

**Key implications:**

*   **Billing** is at the **project** level — all query costs and storage costs roll up to the project's billing account. Use project-level labels and INFORMATION\_SCHEMA to attribute costs to teams
    
*   **IAM** can be applied at project level (broad), dataset level (recommended), or table level (granular). Dataset-level IAM is the standard governance boundary
    
*   **Location is set at the dataset level** and is immutable after creation — cross-region queries are not possible natively (you must copy data). Always choose your region carefully at dataset creation time
    
*   **Cross-project queries** are allowed: SELECT \* FROM project2.dataset.table — but the querying project is billed, not the source project
    

Q15. Monitor Slot Usage in Real Time
------------------------------------

**Q15. How do you monitor BigQuery slot utilisation to detect bottlenecks?**

Use INFORMATION\_SCHEMA views for query-level analysis and Cloud Monitoring for real-time slot dashboards:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Top 10 most slot-intensive jobs in the last 24 hours  SELECT    job_id,    user_email,    query,    total_slot_ms,    total_bytes_billed,    TIMESTAMP_DIFF(end_time, start_time, SECOND) AS duration_seconds  FROM `region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`  WHERE DATE(creation_time) = CURRENT_DATE()    AND job_type = 'QUERY'  ORDER BY total_slot_ms DESC  LIMIT 10;  -- Real-time slot utilisation (rolling 1-min average)  SELECT    TIMESTAMP_TRUNC(start_time, MINUTE) AS minute,    SUM(total_slot_ms) / 60000 AS avg_slots_used  FROM `region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`  WHERE start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)  GROUP BY 1  ORDER BY 1 DESC;   ``

For **real-time monitoring**, use the Cloud Monitoring metric bigquery.googleapis.com/project/slots/allocated\_for\_project. Build a dashboard showing peak slot usage vs. reservation capacity, and set alerts when utilisation exceeds 80% for more than 5 minutes.

Q16. DATE vs. DATETIME vs. TIMESTAMP in BigQuery
------------------------------------------------

**Q16. What is the difference between DATE, DATETIME, and TIMESTAMP in BigQuery?**

TypeStoresTimezone Aware?ExampleDATECalendar date onlyNo2026-03-20DATETIMEDate + time, no timezoneNo2026-03-20T22:00:00TIMESTAMPAbsolute point in time (UTC)Yes (UTC internally)2026-03-20T11:00:00Z

**When to use each:**

*   **DATE**: Business dates (report date, birth date, partition column)
    
*   **DATETIME**: Local time representation where timezone is implicit (e.g., store operating hours)
    
*   **TIMESTAMP**: Event times, log times, any absolute moment — **always preferred for pipeline data** as it unambiguously represents a point in time regardless of where it was generated
    

**Common conversion functions:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sqlCURRENT_TIMESTAMP()                          -- current UTC timestamp  CURRENT_DATE('Australia/Melbourne')          -- today in Melbourne timezone  TIMESTAMP_TRUNC(ts, HOUR)                   -- truncate to hour boundary  FORMAT_TIMESTAMP('%Y-%m-%d', ts, 'Australia/Melbourne')  -- format in local tz  DATETIME(ts, 'Australia/Melbourne')          -- convert UTC timestamp to local datetime   `

Q17. Streaming Buffer vs. Managed Storage
-----------------------------------------

**Q17. What is the BigQuery streaming buffer and how does it differ from managed storage?**

When data is written via **Legacy Streaming Inserts** (tabledata.insertAll), rows land in a **streaming buffer** — a temporary in-memory/SSD storage layer that is immediately queryable but not yet written to Capacitor (BigQuery's columnar storage format). Buffer data is flushed to managed storage within 90 minutes to a few hours.

**Implications:**

*   Streaming buffer rows **cannot be modified by DML** (UPDATE/DELETE) until they are flushed to managed storage
    
*   Streaming buffer data **does not benefit from partitioning/clustering** until flushed
    
*   Streaming buffer has a **separate, higher storage cost** (~$0.01/GB/month vs $0.02/GB/month for active storage — but cannot use long-term pricing)
    
*   Use INFORMATION\_SCHEMA.TABLE\_STORAGE to check active\_logical\_bytes vs long\_term\_logical\_bytes
    

**Modern recommendation**: Use the **BigQuery Storage Write API** (GA since 2022) instead of legacy streaming inserts. It offers committed, buffered, and pending write modes, supports exactly-once semantics, and is both cheaper and more reliable than legacy streaming.​

Q18. Copying Tables Across Projects and Regions
-----------------------------------------------

**Q18. How do you copy BigQuery tables across projects and regions?**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Same region, different project (instant, no data movement)  bq cp source_project:dataset.table dest_project:dataset.table  # Cross-region: requires export → transfer → import  # Step 1: Export to GCS in source region  bq extract --destination_format=PARQUET \    source_project:dataset.table \    gs://source-bucket/export/*.parquet  # Step 2: Use GCS Transfer Service to copy bucket to destination region  # Step 3: Load from destination region GCS to BigQuery  bq load --source_format=PARQUET \    dest_project:dataset.table \    gs://dest-bucket/export/*.parquet   `

**BigQuery Data Transfer Service** can automate cross-project copies within the same region on a schedule. For cross-region copies, there is **no direct native method** — always go through GCS, incurring egress costs. As of 2025, BigQuery dataset replication (GA) can continuously replicate a dataset to another region, which is the preferred DR mechanism over manual copy workflows.

Q19. GENERATE\_ARRAY for Date Spines
------------------------------------

**Q19. How do you use GENERATE\_ARRAY for creating a date spine in BigQuery?**

A **date spine** is a complete sequence of dates with no gaps — essential in dbt models and analytics queries to ensure zero-filled metrics on days with no events.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Generate a complete date sequence  SELECT date_val  FROM UNNEST(    GENERATE_DATE_ARRAY('2026-01-01', CURRENT_DATE(), INTERVAL 1 DAY)  ) AS date_val;  -- Use in a LEFT JOIN to ensure all dates appear in the result  WITH date_spine AS (    SELECT date_val    FROM UNNEST(GENERATE_DATE_ARRAY('2026-01-01', CURRENT_DATE(), INTERVAL 1 DAY)) AS date_val  )  SELECT    ds.date_val,    COALESCE(s.total_sales, 0) AS total_sales  FROM date_spine ds  LEFT JOIN daily_sales s ON ds.date_val = s.sale_date  ORDER BY 1;   `

Use GENERATE\_ARRAY (for integers) when you need numeric sequences, and GENERATE\_DATE\_ARRAY for date sequences. In dbt, use the dbt\_utils.date\_spine macro which wraps this pattern and handles edge cases.

Q20. Nested and Repeated Data in BigQuery
-----------------------------------------

**Q20. How does BigQuery store nested and repeated data, and what are the storage benefits?**

BigQuery stores nested (STRUCT) and repeated (ARRAY) fields using a variant of the **Dremel columnar encoding** that preserves hierarchical structure while maintaining columnar storage benefits.​

Instead of flattening a parent-child relationship into two tables (requiring a JOIN), BigQuery stores the entire record in one physical location with the child records encoded as repeated columns. This means:

*   **No JOIN required** to access nested data — reads are co-located
    
*   Repeated fields are stored contiguously per parent record
    
*   Columnar compression still applies to each field within the struct
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Schema with nested repeated data  CREATE TABLE orders (    order_id STRING,    customer STRUCT<      id STRING,      name STRING,      city STRING    >,   `

  `items ARRAY    sku STRING,      qty INT64,      price NUMERIC    >>  );  -- Query nested scalar  SELECT order_id, customer.city FROM orders;  -- Query repeated struct  SELECT order_id, item.sku, item.qty  FROM orders, UNNEST(items) AS item;`

Q21. DML vs. DDL Cost Implications in BigQuery
----------------------------------------------

**Q21. What is the difference between DML and DDL in BigQuery and what are their cost implications?**

**DDL (Data Definition Language):** CREATE, ALTER, DROP — operations that define structure. Most DDL in BigQuery (creating/dropping tables, views, datasets) is **free** and instantaneous.​

**DML (Data Manipulation Language):** INSERT, UPDATE, DELETE, MERGE — operations that modify data. DML statements in BigQuery **scan the full table** (or relevant partitions) because BigQuery doesn't have row-level indexing. Each DML operation rewrites affected partitions.

**Cost model:**

*   DML is charged on **bytes processed** like SELECT queries
    
*   UPDATE/DELETE on a 1TB table that modifies 1 row still scans (and rewrites) the entire affected partition
    
*   MERGE is most efficient — combine UPDATE + INSERT into one pass; it also qualifies for partition pruning if your merge condition includes the partition column
    
*   **Best practice**: Minimise DML frequency. Batch your updates. Use MERGE over separate UPDATE + INSERT operations. Always include partition filter in DML WHERE clauses.
    

Q22. Soft Deletes in BigQuery
-----------------------------

**Q22. How do you implement soft deletes in BigQuery and why?**

BigQuery is optimised for **append-only** patterns. Running DELETE on rows is expensive (full partition scan + rewrite). Soft deletes flag records as deleted without physically removing them:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Add is_deleted flag to the table  ALTER TABLE dataset.customers  ADD COLUMN IF NOT EXISTS is_deleted BOOL DEFAULT FALSE,  ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;  -- Soft delete: MERGE to set flag  MERGE dataset.customers AS target  USING (SELECT 'cust_123' AS id) AS source  ON target.customer_id = source.id  WHEN MATCHED THEN    UPDATE SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP();  -- Query active records via a view (hides deleted rows)  CREATE OR REPLACE VIEW dataset.active_customers AS  SELECT * EXCEPT(is_deleted, deleted_at)  FROM dataset.customers  WHERE NOT is_deleted;   `

**Why soft deletes:** Preserve audit trail, support GDPR right-to-erasure investigations before hard deletion, enable replay/recovery if deletion was accidental. Schedule periodic hard-delete jobs to physically remove flagged records during low-traffic windows and manage storage costs.

Q23. BigQuery Jobs and Job History
----------------------------------

**Q23. What is a BigQuery job and how do you track and analyse job history?**

A BigQuery **job** is any asynchronous operation: query execution, data load, export, or copy. Every job has a unique job\_id, status (DONE, RUNNING, PENDING), and resource usage metadata.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Query job history via INFORMATION_SCHEMA  SELECT    job_id,    creation_time,    user_email,    state,    error_result.reason AS error_reason,    total_bytes_billed,    total_slot_ms,    SUBSTR(query, 1, 200) AS query_preview  FROM `region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`  WHERE DATE(creation_time) = CURRENT_DATE()    AND state = 'DONE'    AND error_result IS NOT NULL   -- failed jobs only  ORDER BY creation_time DESC;   ``

Use the bq CLI for programmatic access: bq show --job --format=prettyjson job\_id. In Airflow, the BigQueryInsertJobOperator automatically captures the job\_id as an XCom value for downstream logging. Always log job\_id in your pipeline monitoring tables — it enables direct drill-down from a pipeline alert to the exact BigQuery job that failed.

Q24. BigQuery with Looker/Looker Studio
---------------------------------------

**Q24. How do you optimise BigQuery for use with Looker Studio or Looker dashboards?**

BI tools generate repetitive, often sub-optimal SQL queries. Without tuning, each dashboard refresh can trigger expensive BigQuery scans:​

**Optimisation layers:**

1.  **BI Engine reservation**: Purchase a BI Engine reservation (e.g., 1GB–10GB) in the same region as your dataset. Eligible dashboard queries are served from memory, delivering sub-second response and zero additional bytes billed
    
2.  **Materialised views**: Pre-aggregate common dashboard queries (daily totals, weekly cohorts) as materialised views — Looker Studio queries the materialised result, not the base table
    
3.  **Clustering**: Cluster dashboard tables on the columns most frequently used in filters (e.g., region, product\_category, date)
    
4.  **Looker PDTs (Persistent Derived Tables)**: In Looker, define PDTs that run nightly to pre-build complex joins and aggregations, so dashboard queries hit small pre-built tables
    
5.  **Authorised views**: Expose only the columns and rows relevant to each Looker Studio report to minimize bytes scanned per query
    

Q25. Handling Encoding Issues in CSV Imports
--------------------------------------------

**Q25. How do you handle character encoding issues when loading CSV files into BigQuery?**

BigQuery expects **UTF-8** encoding by default. Files with Latin-1, Windows-1252, or other encodings cause load errors or silent data corruption:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Specify encoding during load  bq load \    --source_format=CSV \    --encoding=ISO-8859-1 \    --skip_leading_rows=1 \    dataset.table \    gs://bucket/file.csv \    schema.json   `

**Supported encodings**: UTF-8 (default), ISO-8859-1 (Latin-1), UTF-16BE, UTF-16LE. For other encodings, **pre-process with Python** using iconv or Python's chardet library before loading:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonimport chardet  with open('data.csv', 'rb') as f:      detected = chardet.detect(f.read())      print(detected['encoding'])  # e.g., 'windows-1252'  # Re-encode to UTF-8  with open('data.csv', encoding='windows-1252') as f_in:      with open('data_utf8.csv', 'w', encoding='utf-8') as f_out:          f_out.write(f_in.read())   `

In Dataflow pipelines, always explicitly declare encoding when reading CSV files using ReadFromText(file\_pattern, encoding='utf-8') to fail fast rather than silently corrupting data.

Q26. BigQuery Omni
------------------

**Q26. What is BigQuery Omni and when is it relevant in a multi-cloud strategy?**

BigQuery Omni extends BigQuery's analytics engine to run queries **directly against data stored in AWS S3 or Azure Blob Storage**, without moving the data to GCP. It uses the Anthos infrastructure to deploy BigQuery compute in the target cloud's region.​

**When relevant:**

*   Client has data in S3 they cannot or will not move to GCP (compliance, cost, contractual)
    
*   Multi-cloud data mesh where each cloud owns its data products
    
*   Federated analytics across GCP + AWS without building an ETL pipeline
    

**Limitations**: BigQuery Omni supports only a subset of BigQuery features (no DML, no streaming, no partitioned table creation). For complex transformations or loading into GCP, you still need to physically copy the data. Think of it as a **query bridge**, not a full BigQuery replacement for cross-cloud data.

Q27. IAM for Service Accounts in Dataflow → BigQuery
----------------------------------------------------

**Q27. How do you configure the minimum necessary IAM permissions for a Dataflow pipeline that reads from BigQuery and writes back to BigQuery?**

Follow the **principle of least privilege** — create a dedicated service account per pipeline:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Create dedicated service account  gcloud iam service-accounts create dataflow-pipeline-sa \    --display-name="Dataflow ETL Pipeline SA"  # Dataflow worker permissions  gcloud projects add-iam-policy-binding PROJECT_ID \    --member="serviceAccount:dataflow-pipeline-sa@PROJECT_ID.iam.gserviceaccount.com" \    --role="roles/dataflow.worker"  # BigQuery read source dataset  gcloud projects add-iam-policy-binding PROJECT_ID \    --member="serviceAccount:dataflow-pipeline-sa@PROJECT_ID.iam.gserviceaccount.com" \    --role="roles/bigquery.dataViewer" \    --condition="..."  # scope to specific dataset using IAM conditions  # BigQuery write destination dataset  gcloud projects add-iam-policy-binding PROJECT_ID \    --member="serviceAccount:dataflow-pipeline-sa@PROJECT_ID.iam.gserviceaccount.com" \    --role="roles/bigquery.dataEditor"  # on destination dataset only  # GCS access for temp files (required by Dataflow)  gcloud storage buckets add-iam-policy-binding gs://dataflow-temp-bucket \    --member="serviceAccount:dataflow-pipeline-sa@..." \    --role="roles/storage.objectAdmin"   `

Never use the default Compute Engine service account or editor-level project roles for pipeline service accounts — if the account is compromised, blast radius is limited to only what it needs.

Q28. PIVOT and UNPIVOT in BigQuery
----------------------------------

**Q28. How do you use PIVOT and UNPIVOT in BigQuery?**

PIVOT transforms row values into column headers (wide format); UNPIVOT does the reverse — turns column headers into row values (long format). Both are natively supported in BigQuery standard SQL.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- PIVOT: monthly sales as columns  SELECT *  FROM (    SELECT product, EXTRACT(MONTH FROM sale_date) AS month, amount    FROM sales  )  PIVOT (    SUM(amount) FOR month IN (1 AS Jan, 2 AS Feb, 3 AS Mar,                                4 AS Apr, 5 AS May, 6 AS Jun)  );  -- Result: one row per product, columns Jan/Feb/Mar...  -- UNPIVOT: reverse — column headers back to rows  SELECT product, month, amount  FROM wide_sales_table  UNPIVOT (amount FOR month IN (Jan, Feb, Mar, Apr, May, Jun));   `

**Limitation**: BigQuery PIVOT requires the column values to be known at query-write time (static). For dynamic pivoting (unknown number of columns at runtime), generate the SQL dynamically using Python with the BigQuery API and the EXECUTE IMMEDIATE statement.

Q29. Time Travel in BigQuery
----------------------------

**Q29. How does BigQuery time travel work and what are its use cases?**

BigQuery retains historical snapshots of every table for up to **7 days** (configurable from 2 to 7 days at the table or dataset level). This allows querying past states using FOR SYSTEM\_TIME AS OF:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Query table state 2 hours ago  SELECT * FROM `project.dataset.orders`  FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR);  -- Compare current vs. 24h ago to detect unexpected changes  SELECT    COALESCE(curr.order_id, hist.order_id) AS order_id,    curr.status AS current_status,    hist.status AS status_24h_ago  FROM `project.dataset.orders` curr  FULL OUTER JOIN `project.dataset.orders`    FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR) hist  ON curr.order_id = hist.order_id  WHERE curr.status != hist.status;   ``

**Use cases:**

*   **Accidental DML recovery**: Restore data overwritten by a bad UPDATE or DELETE
    
*   **Pipeline debugging**: Compare table state before and after a pipeline run
    
*   **Audit**: Investigate what data looked like at a specific point in time for compliance
    
*   **Snapshot creation**: CREATE SNAPSHOT TABLE uses time travel internally
    

Time travel storage incurs **no additional charge** — it's included in active storage pricing.

Q30. Post-Load Data Quality Validation with SQL Assertions
----------------------------------------------------------

**Q30. How do you validate data quality after a BigQuery load using SQL?**

Write **assertion queries** that return rows only when a quality check fails — zero rows = pass, any rows = fail. These can be run in CI/CD, in Airflow as BigQueryCheckOperator, or via dbt tests:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Assertion 1: No NULL values in primary key  SELECT COUNT(*) AS null_count  FROM dataset.orders  WHERE order_id IS NULL  HAVING null_count > 0;  -- returns rows only if check FAILS  -- Assertion 2: No duplicate primary keys  SELECT order_id, COUNT(*) AS cnt  FROM dataset.orders  GROUP BY 1  HAVING cnt > 1;  -- Assertion 3: Row count within expected range (±20% of yesterday)  SELECT    CASE WHEN ABS(today_count - yesterday_count) / NULLIF(yesterday_count, 0) > 0.2      THEN 'FAIL' ELSE 'PASS' END AS result  FROM (    SELECT      COUNTIF(DATE(load_date) = CURRENT_DATE()) AS today_count,      COUNTIF(DATE(load_date) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)) AS yesterday_count    FROM dataset.orders  );   `

In Airflow, use BigQueryCheckOperator (fails task if query returns no rows) or BigQueryIntervalCheckOperator (compares metrics between time periods) to gate downstream tasks on data quality.

🟡 Medium Section: Q31–Q60 — Dataflow, Pub/Sub, Composer, DataFusion
====================================================================

Q31. Dataflow Templates — What and How to Deploy
------------------------------------------------

**Q31. What is a Dataflow template and how do you deploy one in production?**

A Dataflow template packages a pre-compiled pipeline so it can be launched **without access to the source code**, ideal for ops teams or automated triggers.​

**Two types:**

**Classic Templates**: Compile-time parameters only.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Build and stage a classic template  python pipeline.py \    --runner=DataflowRunner \    --template_location=gs://bucket/templates/my_pipeline \    --project=my-project \    --region=australia-southeast1   `

**Flex Templates** (recommended): Runtime parameters, Docker container.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Build Docker image  gcloud builds submit --tag gcr.io/project/pipeline-image .  # Build Flex Template spec  gcloud dataflow flex-template build gs://bucket/templates/my_pipeline.json \    --image gcr.io/project/pipeline-image \    --sdk-language PYTHON  # Launch at runtime  gcloud dataflow flex-template run "job-name" \    --template-file-gcs-location gs://bucket/templates/my_pipeline.json \    --parameters inputTable=project:dataset.table,outputBucket=gs://output   `

Use Flex Templates for all new development — they support dynamic schema handling, custom Python packages, and environment variables not available at compile time.

Q32. Passing Runtime Parameters to Dataflow
-------------------------------------------

**Q32. How do you pass and validate runtime parameters to a Dataflow pipeline?**

Use Apache Beam's PipelineOptions with add\_argument to define typed, documented parameters:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonfrom apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions  class MyPipelineOptions(PipelineOptions):      @classmethod      def _add_argparse_args(cls, parser):          parser.add_argument(              '--input_table',              required=True,              help='BigQuery source table in format project:dataset.table'          )          parser.add_argument(              '--output_bucket',              required=True,              help='GCS output bucket URI'          )          parser.add_argument(              '--batch_date',              default=datetime.now().strftime('%Y-%m-%d'),              help='Processing date in YYYY-MM-DD format'          )  # Parse at runtime  options = PipelineOptions()  my_options = options.view_as(MyPipelineOptions)  # Access in pipeline  with beam.Pipeline(options=options) as p:      data = p | 'Read' >> beam.io.ReadFromBigQuery(          table=my_options.input_table      )   `

Validate parameters early in the pipeline (before expensive operations) and fail fast with descriptive error messages. For sensitive parameters (API keys, passwords), use Secret Manager and pass the secret resource name as a parameter, resolving the value inside the pipeline at runtime.

Q33. Pull vs. Push Pub/Sub Subscriptions
----------------------------------------

**Q33. What is the difference between pull and push subscriptions in Pub/Sub and when do you use each?**

FeaturePullPushWho initiatesSubscriber pullsPub/Sub pushes to an endpointEndpoint typeAny (GCE, Dataflow, Cloud Run)HTTPS endpoint (Cloud Run, App Engine, webhook)ScalingSubscriber controls ratePub/Sub controls rate (up to endpoint capacity)Best forDataflow, batch consumers, high throughputCloud Functions, Cloud Run, serverless event handlersAcknowledgementExplicit ack() callHTTP 200 response = ack

**Pull** is best when the consumer needs **flow control** (Dataflow managing backpressure), processes messages in batches, or runs continuously. **Push** is best for **serverless, event-driven architectures** — a new message immediately triggers a Cloud Run function without polling.​

For high-throughput pipelines (>1,000 msg/sec), pull is almost always preferred because push has webhook latency overhead and can overwhelm downstream HTTPS endpoints during bursts.

Q34. Replaying Pub/Sub Messages via Snapshots
---------------------------------------------

**Q34. How do you use Pub/Sub snapshots to replay messages after a pipeline bug fix?**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Step 1: Create a snapshot of the current subscription state  # (do this BEFORE deploying the bug fix, to capture the rollback point)  gcloud pubsub snapshots create pre-fix-snapshot \    --subscription=projects/my-project/subscriptions/my-subscription  # Step 2: Deploy bug fix to the pipeline  # Step 3: Seek the subscription back to the snapshot  # (replays all messages from the snapshot point onwards)  gcloud pubsub subscriptions seek my-subscription \    --snapshot=pre-fix-snapshot  # OR: seek back to a specific timestamp  gcloud pubsub subscriptions seek my-subscription \    --time="2026-03-19T10:00:00Z"   `

**Important notes:**

*   Snapshots are retained for up to **7 days**
    
*   After seeking, messages are redelivered — ensure your pipeline is **idempotent** (handles duplicates gracefully) before replaying
    
*   Delete the snapshot after replay to free storage: gcloud pubsub snapshots delete pre-fix-snapshot
    
*   In production, create a pre-deployment snapshot as part of your CI/CD release process for every streaming pipeline deployment — it's your rollback safety net
    

Q35. Airflow Retry Logic and Timeouts
-------------------------------------

**Q35. How do you configure retry logic, timeouts, and error handling for Airflow tasks?**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonfrom datetime import timedelta  from airflow import DAG  from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator  default_args = {      'owner': 'data-engineering',      'retries': 3,      'retry_delay': timedelta(minutes=5),      'retry_exponential_backoff': True,   # doubles delay on each retry      'max_retry_delay': timedelta(minutes=60),      'execution_timeout': timedelta(hours=2),  # task-level timeout      'on_failure_callback': notify_slack,      # custom failure handler      'on_retry_callback': log_retry_event,      'sla': timedelta(hours=1),               # SLA breach triggers alert  }  with DAG('my_pipeline', default_args=default_args,           schedule_interval='0 6 * * *',           dagrun_timeout=timedelta(hours=4)) as dag:  # DAG-level timeout      load_task = BigQueryInsertJobOperator(          task_id='load_data',          retries=5,              # override default for this specific task          retry_delay=timedelta(minutes=2),          ...      )   `

**Best practices:**

*   Set retry\_exponential\_backoff=True for tasks calling external APIs (avoids hammering a recovering service)
    
*   Set execution\_timeout on tasks to prevent zombie tasks hanging indefinitely
    
*   Set dagrun\_timeout to ensure SLA breaches are caught at the DAG level
    
*   Use on\_failure\_callback to send Slack/PagerDuty alerts immediately without waiting for Airflow's email alerting
    

Q36. execution\_date vs. logical\_date in Airflow
-------------------------------------------------

**Q36. What is the difference between execution\_date and logical\_date in Airflow, and why does the naming cause confusion?**

In Airflow 2.2+, logical\_date replaced execution\_date to reduce confusion, but both refer to the same concept: the **scheduled start of the data interval**, NOT the actual wall-clock time the task ran.​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# DAG scheduled daily at midnight  # A run "for" 2026-03-19 is TRIGGERED on 2026-03-20 00:00:00  # logical_date = 2026-03-19 00:00:00  (the start of the data interval)  # data_interval_start = 2026-03-19 00:00:00  # data_interval_end   = 2026-03-20 00:00:00  def process_data(**context):      # Correct: use logical_date to process "yesterday's" data      processing_date = context['logical_date'].date()  # 2026-03-19      # This is why pipelines run "one day behind" — by design   `

**Why it matters for data engineers:** If your pipeline uses CURRENT\_DATE() instead of logical\_date, you lose the ability to safely backfill historical runs — each backfill run would process "today" instead of the historical period. Always parameterise on logical\_date / data\_interval\_start for idempotent, backfill-safe pipelines.

Q37. Triggering a DAG from External Events
------------------------------------------

**Q37. How do you trigger a Cloud Composer DAG from an external event rather than a schedule?**

**Method 1 — Airflow REST API (recommended):**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonimport requests  # Cloud Run service triggered by GCS event → calls Airflow API  def trigger_dag(dag_id: str, conf: dict):      url = f"https://COMPOSER_URL/api/v1/dags/{dag_id}/dagRuns"      headers = {"Authorization": f"Bearer {get_access_token()}"}      payload = {"conf": conf, "logical_date": datetime.utcnow().isoformat()}      response = requests.post(url, json=payload, headers=headers)      return response.json()   `

**Method 2 — Cloud Functions + Airflow API:** Eventarc triggers a Cloud Function on GCS object finalise → Cloud Function calls the Airflow REST API to trigger the DAG, passing the file path in conf.

**Method 3 — TriggerDagRunOperator:** From within a running DAG, trigger another DAG:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonfrom airflow.operators.trigger_dagrun import TriggerDagRunOperator  trigger_downstream = TriggerDagRunOperator(      task_id='trigger_reporting_dag',      trigger_dag_id='daily_reporting',      conf={"source_table": "project:dataset.table"},      wait_for_completion=True  # optionally wait for triggered DAG  )   `

Method 1 + Eventarc is the modern event-driven pattern — zero polling, instantaneous triggering, fully decoupled.

Q38. Airflow Sensors and GCP Sensors
------------------------------------

**Q38. What are Airflow sensors and what GCP-specific sensors are available?**

Sensors are operators that **wait for a condition to be met** before allowing downstream tasks to proceed. They poke the condition at a configured interval:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonfrom airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor  from airflow.providers.google.cloud.sensors.bigquery import BigQueryTableExistenceSensor  from airflow.providers.google.cloud.sensors.pubsub import PubSubPullSensor  from airflow.providers.google.cloud.sensors.dataflow import DataflowJobStatusSensor  # Wait for upstream file to arrive in GCS  wait_for_file = GCSObjectExistenceSensor(      task_id='wait_for_source_file',      bucket='my-bucket',      object='data/{{ ds }}/input.csv',      mode='reschedule',    # releases worker slot between pokes (efficient!)      poke_interval=60,     # check every 60 seconds      timeout=3600          # fail after 1 hour  )   `

**Key GCP sensors:** GCSObjectExistenceSensor, GCSObjectUpdateSensor, BigQueryTableExistenceSensor, DataflowJobStatusSensor, PubSubPullSensor, CloudComposerEnvironmentSensor.

**Critical option — mode='reschedule'**: Always use reschedule mode in production. The default poke mode keeps the worker slot occupied while waiting, wasting Celery worker capacity. reschedule releases the worker between pokes and is mandatory for sensors with long timeouts.

Q39. Environment Variables in Cloud Composer
--------------------------------------------

**Q39. How do you manage environment variables and Airflow variables in Cloud Composer securely?**

**Avoid**: Storing secrets as Airflow Variables in the metadata database (plaintext, visible to anyone with Airflow UI access).

**Recommended approaches:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Option 1: Secret Manager backend (best practice)  # Configure in airflow.cfg or Composer environment  # [secrets]  # backend = airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend  # backend_kwargs = {"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables"}  # Access in DAG code — automatically fetches from Secret Manager  from airflow.models import Variable  db_password = Variable.get("db_password")  # resolves from Secret Manager  # Option 2: Environment variables set on the Composer environment  gcloud composer environments update my-composer \    --location australia-southeast1 \    --update-env-variables ENVIRONMENT=production,PROJECT_ID=my-project  # Access in DAG  import os  env = os.environ.get('ENVIRONMENT')  # Option 3: GCS-based config files (for non-secret config)  # Store JSON config in GCS, read in DAG using GCS hook   `

For API keys, database passwords, and service credentials — always Secret Manager. For non-sensitive config (project IDs, bucket names, feature flags) — environment variables or Airflow Variables are acceptable.

Q40. DataFusion Pipeline Lifecycle
----------------------------------

**Q40. Describe the full lifecycle of a DataFusion pipeline from development to production.**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   text1. DESIGN (Studio UI)     ├── Drag-and-drop source plugins (BigQuery, GCS, JDBC, Pub/Sub)     ├── Add transform plugins (Wrangler, JavaScript, Joiner, Aggregator)     └── Connect to sink plugins (BigQuery, GCS, Spanner)  2. CONFIGURE     ├── Set runtime arguments (macro substitution: ${date}, ${env})     ├── Configure compute profile (Dataproc cluster size/type)     └── Define error handling (fail on error / skip / write to error dataset)  3. PREVIEW     └── Run on sample data in the UI to validate transformation logic  4. DEPLOY     ├── Export pipeline JSON spec to Git (version control)     ├── Deploy via DataFusion REST API or CDAP CLI for CI/CD     └── Promote across environments (dev → staging → prod) by deploying to         different DataFusion instances with environment-specific runtime args  5. SCHEDULE / TRIGGER     ├── DataFusion native scheduler (basic cron)     └── Cloud Composer: DataFusionStartPipelineOperator (recommended for production)  6. MONITOR     └── Dataflow job metrics (underlying execution engine), DataFusion pipeline history UI   `

Q41. Connecting Cloud SQL to DataFusion
---------------------------------------

**Q41. How do you connect a Cloud SQL database as a source in DataFusion?**

DataFusion uses JDBC-based connectors for Cloud SQL:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Step 1: Enable Cloud SQL Admin API and create a Private IP or Public IP Cloud SQL instance  # Step 2: In DataFusion Studio, add a Database plugin (source)  # Connection properties:  #   Connection String: jdbc:mysql://PRIVATE_IP:3306/database_name  #   Username: db_user  #   Password: ${db_password}  (macro — set as runtime argument from Secret Manager)  #   Driver Name: MySQL (pre-installed) or PostgreSQL  # Step 3: For Cloud SQL with Public IP, use Cloud SQL Auth Proxy  # Deploy Auth Proxy as a sidecar on the DataFusion compute cluster  # Connect to localhost:3306 instead of public IP   `

**For production**: Use **Private IP** Cloud SQL (VPC peering with DataFusion's managed VPC) to avoid exposing the database on the public internet. Configure the DataFusion instance to use a **Customer-Managed Encryption Key (CMEK)** and enable Private Google Access on the subnet used by the Dataproc cluster.

Q42. Running Dataflow from Airflow
----------------------------------

**Q42. How do you launch and monitor a Dataflow job from Cloud Composer?**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonfrom airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator  from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator  # Option 1: Launch a Flex Template  launch_dataflow = DataflowStartFlexTemplateOperator(      task_id='run_etl_pipeline',      body={          "launchParameter": {              "jobName": "etl-pipeline-{{ ds_nodash }}",              "parameters": {                  "input_table": "project:dataset.source",                  "output_table": "project:dataset.target",                  "processing_date": "{{ ds }}"              },              "containerSpecGcsPath": "gs://bucket/templates/pipeline.json",              "environment": {                  "machineType": "n1-standard-4",                  "maxWorkers": 10,                  "serviceAccountEmail": "dataflow-sa@project.iam.gserviceaccount.com",                  "tempLocation": "gs://bucket/dataflow-temp/"              }          }      },      location='australia-southeast1',      wait_until_finished=True,   # block until job completes      deferrable=True             # use deferrable mode to release worker while waiting  )   `

Use deferrable=True (Airflow 2.2+) so the Airflow worker is not blocked while waiting for the Dataflow job to finish — critical for long-running jobs.​

Q43. Cloud Monitoring Metrics for Pub/Sub Health
------------------------------------------------

**Q43. What Cloud Monitoring metrics do you track for Pub/Sub pipeline health?**

MetricWhat It MeasuresAlert Thresholdpubsub.googleapis.com/subscription/num\_undelivered\_messagesBacklog size> expected maxpubsub.googleapis.com/subscription/oldest\_unacked\_message\_ageOldest unprocessed message age> SLA (e.g., 300s)pubsub.googleapis.com/subscription/num\_outstanding\_messagesIn-flight messages being processedSustained high valuepubsub.googleapis.com/topic/send\_message\_operation\_countPublisher throughputDrop to 0 = upstream outagepubsub.googleapis.com/subscription/dead\_letter\_message\_countMessages sent to DLQAny > 0 for critical topics

**Most critical metric**: oldest\_unacked\_message\_age — it directly measures how far behind consumers are, regardless of backlog size. A large backlog is fine if it's being processed quickly; a growing oldest-message age indicates a stuck or slow consumer.​

Set up a Cloud Monitoring dashboard combining all five metrics per subscription, with PagerDuty alerts on oldest\_unacked\_message\_age > 300 seconds for production pipelines.

Q44. Fan-Out with Pub/Sub Topic → Multiple Subscriptions
--------------------------------------------------------

**Q44. How do you implement fan-out (one message to multiple consumers) with Pub/Sub?**

Create **one subscription per consumer** on the same topic. Each subscription maintains its own independent cursor and delivery state:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# One topic, multiple subscriptions for fan-out  gcloud pubsub topics create order-events  # Consumer 1: Dataflow pipeline for order analytics  gcloud pubsub subscriptions create order-analytics-sub \    --topic=order-events \    --ack-deadline=60  # Consumer 2: Cloud Function for fraud detection  gcloud pubsub subscriptions create order-fraud-sub \    --topic=order-events \    --ack-deadline=30  # Consumer 3: Cloud Run for real-time notifications  gcloud pubsub subscriptions create order-notifications-sub \    --topic=order-events \    --push-endpoint=https://notifications-service.run.app/webhook \    --ack-deadline=10   `

Each consumer processes at its own pace, has its own backlog, and fails independently — a slow fraud detection service doesn't block the analytics pipeline. Use **subscription filters** to route only relevant message subsets (e.g., attributes.region = "AU") to specific subscriptions, reducing processing cost.

Q45. Pub/Sub Message Retention
------------------------------

**Q45. What is Pub/Sub message retention and how do you configure it for replay scenarios?**

By default, Pub/Sub retains **unacknowledged messages for 7 days**. For replay scenarios, you can configure **topic-level message retention** to retain messages even after acknowledgement:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Enable message retention on the topic (retain for 7 days after publish)  gcloud pubsub topics create my-topic \    --message-retention-duration=7d  # This allows you to seek any subscription back to any point  # within the retention window, even for already-acknowledged messages  gcloud pubsub subscriptions seek my-subscription \    --time="2026-03-15T00:00:00Z"   `

**Without topic retention**: Once a message is acknowledged, it is deleted — you cannot replay it. **With topic retention**: Messages are retained on the topic storage for the configured duration, and any subscription can be seeked back to replay from any point in that window.

**Cost**: Message retention storage is charged per GB retained. For high-volume topics (GB/hour), this can be significant — balance retention window against replay need and cost.

Q46. Cloud Scheduler + Cloud Functions for Lightweight ETL
----------------------------------------------------------

**Q46. How do you use Cloud Scheduler and Cloud Functions for lightweight, scheduled ETL tasks?**

This pattern is ideal for simple, fast tasks (under 9 minutes) that don't need Composer's orchestration overhead:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Cloud Function triggered by Cloud Scheduler (HTTP target)  import functions_framework  from google.cloud import bigquery  @functions_framework.http  def run_etl(request):      client = bigquery.Client()      # Example: run a BigQuery transformation on a schedule      query = """          INSERT INTO dataset.daily_summary          SELECT DATE(event_time) AS date, COUNT(*) AS events          FROM dataset.raw_events          WHERE DATE(event_time) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)            AND DATE(event_time) NOT IN (SELECT date FROM dataset.daily_summary)      """      job = client.query(query)      job.result()  # wait for completion      return f"Inserted {job.num_dml_affected_rows} rows", 200   `

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Schedule the function to run daily at 1 AM AEST  gcloud scheduler jobs create http daily-etl-job \    --schedule="0 15 * * *" \   # 1 AM AEST = 15:00 UTC    --uri="https://REGION-PROJECT.cloudfunctions.net/run_etl" \    --http-method=GET \    --oidc-service-account-email=scheduler-sa@project.iam.gserviceaccount.com   `

**When to use Scheduler + Functions over Composer:** Single-step jobs, no complex dependencies, sub-5-minute runtime, very low cost requirement. **When to use Composer instead:** Multi-step pipelines, complex dependencies, retry logic, backfilling requirements, or tasks exceeding Cloud Function's 9-minute timeout.

Q47. DataFusion Schema Mapping
------------------------------

**Q47. How does DataFusion handle schema mapping between source and sink?**

DataFusion's pipeline designer performs **automatic schema detection** by inspecting source plugins at design time. Each plugin exposes an output schema that flows through the pipeline as a directed graph.​

**Schema propagation:**

*   Source plugin (e.g., BigQuery) auto-detects the table schema
    
*   Transform plugins (Wrangler, Projection) modify the schema by adding/removing/renaming fields
    
*   The schema is validated at each stage connection — type mismatches surface as design-time errors, not runtime failures
    

**Schema mapping in the Joiner plugin:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   textSource A (orders): order_id STRING, amount NUMERIC  Source B (customers): customer_id STRING, name STRING  → Join on orders.customer_id = customers.customer_id  → Output schema: order_id, amount, name (with column selection)   `

**Handling schema mismatches:** Use the **Schema plugin** to explicitly cast types (e.g., STRING → TIMESTAMP), rename fields, or drop columns before they reach the sink. For sinks with strict schemas (BigQuery), mismatched types cause runtime failures — always preview with the schema validator before deploying.

Q48. PTransform vs. DoFn in Apache Beam
---------------------------------------

**Q48. What is the difference between a PTransform and a DoFn in Apache Beam?**

A **DoFn** (Do Function) defines the **per-element processing logic** — it is the unit of work applied to each element in a PCollection. A **PTransform** is a higher-level **composable abstraction** that encapsulates a complete pipeline operation (which may contain multiple DoFns and sub-transforms):​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonimport apache_beam as beam  # DoFn: per-element transformation  class ParseJsonDoFn(beam.DoFn):      def process(self, element):          import json          record = json.loads(element)          yield {              'user_id': record['uid'],              'event': record['event_type'],              'ts': record['timestamp']          }  # PTransform: composable, reusable pipeline component  class ParseAndEnrichEvents(beam.PTransform):      def expand(self, pcoll):          return (              pcoll              | 'Parse' >> beam.ParDo(ParseJsonDoFn())              | 'Filter' >> beam.Filter(lambda x: x['event'] != 'test')              | 'AddMetadata' >> beam.Map(lambda x: {**x, 'processed_at': time.time()})          )  # Usage in pipeline  with beam.Pipeline() as p:      (p       | 'ReadPubSub' >> beam.io.ReadFromPubSub(topic='...')       | 'ParseEvents' >> ParseAndEnrichEvents()   # clean, reusable transform       | 'WriteBQ' >> beam.io.WriteToBigQuery(...)      )   `

Use PTransform to build **reusable pipeline libraries** — package common patterns (PII masking, schema validation, error routing) as PTransforms shared across multiple pipelines.

Q49. Reading from Cloud SQL in Dataflow
---------------------------------------

**Q49. How do you read data from Cloud SQL inside a Dataflow pipeline?**

Beam doesn't have a native Cloud SQL source, so you use the **JDBC connector** via ReadFromJdbc or make direct database calls inside a DoFn:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Method 1: ReadFromJdbc (batch, parallel reads)  from apache_beam.io.jdbc import ReadFromJdbc  records = (      p | 'ReadCloudSQL' >> ReadFromJdbc(          table_name='orders',          driver_class_name='org.postgresql.Driver',          jdbc_url='jdbc:postgresql://CLOUD_SQL_PRIVATE_IP:5432/mydb',          username='user',          password=secret_manager_client.get_secret('db_password'),          query='SELECT * FROM orders WHERE order_date = ?',          query_parameters=[processing_date]      )  )  # Method 2: DoFn with connection pool (for streaming enrichment lookups)  class LookupCustomerDoFn(beam.DoFn):      def setup(self):          # Called once per worker — create connection pool          self.conn = pg8000.connect(host=CLOUD_SQL_IP, ...)      def process(self, element):          cursor = self.conn.cursor()          cursor.execute("SELECT name FROM customers WHERE id = %s", [element['customer_id']])          result = cursor.fetchone()          yield {**element, 'customer_name': result[0] if result else 'Unknown'}      def teardown(self):          self.conn.close()   `

Always use setup() and teardown() lifecycle methods for database connections — never create connections in \_\_init\_\_ (called at serialisation time, not worker startup).

Q50. Dataflow DirectRunner for Local Testing
--------------------------------------------

**Q50. How do you use the DirectRunner to test Dataflow pipelines locally?**

The DirectRunner executes Beam pipelines locally on your machine without any GCP services — enabling fast iteration and unit testing:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonimport apache_beam as beam  from apache_beam.testing.test_pipeline import TestPipeline  from apache_beam.testing.util import assert_that, equal_to  # Unit test using TestPipeline (uses DirectRunner)  class MyTransformTest(unittest.TestCase):      def test_parse_json(self):          with TestPipeline() as p:              input_data = ['{"user_id": "abc", "event": "click"}']              expected = [{'user_id': 'abc', 'event': 'click'}]              result = (                  p                  | beam.Create(input_data)                  | beam.ParDo(ParseJsonDoFn())              )              assert_that(result, equal_to(expected))  # Run pipeline locally (not in test context)  pipeline = beam.Pipeline(runner='DirectRunner')  # ... build pipeline ...  pipeline.run().wait_until_finish()   `

**Limitations of DirectRunner**: Single-machine, no autoscaling, no Dataflow Shuffle/Streaming Engine. It's accurate for **logic testing** but not for performance profiling. For integration tests, use a dedicated GCP test project with real Dataflow jobs running on small datasets.

Q51. Unit Testing Airflow DAGs
------------------------------

**Q51. How do you write unit tests for Airflow DAGs?**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonimport pytest  from airflow.models import DagBag  class TestMyDag:      def setup_method(self):          self.dagbag = DagBag(dag_folder='dags/', include_examples=False)      def test_dag_loads_without_errors(self):          """DAG must load without import errors"""          assert 'my_pipeline_dag' in self.dagbag.dags          assert len(self.dagbag.import_errors) == 0      def test_dag_has_correct_tasks(self):          dag = self.dagbag.get_dag('my_pipeline_dag')          task_ids = [task.task_id for task in dag.tasks]          assert 'quality_gate' in task_ids          assert 'load_to_bigquery' in task_ids      def test_task_dependencies(self):          dag = self.dagbag.get_dag('my_pipeline_dag')          quality_gate = dag.get_task('quality_gate')          load_task = dag.get_task('load_to_bigquery')          assert load_task in quality_gate.downstream_list      def test_dag_has_no_cycles(self):          dag = self.dagbag.get_dag('my_pipeline_dag')          assert dag.test_cycle() is False      def test_retries_configured(self):          dag = self.dagbag.get_dag('my_pipeline_dag')          for task in dag.tasks:              assert task.retries >= 1, f"Task {task.task_id} has no retries configured"   `

Run these in CI on every PR. Tests that catch import errors, missing tasks, broken dependencies, and missing retry configs prevent production incidents from misconfigured DAGs.

Q52. Alerting on Airflow Task Failures
--------------------------------------

**Q52. How do you implement robust alerting for Airflow task failures in Cloud Composer?**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonfrom airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator  def alert_slack_on_failure(context):      dag_id = context['dag'].dag_id      task_id = context['task_instance'].task_id      execution_date = context['execution_date']      log_url = context['task_instance'].log_url      message = f"""  :red_circle: *Task Failed*  • *DAG*: {dag_id}  • *Task*: {task_id}  • *Execution Date*: {execution_date}  • *Log*: <{log_url}|View Logs>      """      SlackWebhookOperator(          task_id='slack_alert',          http_conn_id='slack_webhook',          message=message      ).execute(context)  default_args = {      'on_failure_callback': alert_slack_on_failure,      'sla_miss_callback': alert_slack_on_sla_miss,  }   `

**Multi-layered alerting strategy:**

1.  **Task level**: on\_failure\_callback → Slack (immediate, actionable)
    
2.  **SLA level**: sla\_miss\_callback → PagerDuty (for SLA-breaching pipelines)
    
3.  **DAG level**: on\_failure\_callback on the DAG object for summary alerts
    
4.  **Cloud Monitoring**: Log-based metric on ERROR severity logs → alerting policy → email/PagerDuty for systemic issues
    

Q53. GCS → BigQuery Direct Load vs. Dataflow ETL
------------------------------------------------

**Q53. When do you use direct GCS → BigQuery load jobs vs. a Dataflow ETL pipeline?**

CriteriaDirect BQ LoadDataflow ETLTransformation needed?None (load as-is)Yes (complex logic)Data volumeAnyAnyLatency requirementMinutesSeconds to minutesCostLow (loading is free; storage only)Higher (worker costs)Error handlingBasic (reject rows)Rich (dead-letter, custom logic)PII processing needed?NoYes

**Use direct load when:** The source file is already in the right schema, format (CSV/Parquet/Avro/JSON), and no transformation is needed. BigQuery load jobs are **free** (only storage is charged) and handle petabyte-scale files efficiently.

**Use Dataflow when:** The data requires schema transformation, field-level masking, enrichment from other sources, deduplication, or routing to multiple destinations. Dataflow adds operational complexity and cost — don't use it as a default if a direct load achieves the same result.​

Q54. Schema Mismatches Between Pub/Sub Messages and BigQuery
------------------------------------------------------------

**Q54. How do you handle schema mismatches between incoming Pub/Sub messages and the target BigQuery table schema?**

Implement a **flexible parsing and schema enforcement layer** in Dataflow between Pub/Sub and BigQuery:

```
class ParseAndValidateDoFn(beam.DoFn):
    def __init__(self, expected_schema):
        self.expected_schema = expected_schema

    def process(self, element):
        try:
            record = json.loads(element.decode('utf-8'))

            # Coerce types to
```

🟢 100 Scenario / Use-Case Based Questions
==========================================

Data Lake & Warehouse Design
----------------------------

**S1. A client wants to ingest 500GB/day of clickstream data from their website into BigQuery for analytics. Design the end-to-end architecture.**

**Answer**: Use Google Tag Manager → Pub/Sub for real-time event ingestion. Deploy a Dataflow streaming pipeline to parse, validate (using DLP for PII), and transform JSON events into a structured schema. Write to a BigQuery partitioned table (event\_date partition, user\_id cluster). Raw events land in GCS simultaneously (dead-letter for replay). Use dbt for modelling in the analytics layer. CI/CD via Cloud Build deploys pipeline changes, with data quality tests gating each promotion.

**S2. Your client has data in 15 different source systems (ERP, CRM, IoT, flat files). How do you design a scalable ingestion framework?**

**Answer**: Build a metadata-driven ingestion framework. Store source configs (connection, schema, schedule, load type) in a Cloud SQL config table. A master Airflow DAG reads configs and dynamically generates child DAGs per source. Use DataFusion for JDBC sources, Datastream for CDC databases, GCS uploads for flat files, and custom Cloud Functions for APIs. All data lands in a raw GCS zone → Dataflow normalizes to Parquet in the refined zone → BigQuery external tables for SQL access.​

**S3. A client's BigQuery costs have tripled in the last month. How do you investigate and resolve it?**

**Answer**: Query INFORMATION\_SCHEMA.JOBS to identify top queries by total\_bytes\_billed and user\_email. Check for new SELECT \* queries, missing partition filters, or ad-hoc exploration by analysts. Implement: (1) partition pruning enforcement via require\_partition\_filter=TRUE, (2) column-level access to reduce SELECT \*, (3) BigQuery cost controls using custom quotas per user/group, (4) educate teams on using bq --dry\_run before executing large queries, and (5) consider switching from on-demand to capacity pricing if workloads are predictable.​

**S4. You need to design a data platform for a healthcare client with strict HIPAA compliance requirements.**

**Answer**: Architecture: VPC Service Controls perimeter around all GCP services. Encrypt all data at rest with CMEK (Cloud KMS). Apply Cloud DLP to automatically detect and tokenize PHI (Protected Health Information) before writing to BigQuery. Implement column-level security via policy tags. Enable all Audit Log types (DATA\_READ, DATA\_WRITE, ADMIN\_WRITE) and export to a separate, locked-down compliance project. Use Assured Workloads to enforce healthcare-specific controls. Document data lineage via Data Catalog.​

**S5. A real-time dashboard must show order status within 30 seconds of an order event. How do you design this?**

**Answer**: Order service publishes to Pub/Sub → Dataflow streaming pipeline enriches with product/customer dimensions (SideInput from Bigtable lookup) → writes to BigQuery via Storage Write API (streaming, low latency) AND to Bigtable for sub-millisecond serving. Looker Studio queries BigQuery for historical trends; a custom API hits Bigtable for real-time status. Dataflow with Streaming Engine ensures end-to-end latency <10 seconds.​

ETL / Pipeline Problems
-----------------------

**S6. Your nightly Dataflow batch job suddenly takes 4x longer than usual. How do you diagnose it?**

**Answer**: Check the Dataflow UI for hot keys (one worker handling disproportionate data), which indicates data skew. Check upstream source — did GCS file size increase? Look at Cloud Monitoring for worker CPU/memory bottlenecks. Check for new NULLs or data anomalies causing slow transforms. If skew, add a Reshuffle transform to redistribute. If source grew, increase --maxNumWorkers and adjust the autoscaling algorithm.

**S7. A Pub/Sub subscription has a growing backlog of 50 million unprocessed messages. What do you do?**

**Answer**: Immediately scale up Dataflow workers (gcloud dataflow jobs update-options --max-workers=N). Check if there's a processing error causing repeated NACKs (check dead-letter topic volume). If messages are being processed but too slowly, profile the DoFn for bottlenecks — database calls, API calls inside the transform. Consider increasing parallelism by splitting the subscription or using Pub/Sub Lite with more throughput capacity. Monitor oldest\_unacked\_message\_age until it drops.

**S8. A client requires zero-downtime migration of their on-premises Oracle data warehouse to BigQuery. What is your migration plan?**

**Answer**:

1.  **Assessment**: Profile Oracle schemas, query patterns, stored procedures, and data volumes
    
2.  **Schema conversion**: Use BigQuery Migration Service to auto-convert DDL; manually handle Oracle-specific types
    
3.  **Initial load**: Extract to GCS as Parquet using Oracle Data Pump + custom scripts; load to BigQuery
    
4.  **CDC**: Set up Datastream with Oracle LogMiner CDC to replicate changes during cutover period
    
5.  **Validation**: Row counts, checksums, business metric comparisons between Oracle and BQ
    
6.  **Cutover**: Pause source writes, apply final CDC delta, flip application connection strings, decommission Oracle
    

**S9. Your Airflow DAG fails intermittently due to Cloud SQL timeouts. How do you fix it?**

**Answer**: Implement exponential backoff retry in the Airflow operator (retries=3, retry\_delay=timedelta(minutes=2), retry\_exponential\_backoff=True). Use Cloud SQL Auth Proxy for connection management and connection pooling (SQLAlchemy pool settings). Investigate if Cloud SQL is undersized (CPU/RAM/connections) during peak hours — consider upgrading instance or using connection pooling via Cloud SQL's built-in pooling. Add custom metrics to track connection wait times.

**S10. A downstream BI team complains their reports show different numbers than the data engineering team's pipeline outputs. How do you resolve it?**

**Answer**: This is a data trust issue. First, document the agreed business definitions for each metric (e.g., what constitutes "active user"). Trace the data lineage from raw source → transformation → mart → BI tool using Data Catalog. Compare SQL logic between the pipeline and BI tool calculations. Implement a single source of truth: create a certified BigQuery view owned by data engineering that the BI tool queries directly. Add automated reconciliation checks that compare pipeline output to source system counts daily.

Leadership & Stakeholder Scenarios
----------------------------------

**S11. A junior engineer on your team has committed broken code to production that caused a 4-hour pipeline outage. How do you handle it?**

**Answer**: First priority is restoring service: roll back via Terraform/Cloud Build, trigger historical backfill via Airflow. Once resolved, conduct a blameless post-mortem — document the timeline, root cause (lack of automated tests? missing code review?), and corrective actions. Work WITH the junior engineer to add the missing tests and improve the CI gate. Communicate transparently to stakeholders with an incident report. The goal is systemic improvement, not blame — this builds psychological safety on the team.​

**S12. A client's senior stakeholder wants a feature added to the pipeline mid-sprint that would require significant rework. How do you handle it?**

**Answer**: Acknowledge the business value of the request, then present a transparent impact analysis: "Adding this will require X days, push Y deliverable by Z days, and risk the sprint commitment." Offer options: (1) defer to next sprint with documented priority, (2) descope a lower-priority item to accommodate, (3) fast-track a minimal version now with full implementation later. Document the decision in writing. Never silently absorb scope without acknowledging the tradeoff — this is how projects fail.​

**S13. You are leading a team of 5 data engineers. Two team members have a technical disagreement about whether to use Dataflow or Dataproc for a new pipeline. How do you resolve it?**

**Answer**: Frame it as a technical decision, not a personal one. Ask both engineers to prepare a structured comparison (criteria: operational overhead, cost, team skillset, performance at expected scale, time to build). Facilitate a decision meeting where both present to the team. Guide the discussion toward objective criteria aligned with project constraints. Make the final call based on facts and document the decision rationale. This builds a culture of evidence-based decisions and respects both engineers' expertise.

**S14. Halfway through a 3-month data lake project, you discover that a key data source has inconsistent quality that was not identified in scoping. How do you escalate?**

**Answer**: Immediately quantify the issue: what % of records are affected, which downstream analytics are impacted, and what remediation options exist (cleanse, quarantine, source fix). Prepare a concise risk document with options and recommendations. Escalate to the project lead/client sponsor within 24 hours — never sit on risks. Propose a revised timeline or scope adjustment. In parallel, implement a data quality quarantine layer so the pipeline doesn't propagate bad data while the issue is being resolved.

**S15. A client asks you to skip unit testing to accelerate delivery. How do you respond?**

**Answer**: Explain the risk-reward: skipping tests now creates technical debt that compounds — a production bug in untested code costs 5-10x more to fix than a test written upfront. Propose a pragmatic compromise: write tests only for the highest-risk transformations (financial calculations, PII handling), use test templates to reduce effort, and automate test execution in CI so it doesn't slow delivery once set up. Frame it as protecting the client's investment, not slowing down the team.

🟢 Data Quality & Observability: S16–S30
========================================

S16. Zero-Tolerance Financial Data Quality Framework
----------------------------------------------------

**S16. Build a data quality framework for a financial data pipeline with zero-tolerance for errors.**

Financial pipelines have the highest stakes — a single bad row can mean incorrect regulatory reports, wrong trades, or compliance breaches. The framework must be **preventative** (stop bad data entering), **detective** (catch anomalies immediately), and **corrective** (quarantine, alert, replay).

**Architecture:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   textSource System      ↓  [Layer 1 — Schema Enforcement]  Pub/Sub Schema Registry (Avro/Protobuf) — rejects malformed messages at publish time      ↓  [Layer 2 — Field-Level Validation in Dataflow]  - Null checks on required fields (trade_id, amount, counterparty)  - Type coercion failures → dead-letter topic (not silent drop)  - Range checks: amount > 0, settlement_date >= trade_date  - Referential integrity: counterparty_id exists in master table (Bigtable lookup)      ↓  [Layer 3 — Staging Quarantine Table in BigQuery]  Write ALL records to staging.trades_incoming (never directly to production)      ↓  [Layer 4 — dbt Quality Gate]  dbt tests run against staging:    - not_null on all 12 required fields    - unique on trade_id    - accepted_values for currency_code (ISO 4217)    - custom SQL: no duplicate (trade_id, trade_date) combos    - row count within ±5% of previous 5-day average  Only on 100% test pass → MERGE to production.trades      ↓  [Layer 5 — Reconciliation]  Daily SQL: compare staging row count vs source system count  Alert if delta > 0 rows   `

**Key design decisions:**

*   **Never write directly to production** — always stage first, gate second
    
*   **Dead-letter everything** — malformed records go to a quarantine table with error reason, never silently dropped
    
*   **Escalation path**: dbt test failure → Slack alert → PagerDuty if not acknowledged in 15 min → halt all downstream pipelines via Airflow ShortCircuitOperator
    
*   **Immutable audit log**: Every record transition (quarantine → production, rejection reason) written to an audit BigQuery table with timestamps, operator identity, and job\_id
    

S17. SLA Monitoring for Pipelines That Must Complete by 6 AM
------------------------------------------------------------

**S17. Design SLA monitoring for pipelines that must complete by 6 AM daily.**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Airflow SLA miss callback  from airflow.utils.email import send_email  from datetime import timedelta  def sla_miss_alert(dag, task_list, blocking_task_list, slas, blocking_tis):      """Fires when any task misses its SLA"""      message = f"""      SLA BREACH ALERT      DAG: {dag.dag_id}      Tasks breached: {[t.task_id for t in task_list]}      Time: {datetime.now().strftime('%Y-%m-%d %H:%M AEST')}      """      send_pagerduty_alert(message, severity='critical')      send_slack_message('#data-ops', message)  with DAG(      'financial_daily_pipeline',      schedule_interval='0 20 * * *',   # 6 AM AEST = 8 PM UTC      dagrun_timeout=timedelta(hours=9), # must complete within 9 hours      sla_miss_callback=sla_miss_alert,      default_args={          'sla': timedelta(hours=8)      # each task must complete within 8h      }  ) as dag:      ...   `

**Additional monitoring layers beyond Airflow:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Cloud Monitoring: alert if table freshness > SLA  -- Schedule this query via Cloud Scheduler every 30 minutes after 5 AM  SELECT    table_name,    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_modified_time, MINUTE) AS minutes_stale,    CASE WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_modified_time, HOUR) > 1      THEN 'SLA_BREACH' ELSE 'OK' END AS sla_status  FROM (    SELECT 'orders_daily' AS table_name,           last_modified_time    FROM `project.dataset.INFORMATION_SCHEMA.TABLE_STORAGE`    WHERE table_name = 'orders_daily'  )  WHERE sla_status = 'SLA_BREACH';   ``

**Tiered escalation**: 5:00 AM — pipeline not complete → Slack warning. 5:45 AM — pipeline not complete → PagerDuty page to on-call engineer. 6:15 AM — SLA breached → executive notification + downstream system freeze.​

S18. 15% NULL Rate on a Non-Nullable Business Key
-------------------------------------------------

**S18. A BigQuery table has a 15% NULL rate in a non-nullable business key column. What do you do?**

Never accept NULLs in business keys — they indicate upstream data quality failure or a transformation bug. This is a P1 incident.​

**Immediate response (within 1 hour):**

1.  **Quarantine**: Stop loading new data from the affected source immediately — prevent more NULLs entering production
    
2.  **Scope**: SELECT COUNT(\*), MIN(event\_date), MAX(event\_date) FROM table WHERE business\_key IS NULL — how many records, which date range?
    
3.  **Root cause**: Trace back through INFORMATION\_SCHEMA.JOBS to find the job that loaded NULL rows. Check source data in GCS/staging for the same NULLs
    
4.  **Isolate**: Are NULLs from a specific source system, date range, or transformation step?
    

**Resolution paths:**

*   **Upstream bug**: Coordinate with source system team to fix and resend. Reload affected partitions
    
*   **Transformation bug**: Fix the Dataflow/dbt logic, validate in staging, reprocess affected date partitions using WRITE\_TRUNCATE with corrected data
    
*   **Source system nulls are expected** (e.g., optional B2B partner ID): Reconsider the schema — the column should not be non-nullable. Document the business rule change
    

**Prevention**: Add a not\_null dbt test on all business key columns, gated in CI before any deploy. Add a pre-load Airflow check using BigQueryCheckOperator that fails if any primary key NULLs are found in staging.

S19. Data Freshness Monitoring Across 200 BigQuery Tables
---------------------------------------------------------

**S19. Design a scalable data freshness monitoring system for 200 BigQuery tables.**

Manual per-table monitoring doesn't scale. Build a **metadata-driven freshness monitoring framework**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Step 1: Maintain a freshness SLA registry table  CREATE TABLE monitoring.table_sla_registry (    project_id STRING,    dataset_id STRING,    table_name STRING,    max_staleness_hours INT64,      -- e.g., 2 for hourly, 25 for daily    severity STRING,                -- 'critical', 'high', 'low'    owner_slack_channel STRING,    is_active BOOL  );  -- Step 2: Freshness check query (runs every 15 min via Cloud Scheduler)  SELECT    r.project_id,    r.dataset_id,    r.table_name,    r.max_staleness_hours,    r.severity,    r.owner_slack_channel,    s.last_modified_time,    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), s.last_modified_time, HOUR) AS hours_stale,    CASE      WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), s.last_modified_time, HOUR) > r.max_staleness_hours      THEN 'STALE' ELSE 'FRESH'    END AS status  FROM monitoring.table_sla_registry r  JOIN `region-us.INFORMATION_SCHEMA.TABLE_STORAGE_BY_PROJECT` s    ON r.project_id = s.project_id    AND r.dataset_id = s.table_schema    AND r.table_name = s.table_name  WHERE r.is_active = TRUE    AND TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), s.last_modified_time, HOUR) > r.max_staleness_hours;   ``

**Step 3**: A Cloud Function reads STALE results, groups by owner\_slack\_channel, and posts consolidated alerts — one Slack message per channel listing all stale tables with their staleness duration. **Step 4**: Publish tables\_stale\_count as a custom Cloud Monitoring metric for trend analysis and executive dashboards.

S20. Alerting for a Streaming Pipeline With <1 Minute Acceptable Lag
--------------------------------------------------------------------

**S20. Design an alerting strategy for a streaming pipeline with <1 minute acceptable lag.**

At sub-minute SLAs, alerting must itself be near-real-time — traditional polling approaches are too slow:​

**Metrics to monitor:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Cloud Monitoring alert policies (set via Terraform)  # Alert 1: Pub/Sub oldest unacked message age > 30 seconds (leading indicator)  metric: pubsub.googleapis.com/subscription/oldest_unacked_message_age  threshold: 30 seconds  duration: 1 minute  alerting_channel: pagerduty-streaming-oncall  # Alert 2: Dataflow system lag > 45 seconds  metric: dataflow.googleapis.com/job/system_lag  threshold: 45 seconds  duration: 2 minutes  alerting_channel: pagerduty-streaming-oncall  # Alert 3: Dataflow data freshness > 60 seconds (end-to-end measurement)  metric: dataflow.googleapis.com/job/data_watermark_age  threshold: 60 seconds  duration: 1 minute  alerting_channel: pagerduty-streaming-oncall  # Alert 4: Dead-letter message count > 0 (any processing failures)  metric: pubsub.googleapis.com/subscription/num_undelivered_messages  filter: subscription_id = "dead-letter-sub"  threshold: 1  alerting_channel: slack-data-engineering   `

**End-to-end latency measurement**: Embed a publish\_timestamp in every Pub/Sub message. In Dataflow, compute CURRENT\_TIMESTAMP - publish\_timestamp for each processed record and publish as a custom metric. This measures true end-to-end latency, not just Pub/Sub or Dataflow individually.

S21. Build a Data Catalog for a 500-Table Data Warehouse with Minimal Manual Effort
-----------------------------------------------------------------------------------

**S21. How do you build a data catalog for a 500-table warehouse with automation?**

Manual cataloguing of 500 tables is unsustainable. Use a **multi-layer automated approach**:

**Layer 1 — Automatic technical metadata (zero effort):** Enable BigQuery's native integration with Data Catalog — it auto-discovers all datasets/tables and populates technical metadata (schema, row count, last modified, column types, sample values) without any manual steps.

**Layer 2 — Automated PII classification:** Configure Cloud DLP to scan all BigQuery tables on a schedule. DLP findings automatically create policy tags in Data Catalog (PII.EMAIL, PII.PHONE, SENSITIVE.FINANCIAL) via the Data Catalog API.

**Layer 3 — Lineage from dbt:** Run dbt docs generate and use the dbt-dataplex integration or custom Python scripts to push dbt model descriptions, column descriptions, and lineage graphs (source → staging → mart) into Data Catalog as lineage entries.

**Layer 4 — Business glossary (semi-automated):** Import existing business definitions from Confluence or a spreadsheet via the Data Catalog API. Assign glossary terms to columns in bulk using the tag template API.

**Layer 5 — Governance workflow:** Any new table deployed via CI/CD triggers a Cloud Build step that checks for minimum catalog completeness (table description, owner tag, PII scan run). Missing metadata fails the deployment.

S22. Handle Schema Drift from a Vendor API
------------------------------------------

**S22. A vendor API changes their response schema without notice. How do you handle schema drift in your pipeline?**

Schema drift is a production reality when consuming third-party APIs. Build **resilience by design**:​

**Defensive parsing in Dataflow:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonclass ResilientParseDoFn(beam.DoFn):      REQUIRED_FIELDS = {'transaction_id', 'amount', 'timestamp'}      OPTIONAL_FIELDS = {'merchant_name', 'category', 'metadata'}      def process(self, element):          record = json.loads(element)          # Hard fail: required fields missing          missing = self.REQUIRED_FIELDS - set(record.keys())          if missing:              yield beam.pvalue.TaggedOutput('dead_letter',                  {'raw': element, 'error': f'Missing required fields: {missing}'})              return          # Graceful handling: new unexpected fields → capture in a JSON blob          known_fields = self.REQUIRED_FIELDS | self.OPTIONAL_FIELDS          new_fields = set(record.keys()) - known_fields          if new_fields:              # Log new fields for schema evolution tracking              log_new_schema_fields(new_fields, source='vendor_api')              record['_extra_fields'] = json.dumps({k: record.pop(k) for k in new_fields})          yield record   `

**Schema evolution strategy:**

*   Store a \_raw\_json column in BigQuery's JSON native type as a safety net — even if parsing breaks, the raw data is preserved for reprocessing
    
*   Run a weekly schema comparison job: compare current API response schema against registered schema; alert if new fields detected so the team can proactively update the pipeline
    
*   Use BigQuery's schema auto-detection with SCHEMA\_UPDATE\_OPTION=ALLOW\_FIELD\_ADDITION for append-only scenarios where new columns are non-breaking
    

S23. BigQuery Table Growing 50GB/Day — Cost and Retention Management
--------------------------------------------------------------------

**S23. A BigQuery table is growing 50GB/day. How do you manage costs and retention?**

50GB/day = ~1.5TB/month = ~18TB/year. At BigQuery active storage pricing of $0.02/GB/month, that's $360/month at 12 months without any retention management. Implement a tiered retention strategy:​

**Step 1 — Partition and set expiration:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Set partition expiration on existing table  ALTER TABLE dataset.events  SET OPTIONS (    partition_expiration_days = 365  -- auto-delete partitions older than 1 year  );   `

**Step 2 — Tiered storage using GCS Lifecycle:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json// Lifecycle policy on the raw GCS backup  {    "lifecycle": {      "rule": [        {"action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},         "condition": {"age": 30}},        {"action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},         "condition": {"age": 90}},        {"action": {"type": "SetStorageClass", "storageClass": "ARCHIVE"},         "condition": {"age": 365}}      ]    }  }   `

**Step 3 — Long-term storage discount:** BigQuery automatically reduces storage cost by 50% (to $0.01/GB/month) for table partitions not modified in 90+ days. Avoid touching old partitions unnecessarily — even SELECT \* doesn't trigger this, but any DML does.

**Step 4 — Summarisation tables:** For data older than 90 days, run a weekly Dataflow job to aggregate raw events into hourly/daily summaries, delete the raw partitions, and retain only summaries. This typically reduces storage by 95%+ for time-series data.

S24. Automated Anomaly Detection on Daily Pipeline Row Counts
-------------------------------------------------------------

**S24. Implement automated anomaly detection on daily pipeline row counts.**

Simple threshold alerting (e.g., "alert if rows < 1M") is fragile — it doesn't account for weekends, holidays, or seasonal patterns. Use **statistical anomaly detection**:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sql-- Store daily row counts in a monitoring table  INSERT INTO monitoring.pipeline_row_counts  SELECT    'orders_daily' AS pipeline_name,    CURRENT_DATE() AS run_date,    COUNT(*) AS row_count,    CURRENT_TIMESTAMP() AS recorded_at  FROM dataset.orders  WHERE DATE(load_date) = CURRENT_DATE();  -- Anomaly detection: z-score vs. rolling 30-day average  WITH stats AS (    SELECT      pipeline_name,      AVG(row_count) AS mean_30d,      STDDEV(row_count) AS stddev_30d    FROM monitoring.pipeline_row_counts    WHERE run_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)      AND run_date < CURRENT_DATE()  -- exclude today    GROUP BY 1  ),  today AS (    SELECT pipeline_name, row_count    FROM monitoring.pipeline_row_counts    WHERE run_date = CURRENT_DATE()  )  SELECT    t.pipeline_name,    t.row_count,    s.mean_30d,    s.stddev_30d,    (t.row_count - s.mean_30d) / NULLIF(s.stddev_30d, 0) AS z_score,    CASE WHEN ABS((t.row_count - s.mean_30d) / NULLIF(s.stddev_30d, 0)) > 3      THEN 'ANOMALY' ELSE 'NORMAL' END AS status  FROM today t JOIN stats s USING (pipeline_name)  WHERE status = 'ANOMALY';   `

A **z-score > 3** (3 standard deviations from the 30-day mean) flags statistically significant anomalies. Run this query after each pipeline completes via Cloud Scheduler → Cloud Function → alert if any rows returned.

S25. Reconciliation Checks Between Cloud SQL and BigQuery
---------------------------------------------------------

**S25. Design reconciliation checks between a Cloud SQL source and BigQuery target.**

Reconciliation validates that your ETL pipeline moved data completely and correctly:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   python# Airflow DAG task: post-load reconciliation  from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator  from airflow.providers.postgres.hooks.postgres import PostgresHook  def reconcile_row_counts(**context):      processing_date = context['ds']  # logical_date      # Source count from Cloud SQL      pg_hook = PostgresHook(postgres_conn_id='cloud_sql_prod')      source_count = pg_hook.get_first(          f"SELECT COUNT(*) FROM orders WHERE DATE(created_at) = '{processing_date}'"      )[0]      # Target count from BigQuery      bq_hook = BigQueryHook()      target_count = bq_hook.get_first(          f"SELECT COUNT(*) FROM `project.dataset.orders` "          f"WHERE DATE(load_date) = '{processing_date}'"      )[0]      # Reconciliation tolerance: 0% for financial data      if source_count != target_count:          raise ValueError(              f"RECONCILIATION FAILED: Source={source_count}, Target={target_count}, "              f"Delta={source_count - target_count} rows for {processing_date}"          )      # Also validate business metrics      source_sum = pg_hook.get_first(          f"SELECT SUM(amount) FROM orders WHERE DATE(created_at) = '{processing_date}'"      )[0]      target_sum = bq_hook.get_first(          f"SELECT SUM(amount) FROM `project.dataset.orders` "          f"WHERE DATE(load_date) = '{processing_date}'"      )[0]      if abs(float(source_sum) - float(target_sum)) > 0.01:          raise ValueError(f"AMOUNT RECONCILIATION FAILED: {source_sum} vs {target_sum}")   ``

Reconcile three things: **row count** (completeness), **sum of key financial metrics** (accuracy), and **max/min of timestamp columns** (no truncation). Write reconciliation results to a BigQuery audit table regardless of pass/fail — this creates a permanent record for regulatory audits.

🔴 Security & Compliance: S26–S40
=================================

S26. GDPR Erasure Request — Deleting a User's Data from BigQuery
----------------------------------------------------------------

**S26. A GDPR right-to-erasure request comes in for a user. How do you delete their data across your BigQuery data platform?**

GDPR Article 17 requires erasure within 30 days. BigQuery's immutable storage model makes this non-trivial — you must have designed for this in advance:

**If crypto-shredding is implemented (ideal):**Delete the user's encryption key from Cloud KMS. All encrypted PII columns for that user are now cryptographically unreadable — erasure complete in seconds. Log the key deletion with timestamp and user\_id in the compliance audit table.

**If crypto-shredding is not implemented:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Step 1: Identify all tables containing the user's data  -- (maintained in a data inventory table)  SELECT DISTINCT table_name, pii_column  FROM data_governance.pii_inventory  WHERE has_user_identifier = TRUE;  -- Step 2: Execute DML erasure on each table  -- (must target specific partitions to reduce cost)  MERGE `project.dataset.events` AS target  USING (SELECT 'user_123' AS user_id) AS source  ON target.user_id = source.user_id  WHEN MATCHED THEN UPDATE SET    email = NULL,    phone = NULL,    ip_address = NULL,    full_name = 'REDACTED',    is_erased = TRUE,    erased_at = CURRENT_TIMESTAMP();   ``

**Process governance:**

*   Assign each erasure request a ticket ID and track status in a compliance management system
    
*   Log every table modified, row count affected, and completion timestamp
    
*   For BigQuery time travel: old snapshots containing the user's PII will automatically expire within 7 days — document this in your GDPR data processor agreement
    
*   Run a post-erasure verification query to confirm PII columns are NULL for the user
    

S27. Column Masking for Contractors Needing Analytics but Not PII
-----------------------------------------------------------------

**S27. How do you grant contractors access to analytics datasets while hiding PII columns?**

Use BigQuery's **column-level security via policy tags** — the cleanest, most maintainable approach:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Terraform: define policy tag taxonomy  resource "google_data_catalog_taxonomy" "pii_taxonomy" {    display_name = "PII Classification"    region       = "australia-southeast1"  }  resource "google_data_catalog_policy_tag" "pii_email" {    taxonomy     = google_data_catalog_taxonomy.pii_taxonomy.name    display_name = "PII.Email"  }  # Grant contractors the ability to see non-PII columns only  # (do NOT grant Fine-Grained Reader role to contractor group)  resource "google_bigquery_dataset_iam_binding" "contractor_viewer" {    dataset_id = "analytics"    role       = "roles/bigquery.dataViewer"    members    = ["group:contractors@company.com"]  }  # Without Fine-Grained Reader on the policy tag,  # contractors see NULL for all tagged PII columns automatically   `

**Result**: Contractors can run SELECT \* FROM analytics.orders — they see all columns, but email, phone, full\_name, and ip\_address return NULL. No SQL changes needed — the masking is enforced at the storage layer transparently.

**Alternative for more complex masking rules** (e.g., show last 4 digits of phone): Create an authorized view that applies explicit masking expressions:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sqlCREATE VIEW analytics_contractor.orders AS  SELECT    order_id,    customer_id,    amount,    CONCAT('***-***-', RIGHT(phone, 4)) AS phone_masked,    REGEXP_REPLACE(email, r'(^[^@]+)', '***') AS email_masked  FROM analytics.orders;   `

S28. Data Breach Incident Response in Your Pipeline
---------------------------------------------------

**S28. A data breach is suspected in your data pipeline — what is your incident response?**

Respond with a structured, documented process — regulators will ask for your incident log:

**Phase 1 — Detect & Contain (0–2 hours):**

1.  Confirm the breach: check Cloud Audit Logs for unusual DATA\_READ events (large exports, off-hours access, unexpected principals)
    
2.  **Immediately revoke suspected compromised credentials**: gcloud iam service-accounts disable \[EMAIL\]
    
3.  Rotate any leaked keys or secrets in Secret Manager
    
4.  Enable VPC Service Controls emergency lockdown if not already in place
    
5.  Preserve evidence: export relevant audit logs to a locked, compliance-project BigQuery dataset before they could be altered
    

**Phase 2 — Assess (2–24 hours):**

1.  Identify: what data was accessed? Which tables, which columns, which users?
    
2.  Quantify: how many records, which individuals affected, what categories of PII?
    
3.  Determine root cause: misconfigured IAM? Compromised service account? Insider threat?
    

**Phase 3 — Notify (24–72 hours for GDPR):**

*   GDPR requires notifying the supervisory authority within 72 hours of becoming aware
    
*   Notify affected individuals if the breach is likely to result in high risk to their rights
    
*   Engage DPO (Data Protection Officer) and legal team
    

**Phase 4 — Remediate and Harden:**

*   Fix the vulnerability (remove overly broad IAM, add VPC Service Controls, enforce MFA)
    
*   Conduct a post-incident review with full timeline
    
*   Update runbooks and automated detection to catch similar patterns faster
    

S29. Multi-Tenant Platform — Clients Cannot See Each Other's Data
-----------------------------------------------------------------

**S29. Design a multi-tenant data platform where each client's data is completely isolated.**

Strong isolation is non-negotiable when clients are competitors or have contractual data segregation requirements:​

**Architecture — Project-per-tenant (strongest isolation):**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   textGCP Organisation  ├── project-client-acme (dedicated project, dedicated billing)  │   ├── BigQuery dataset: acme_raw, acme_analytics  │   ├── GCS bucket: gs://acme-datalake/  │   └── Service Account: acme-pipeline-sa (only has access to ACME project)  ├── project-client-globex  │   ├── BigQuery dataset: globex_raw, globex_analytics  │   └── Service Account: globex-pipeline-sa  └── project-platform-shared      ├── Shared tooling: Composer, CI/CD pipelines      └── Monitoring & governance   `

**Automation:** Use Terraform with a tenant variable to provision new client environments identically. A terraform apply -var="tenant=new\_client" creates the full isolated environment in minutes.

**Cross-cutting governance (without cross-tenant data access):**

*   Billing consolidation via GCP organisation-level billing accounts
    
*   Centralised audit log export from all tenant projects to a **locked compliance project** that no tenant can access
    
*   Shared Data Catalog taxonomy (PII tags) applied consistently across all tenant datasets
    

S30. Audit Logging to Prove Data Access to Regulators
-----------------------------------------------------

**S30. Implement audit logging that proves to regulators who accessed what data and when.**

Regulators (APRA, GDPR supervisory authorities) may request evidence of who accessed PII and when. Build an **immutable, queryable audit trail**:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Enable all three Cloud Audit Log types for BigQuery  gcloud projects set-iam-policy PROJECT_ID policy.json  # policy.json includes:  # "auditLogConfigs": [  #   {"logType": "ADMIN_READ"},  #   {"logType": "DATA_READ"},   ← who queried data  #   {"logType": "DATA_WRITE"}   ← who modified data  # ]  # Export audit logs to a LOCKED BigQuery dataset  gcloud logging sinks create compliance-audit-sink \    bigquery.googleapis.com/projects/compliance-project/datasets/audit_logs \    --log-filter='protoPayload.serviceName="bigquery.googleapis.com"'   `

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Compliance query: who accessed PII tables in the last 30 days  SELECT    timestamp,    protopayload_auditlog.authenticationinfo.principalemail AS user,    protopayload_auditlog.resourcename AS resource,    protopayload_auditlog.methodname AS action,    protopayload_auditlog.requestmetadata.callerip AS source_ip,    JSON_VALUE(protopayload_auditlog.requestjson, '$.query.query') AS sql_query  FROM `compliance_project.audit_logs.cloudaudit_googleapis_com_data_access`  WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)    AND REGEXP_CONTAINS(protopayload_auditlog.resourcename, 'customers|transactions|pii')  ORDER BY timestamp DESC;   ``

**Lock the compliance project**: Apply Organisation Policy constraints/iam.restrictGrantsForConstraints to prevent anyone from granting themselves access to the compliance project. Even GCP project owners cannot self-escalate access.

S31. Cross-Border Data Residency Requirements
---------------------------------------------

**S31. Handle cross-border data residency — EU data must stay in EU.**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Enforce BigQuery dataset location at creation  bq mk --dataset --location=EU project:eu_customer_data  # Organisation Policy to prevent datasets being created in non-approved regions  gcloud org-policies set-policy \    --project=eu-data-project residency-policy.yaml  # residency-policy.yaml:  # constraint: constraints/gcp.resourceLocations  # listPolicy:  #   allowedValues:  #     - in:eu-locations  # europe-west1, europe-west4, EU multi-region only   `

**Pipeline design:** All EU customer data flows through Pub/Sub topics and Dataflow jobs deployed in europe-west1. GCS buckets for EU data are dual-region EUR4. BigQuery datasets are EU multi-region. Never pass EU PII through US-region services — check every GCP service used in the pipeline for its data residency guarantees.

**Contractual:** Document in your data processing agreement exactly which GCP regions process EU data. Use **Assured Workloads** for regulated industries (financial services, healthcare) to enforce regional controls at the infrastructure level and get compliance attestations.

S32. Least-Privilege IAM for a 20-Person Data Team
--------------------------------------------------

**S32. Set up least-privilege IAM for a 20-person team with 5 different roles.**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   text# roles/data-engineer (senior): full read/write on dev, read-only prod  - roles/bigquery.dataEditor → dev-dataset  - roles/bigquery.dataViewer → prod-dataset  - roles/bigquery.jobUser → project level  - roles/dataflow.developer → project level  - roles/storage.objectAdmin → dev-bucket  # roles/data-analyst: read-only on analytics layer (no raw/PII data)  - roles/bigquery.dataViewer → analytics-dataset ONLY  - roles/bigquery.jobUser → project level (billed queries)  # roles/data-scientist: read analytics + write to their own sandbox dataset  - roles/bigquery.dataViewer → analytics-dataset  - roles/bigquery.dataEditor → sandbox-ds-dataset  - roles/aiplatform.user → vertex AI experiments  # roles/pipeline-service-account: per-pipeline SA (automated)  - Specific resource-level IAM only (specific dataset, specific bucket path)  - No human-accessible roles; key-less (Workload Identity)  # roles/data-platform-admin: infra management (Terraform)  - roles/owner → dev project  - roles/editor → staging project  - Via break-glass procedure only → prod project (time-limited, logged)   `

Enforce this via **Terraform** — no manual IAM grants. All changes go through PR review and apply via CI/CD. Run gcloud asset search-all-iam-policies weekly to detect manual IAM drift.

S33. Production Data Masking for Dev Environments
-------------------------------------------------

**S33. Implement data masking when loading production data into a development environment.**

**Never copy raw production PII to dev** — use a Cloud DLP-based de-identification pipeline:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Dataflow pipeline: prod → masked dev copy  import apache_beam as beam  from apache_beam.io.gcp.bigquery import ReadFromBigQuery, WriteToBigQuery  class MaskPIIDoFn(beam.DoFn):      def __init__(self):          self.dlp_client = None      def setup(self):          from google.cloud import dlp_v2          self.dlp_client = dlp_v2.DlpServiceClient()      def process(self, element):          # Replace PII fields with realistic fake data          import hashlib, random          masked = dict(element)          if 'email' in masked and masked['email']:              # Deterministic masking: same input → same output (preserves join keys)              hash_val = hashlib.md5(masked['email'].encode()).hexdigest()[:8]              masked['email'] = f"user_{hash_val}@example.com"          if 'phone' in masked and masked['phone']:              masked['phone'] = f"04{random.randint(10000000, 99999999)}"          if 'full_name' in masked and masked['full_name']:              masked['full_name'] = 'Test User'          yield masked   `

Run this pipeline weekly to refresh the dev dataset. Use **deterministic masking** (hash-based) for fields used as join keys — the same customer\_id maps to the same masked email consistently, so joins work in dev without exposing real PII.

S34. Service Account Key Accidentally Committed to GitHub
---------------------------------------------------------

**S34. A service account key was accidentally committed to GitHub. What do you do immediately?**

This is a **security incident** requiring immediate response — treat every second as the key being actively exploited:​

**Immediate actions (within 5 minutes):**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Step 1: Disable the key IMMEDIATELY (before deleting — disabling is faster)  gcloud iam service-accounts keys disable KEY_ID \    --iam-account=compromised-sa@project.iam.gserviceaccount.com  # Step 2: Delete the key entirely  gcloud iam service-accounts keys delete KEY_ID \    --iam-account=compromised-sa@project.iam.gserviceaccount.com  # Step 3: Check audit logs for any usage of this key in the last 24 hours  # Filter by the key's unique_id in Cloud Audit Logs   `

**Within 30 minutes:**

1.  Remove the key from Git history using git filter-branch or BFG Repo Cleaner — even after removal, assume it was cached by GitHub's secrets scanning and any forks
    
2.  Check if the repository was public — if yes, treat as fully compromised
    
3.  Review Cloud Audit Logs for any API calls made with this key since the commit timestamp
    
4.  Rotate any downstream secrets or tokens that the service account had access to
    

**Prevention:**

*   Enable **GitHub Secret Scanning** + git-secrets pre-commit hook on all repositories
    
*   Use **Workload Identity Federation** instead of service account keys — no downloadable keys, ever
    
*   Enforce an organisation policy constraints/iam.disableServiceAccountKeyCreation for all production projects
    

S35. Secrets Rotation with Zero Downtime
----------------------------------------

**S35. Design a secrets rotation strategy for pipeline credentials with zero downtime.**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Secret Manager rotation using versioning (not replacement)  from google.cloud import secretmanager  def rotate_secret(secret_id: str, new_value: str):      client = secretmanager.SecretManagerServiceClient()      parent = f"projects/my-project/secrets/{secret_id}"      # Add new version (doesn't break existing consumers using 'latest')      new_version = client.add_secret_version(          parent=parent,          payload={"data": new_value.encode()}      )      # Test new version works (e.g., test DB connection)      if test_connection(new_value):          # Disable old version (keep for rollback window)          client.disable_secret_version(name=f"{parent}/versions/PREVIOUS")      else:          # Rollback: disable new version          client.disable_secret_version(name=new_version.name)          raise RuntimeError("New secret version failed validation — rolling back")   `

**Pipeline consumer pattern:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Always fetch 'latest' version — picks up rotated secret automatically  def get_secret(secret_id: str) -> str:      client = secretmanager.SecretManagerServiceClient()      name = f"projects/my-project/secrets/{secret_id}/versions/latest"      response = client.access_secret_version(name=name)      return response.payload.data.decode()  # Fetch at task execution time, not at import time  # This means rotating the secret doesn't require redeploying pipelines   `

Implement a **dual-write window**: keep both old and new versions active for 1 hour during rotation. This allows in-flight pipeline runs using the old secret to complete gracefully while new runs pick up the new secret.

🟠 Performance: S36–S55
=======================

S36. BigQuery Query Gone from 30 Seconds to 15 Minutes — Diagnose It
--------------------------------------------------------------------

**S36. A BigQuery query that used to take 30 seconds now takes 15 minutes. How do you diagnose and fix it?**

**Systematic diagnosis:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Step 1: Find the slow job and compare to historical runs  SELECT    job_id,    creation_time,    TIMESTAMP_DIFF(end_time, start_time, SECOND) AS duration_s,    total_bytes_billed,    total_slot_ms,    -- Check for query plan changes    query  FROM `region-us.INFORMATION_SCHEMA.JOBS`  WHERE query LIKE '%my_slow_query_identifier%'  ORDER BY creation_time DESC  LIMIT 20;   ``

**Common root causes and fixes:**

Root CauseDiagnosis SignalFixData volume explosiontotal\_bytes\_billed 10x higher than usualAdd/fix partition filterPartition pruning brokenBytes billed = full table scanEnsure filter uses partition column directly, not inside a functionNew cross join or cartesian productQuery plan shows "BROADCAST" on large tableFix accidental cross join in SQLSlot contentiontotal\_slot\_ms similar but duration longerOther jobs competing for slots; add reservationSkewed dataOne worker stage takes 10x longerAdd Reshuffle or pre-aggregate skewed keySchema change added large columnBytes billed increasedRemove new large column from SELECTStatistics stalenessN/A in BQ (always fresh)Not applicable — BQ uses live stats

Check the **Query Execution Plan** in BigQuery console (Execution Details tab) — it shows each stage's input/output bytes and slot consumption, making the bottleneck visually obvious.

S37. BigQuery Table for 10B Rows of IoT Sensor Data
---------------------------------------------------

**S37. Design a BigQuery table structure for 10 billion rows of IoT sensor data, queried by device and date.**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   sqlCREATE TABLE iot.sensor_readings (    -- Partition column: most queries filter by date    reading_date DATE NOT NULL,    -- Cluster columns: most queries also filter by device_id and metric_type    device_id STRING NOT NULL,    metric_type STRING NOT NULL,    -- Measurement fields    timestamp TIMESTAMP NOT NULL,    value FLOAT64,    unit STRING,    quality_flag INT64,    -- Metadata    site_id STRING,    firmware_version STRING,    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()  )  PARTITION BY reading_date  CLUSTER BY device_id, metric_type, site_id  OPTIONS (    partition_expiration_days = 730,  -- 2-year retention    require_partition_filter = TRUE   -- prevent full-table scans  );   `

**Why this design:**

*   Partitioning on reading\_date means queries filtered by date range only scan relevant partitions (most IoT queries are time-bounded)
    
*   Clustering on device\_id, metric\_type means queries for a specific device + metric type scan only contiguous storage blocks within the partition — BigQuery skips non-matching blocks
    
*   require\_partition\_filter = TRUE prevents accidental full 10B-row scans — analysts must always include a date filter
    
*   At 10B rows with 10 fields, a single day's partition might be ~50GB — manageable and cheap to query
    

S38. Optimise Dataflow Processing 1M Events/Second at p99 <500ms
----------------------------------------------------------------

**S38. How do you architect a Dataflow streaming pipeline to process 1 million events/second with p99 latency under 500ms?**

At 1M events/sec, every millisecond of per-element overhead compounds massively. The architecture must be **horizontally scalable and stateless by design**:​

**Pipeline design principles:**

*   **Minimise stateful operations**: Stateful transforms (GroupByKey, windows) have higher latency. Push state to Bigtable (external, fast lookups) rather than accumulating in Dataflow windows
    
*   **Use Streaming Engine**: Offloads window state from workers, enabling aggressive autoscaling without memory OOM
    
*   **Fuse aggressively but break hot fusions**: Let Dataflow fuse simple transforms (parse → validate → enrich) into single stages, but add Reshuffle before any GroupByKey to distribute load
    

**Infrastructure settings:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonoptions = PipelineOptions([      '--runner=DataflowRunner',      '--enable_streaming_engine',      '--streaming',      '--autoscalingAlgorithm=THROUGHPUT_BASED',      '--maxNumWorkers=200',      '--machine_type=n1-standard-8',     # 8 vCPU per worker for parallel DoFn threads      '--numberOfWorkerHarnessThreads=40', # 40 threads per worker      '--experiments=enable_recommendations',      '--experiments=min_num_workers=10',  # minimum to handle bursts quickly  ])   `

**Latency monitoring**: Set a Cloud Monitoring alert on dataflow.googleapis.com/job/system\_lag > 300ms (leaving 200ms buffer to p99 SLA). At 1M/sec, a single slow DoFn (database call, API call) will bottleneck thousands of records — profile with Cloud Profiler and eliminate all synchronous I/O from hot paths.

S39. Airflow Scheduler Overloaded with 50 Parallel DAG Tasks
------------------------------------------------------------

**S39. A nightly Composer DAG with 50 parallel tasks is overloading the Airflow scheduler. How do you fix it?**

The Airflow scheduler parses DAGs, evaluates task states, and schedules tasks — it's CPU-bound for complex DAGs with many concurrent tasks:​

**Diagnosis:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Check scheduler heartbeat metric in Cloud Monitoring  # metric: airflow.googleapis.com/environment/scheduler/heartbeat_age  # If > 10 seconds, scheduler is overloaded   `

**Fixes in order of impact:**

1.  **Use deferrable operators**: Replace BigQueryInsertJobOperator with its deferrable version — it releases the worker slot while waiting for BigQuery to complete. 50 tasks → 50 fewer occupied workers → scheduler processes queue faster
    
2.  **Limit parallelism with pools:**
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Create a pool limiting BigQuery concurrency  # airflow pools set bigquery_pool 20 "Max 20 concurrent BQ jobs"  task = BigQueryInsertJobOperator(      task_id='process_partition',      pool='bigquery_pool',  # max 20 concurrent regardless of DAG parallelism      ...  )   `

1.  **Break the monolithic DAG** into smaller DAGs using TriggerDagRunOperator — 50-task DAG → 5 DAGs of 10 tasks each reduces scheduler cognitive load
    
2.  **Upgrade to Composer 2/3**: Uses GKE Autopilot with horizontal scheduler scaling — multiple scheduler replicas handle the load
    
3.  **Optimise DAG file parsing**: Reduce dag\_file\_processor\_timeout and use eager\_loading=False on variable-heavy DAGs
    

S40. Cost-Efficient Architecture for a Startup with Unpredictable Workloads
---------------------------------------------------------------------------

**S40. Design a cost-efficient GCP data architecture for a startup with unpredictable, bursty workloads.**

Startups need to avoid paying for idle capacity while handling occasional large spikes:​

**Serverless-first architecture:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   textIngestion:    Cloud Functions (trigger-based, pay-per-invocation) + Pub/Sub  Processing:   Dataflow (autoscaling, pay per worker-hour) or                Cloud Run jobs (for batch, scales to zero)  Storage:      BigQuery (serverless) + GCS Standard  Orchestration: Cloud Scheduler + Cloud Tasks (no always-on Composer)  BI:           Looker Studio (free) connecting to BigQuery   `

**Cost controls:**

*   BigQuery: on-demand pricing (no committed slots needed at startup scale)
    
*   Dataflow: --maxNumWorkers=5 cap to prevent runaway scaling
    
*   No Cloud Composer until workloads justify it (~$300/month minimum) — use Cloud Scheduler + Cloud Run for orchestration
    
*   GCS: Standard class only until data is confirmed stable; lifecycle rules after 3 months
    
*   Use **BigQuery sandbox** for development (no cost for storage <10GB, 1TB free queries/month)
    
*   Budget alerts: set gcloud billing budgets create at $500/month with email alerts at 50%, 90%, 100%
    

**Scale trigger**: When monthly BigQuery costs exceed $500, evaluate switching to Standard Edition reservations. When orchestration needs grow beyond 5 scheduled pipelines, introduce Composer.

S41–S45. Performance Scenarios (Detailed)
-----------------------------------------

**S41. BigQuery job using 90% of project slot quota — blocking other users:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   sql-- Identify the offending job  SELECT job_id, user_email, total_slot_ms, query  FROM `region-us.INFORMATION_SCHEMA.JOBS`  WHERE state = 'RUNNING'  ORDER BY total_slot_ms DESC LIMIT 5;  -- Cancel it if necessary  CALL BQ.JOBS.CANCEL('project:region.job_id');   ``

Implement **workload management reservations**: Create a PRODUCTION reservation (guaranteed 200 slots) and an ADHOC reservation (20 slots, on-demand burst). Assign production pipelines to PRODUCTION and analysts to ADHOC — analysts can never starve production jobs.​

**S42. Dataflow join — 1TB stream vs. 10GB dimension table:**Load the 10GB dimension table as a **SideInput** (broadcast join). Dataflow loads the entire dimension table into each worker's memory once, then processes stream elements locally without a shuffle. If 10GB is too large for memory, use Bigtable as an external lookup store — stream elements call Bigtable for dimension lookups at <10ms latency.​

**S43. Cloud Function timing out on large GCS files:**Cloud Functions have a 9-minute maximum timeout. Redesign the trigger pattern: GCS object → Cloud Function validates file metadata (size, name) → if file > threshold, publish a message to Pub/Sub → Dataflow reads the full file for processing. The Cloud Function becomes a lightweight router, not a data processor. For files up to a few GB, switch to Cloud Run Jobs (no timeout limit, up to 24 hours).​

**S44. Reduce BigQuery monthly bill by 40%:**

1.  Enable require\_partition\_filter on all large tables — prevents accidental full scans (often accounts for 30-50% of wasted cost)
    
2.  Audit INFORMATION\_SCHEMA.JOBS for top 10 most expensive queries — optimise those first (80/20 rule)
    
3.  Replace COUNT(DISTINCT) with APPROX\_COUNT\_DISTINCT in dashboards
    
4.  Set custom user quotas for analysts: gcloud bigquery update-project --max-bytes-billed-per-query=10GB
    
5.  Switch frequently-queried dashboard tables to materialised views​
    

**S45. Caching layer for repeated identical BigQuery queries:**BigQuery has a built-in **query result cache** (free) that serves identical queries from cache for 24 hours — no configuration needed, just ensure useQueryCache: true (default). For longer caching or more control: use BigQuery **BI Engine** (in-memory acceleration for up to 250GB) for dashboard tools. For application-level caching: store query results in Memorystore (Redis) with a 1-hour TTL, keyed by query hash.

🔵 Migration & Integration: S46–S65
===================================

S46. Migrate Spark on Dataproc to Apache Beam on Dataflow
---------------------------------------------------------

**S46. How do you migrate a Spark pipeline running on Dataproc to Apache Beam on Dataflow?**

This is a common modernisation task — Dataflow reduces operational overhead (no cluster management) and has better GCP integration:​

**Migration mapping:**

Spark ConceptBeam EquivalentSparkContext / SparkSessionbeam.PipelineRDD / DataFramePCollectionmap()beam.Map()flatMap()beam.FlatMap()filter()beam.Filter()groupByKey()beam.GroupByKey()reduceByKey()beam.CombinePerKey()join()beam.CoGroupByKey() or SideInputspark.read.parquet()beam.io.ReadFromParquet()df.write.bigquery()beam.io.WriteToBigQuery()

**Migration strategy:**

1.  Start with the simplest pipeline (fewest transformations)
    
2.  Write Beam version in Python/Java, run with DirectRunner and compare output to Spark output on the same sample dataset
    
3.  Validate on Dataflow with a 1-day historical dataset
    
4.  Run Spark and Dataflow in parallel for one week, compare outputs
    
5.  Cut over to Dataflow, decommission Dataproc cluster
    

**When NOT to migrate**: Spark MLlib pipelines with custom ML logic — Vertex AI + BigQuery ML may be a better target than Beam. Also, complex Spark SQL with 200-line queries — keep on Dataproc or migrate directly to BigQuery.

S47. Legacy SFTP File Feed into a Modern GCP Pipeline
-----------------------------------------------------

**S47. How do you integrate a legacy SFTP file feed into a GCP data pipeline?**

SFTP is common in financial services, healthcare, and government integrations:​

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Cloud Run Job: SFTP poller (scheduled via Cloud Scheduler)  import paramiko  from google.cloud import storage  def poll_sftp_and_upload():      ssh = paramiko.SSHClient()      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())      ssh.connect(          hostname=SFTP_HOST,          username=SFTP_USER,          pkey=paramiko.RSAKey.from_private_key_file('/secrets/sftp_key')      )      sftp = ssh.open_sftp()      gcs_client = storage.Client()      bucket = gcs_client.bucket('landing-zone')      for filename in sftp.listdir('/outbound/'):          if filename.endswith('.csv') and filename not in get_processed_files():              local_path = f'/tmp/{filename}'              sftp.get(f'/outbound/{filename}', local_path)              # Upload to GCS landing zone              blob = bucket.blob(f'sftp/{datetime.today().strftime("%Y/%m/%d")}/{filename}')              blob.upload_from_filename(local_path)              # Mark as processed (in Cloud Firestore)              mark_file_processed(filename)      sftp.close()      ssh.close()   `

**Full pipeline**: Cloud Scheduler (every 15 min) → Cloud Run Job (SFTP poll + GCS upload) → GCS object finalise event → Eventarc → Cloud Function (trigger validation) → Dataflow (transform + load) → BigQuery. Store SFTP keys in Secret Manager, never in code or environment variables.

S48. Salesforce CRM Data to BigQuery
------------------------------------

**S48. How do you connect Salesforce CRM data to BigQuery for sales analytics?**

Multiple options depending on freshness and complexity requirements:​

**Option 1 — BigQuery Data Transfer Service (simplest):**Native Salesforce connector syncs standard Salesforce objects (Accounts, Contacts, Opportunities) to BigQuery on a configurable schedule (hourly minimum). Zero code, but limited to standard objects and no complex transformations.

**Option 2 — Fivetran/Stitch/Airbyte (managed ETL):**Fully managed SaaS connectors handle Salesforce API pagination, rate limiting, and incremental sync. Data lands in BigQuery as raw tables. dbt transforms it into analytics models. Best for teams without Salesforce API expertise.

**Option 3 — Custom Dataflow pipeline (most control):**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Read from Salesforce REST API with pagination  import simple_salesforce  class SalesforceReadDoFn(beam.DoFn):      def setup(self):          self.sf = Salesforce(              username=get_secret('sf_username'),              password=get_secret('sf_password'),              security_token=get_secret('sf_token')          )      def process(self, query_date):          # SOQL query with incremental load          records = self.sf.query_all(              f"SELECT Id, Name, Amount, StageName, CloseDate "              f"FROM Opportunity WHERE LastModifiedDate >= {query_date}"          )          for record in records['records']:              yield record   `

Use Option 2 for most client engagements — it handles Salesforce API complexity (OAuth, bulk API, API version changes) and lets you focus on the analytics layer.

S49. Migrate Airflow DAGs from Composer 1 to Composer 2
-------------------------------------------------------

**S49. How do you migrate Cloud Composer 1 DAGs to Composer 2?**

Composer 2 uses GKE Autopilot instead of GKE Standard, has a different airflow.cfg structure, and supports deferrable operators:​

**Migration checklist:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Step 1: Export Composer 1 environment config  gcloud composer environments describe my-composer-1 \    --location australia-southeast1 \    --format json > composer1_config.json  # Step 2: Create Composer 2 environment  gcloud composer environments create my-composer-2 \    --location australia-southeast1 \    --image-version composer-2.9.0-airflow-2.9.3 \    --environment-size medium  # Step 3: Migrate configurations  # - Airflow Variables: export from Composer 1 UI, import to Composer 2  # - Connections: recreate using Secret Manager backend in Composer 2  # - PyPI packages: update requirements.txt (some packages renamed in Airflow 2.x)   `

**DAG compatibility issues to fix:**

*   airflow.contrib.\* providers → airflow.providers.google.\* (Airflow 2.x naming)
    
*   execution\_date → logical\_date (soft deprecation, still works but update)
    
*   PythonOperator with provide\_context=True → removed in Airflow 2.x, use \*\*context directly
    
*   Celery-specific configs (worker concurrency) → replaced by GKE Autopilot worker pod settings
    

**Cutover**: Run both environments in parallel for 2 weeks. DAGs deployed to both, compare execution results. Cut over by updating the Cloud Scheduler triggers to point to Composer 2 endpoints.

S50. Integrate a Real-Time ML Model Prediction into a Streaming Dataflow Pipeline
---------------------------------------------------------------------------------

**S50. How do you call a Vertex AI model endpoint from within a Dataflow streaming pipeline?**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonfrom google.cloud import aiplatform  import apache_beam as beam  class PredictWithVertexAIDoFn(beam.DoFn):      def __init__(self, endpoint_id: str, project: str, location: str):          self.endpoint_id = endpoint_id          self.project = project          self.location = location      def setup(self):          # Initialise client once per worker          aiplatform.init(project=self.project, location=self.location)          self.endpoint = aiplatform.Endpoint(self.endpoint_id)      def process(self, element):          # Build feature vector          instance = {              "transaction_amount": element['amount'],              "merchant_category": element['merchant_cat'],              "hour_of_day": element['hour'],              "velocity_1h": element['txn_count_1h']          }          # Call Vertex AI online prediction endpoint          prediction = self.endpoint.predict(instances=[instance])          fraud_score = prediction.predictions[0]['fraud_probability']          yield {              **element,              'fraud_score': fraud_score,              'is_high_risk': fraud_score > 0.85          }   `

**Performance considerations**: Online prediction endpoints add ~20–100ms latency per call. For high-throughput pipelines, batch prediction calls: accumulate elements into batches of 100 using beam.BatchElements(), then call the endpoint with instances=\[...\] (up to 1000 instances per request). This reduces API overhead by 100x.

S51–S55. Migration Scenarios (Detailed Summaries)
-------------------------------------------------

**S51. Vendor delivers data via email attachments — automate ingestion:**Set up a Gmail API integration or use Cloud Run to poll a dedicated Gmail inbox. New emails → extract attachment → validate (filename pattern, size) → upload to GCS landing zone → trigger Dataflow pipeline. Alternatively, ask the vendor to SFTP or use a direct API integration — email-based data delivery is fragile and should be treated as a temporary measure with a migration timeline.

**S52. Migrate 5 years of historical data from S3 to GCS with transformation:**Use **Storage Transfer Service** for bulk S3 → GCS transfer (handles parallel transfer, checksum validation, rate limiting). For transformation during migration: run a Dataflow pipeline that reads from S3 source bucket, applies transformations (schema normalisation, format conversion to Parquet), and writes to GCS destination. Process year-by-year to validate before proceeding. Estimated throughput: Storage Transfer Service can handle TBs/hour.

**S53. API-to-BigQuery ingestion pipeline for a paginated REST API:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Cloud Run Job with pagination handling  def fetch_all_pages(base_url: str, headers: dict) -> list:      results = []      next_url = base_url      while next_url:          response = requests.get(next_url, headers=headers)          data = response.json()          results.extend(data['items'])          next_url = data.get('next_page_url')  # None when last page          time.sleep(0.1)  # respect rate limits      return results   `

Store the last updated\_at timestamp in Secret Manager/Firestore as a high-watermark for incremental loads. Schedule via Cloud Scheduler, write results to GCS as JSONL → BigQuery load job.

**S54. Integrate GA4 data with internal CRM data in BigQuery:**GA4 has a native BigQuery export — enable it in Firebase/GA4 console, data arrives in analytics\_PROPERTY\_ID dataset daily. Join with CRM data using user\_pseudo\_id (GA4's anonymised user ID) mapped to internal CRM user\_id via a cross-reference table built from first-party login events.

**S55. Connect on-premises Oracle to BigQuery via Datastream:**Install the Datastream connectivity agent on-premises (or use a Cloud VPN tunnel). Create a Datastream connection profile pointing to Oracle. Configure LogMiner CDC on Oracle (SUPPLEMENTAL LOG DATA). Create a Datastream stream: Oracle → GCS (in Avro format) → BigQuery (using Datastream's native BigQuery destination). Datastream handles schema mapping, type conversion, and CDC event merge automatically.

🟣 Team & Delivery: S56–S75
===========================

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Team & Delivery ---------------   `

S56. Onboard a new data engineer to a complex GCP project
---------------------------------------------------------

Start with context, not code. Give them a simple architecture map, the domain glossary, the top 3 pipelines, and access to a dev environment first. Pair them with a buddy, then give one low-risk task such as a dbt model change or a small Airflow fix so they learn the delivery standards, CI/CD, and review process quickly. The goal is to move them from observation to safe ownership in 2–4 weeks.​

S57. Two engineers are duplicating work
---------------------------------------

I would stop the duplication by making ownership explicit. Re-scope work into named workstreams, assign one owner per deliverable, and document interfaces and dependencies in a shared board. Then I’d turn the overlap into a design review so the team can choose one approach and preserve the best ideas.

S58. An external dependency is blocking the deadline
----------------------------------------------------

First, quantify the impact: what is blocked, by how long, and what the minimum viable scope is. Then escalate early with options, not just problems: wait, replace the dependency, or reduce scope. Good project leadership is about giving stakeholders a decision, not surprises.

S59. Prioritise 30 tasks with limited capacity
----------------------------------------------

I’d rank work by business value, urgency, risk, and dependency unlocks. Then I’d separate tasks into must-do, should-do, and can-wait, and use a visible backlog with explicit trade-offs. For client work, I’d confirm priorities with the sponsor so the team is not optimising in a vacuum.

S60. The client does not trust the new warehouse
------------------------------------------------

Treat this as a trust and governance problem, not a SQL problem. Reconcile key numbers from source to warehouse, document business definitions, and show lineage from raw to curated layers. Then publish a certified view or semantic layer so the client has one agreed source of truth.

S61. Run a sprint retrospective for a data engineering team
-----------------------------------------------------------

I’d focus on delivery flow, technical quality, and handoffs. Ask what slowed us down, what caused defects, and what we should stop doing immediately. End with one or two measurable actions only, such as better test coverage, stronger definitions of done, or improved monitoring.

S62. Estimate a 3-month data lake project
-----------------------------------------

I’d estimate in phases: discovery, design, ingestion, transformation, testing, and handover. Then I’d map each source by complexity, data quality, and integration method, and include contingency for unknowns. For consulting, I’d also estimate client effort, dependencies, and decision points.

S63. Knowledge transfer when a key engineer leaves
--------------------------------------------------

Capture their context before they leave: pipeline diagrams, runbooks, gotchas, access paths, and incident history. Then pair them with successors on the most critical areas and record walkthroughs. I’d also turn tribal knowledge into docs, tests, and alerts so the team is not dependent on one person.

S64. Design a technical interview process for a mid-level GCP data engineer
---------------------------------------------------------------------------

Use a balanced process: a SQL/pipeline screen, a GCP architecture discussion, and a scenario-based stakeholder round. I’d test practical skills like BigQuery modelling, Dataflow design, Airflow orchestration, and debugging. For a mid-level hire, I’d look for solid execution and good judgement more than niche depth.

S65. Mentor a junior engineer writing inefficient SQL
-----------------------------------------------------

I’d first explain the query cost and why it matters. Then I’d show them how partitioning, clustering, column pruning, and join order affect performance. The best mentoring style is to pair on one real query and make the improvement visible in both cost and runtime.

S66. Retail client with 1000 stores sending hourly sales data
-------------------------------------------------------------

Use a store-level ingest path into Pub/Sub or GCS, then land the data in BigQuery partitioned by business date and clustered by store and product. Add validation and deduplication before the curated layer so store outages or duplicate files don’t poison reporting. If BI freshness matters, keep a near-real-time aggregate table for daily trade decisions.​

S67. Build a near-real-time recommendation engine pipeline
----------------------------------------------------------

I’d separate feature generation, online serving, and offline training. Streaming events go through Pub/Sub and Dataflow, features are written to BigQuery and an online store, and model scoring happens through Vertex AI or a similar low-latency service. The key is keeping feature definitions consistent between training and serving.

S68. Multi-cloud data architecture with GCP and Azure
-----------------------------------------------------

Choose a source-of-truth strategy first, then minimise data movement. Keep domain-owned data in the native cloud where it is produced, and expose governed access through replicated curated datasets or federated query only where needed. For cross-cloud analytics, define clear residency, latency, and cost rules so the architecture does not drift into expensive sprawl.

S69. Lakehouse with Apache Iceberg on GCS and BigQuery
------------------------------------------------------

Use GCS as the open storage layer and Iceberg as the table format for ACID, schema evolution, and time travel. BigQuery can query the table natively, while other engines like Spark can also read it, which reduces lock-in. This is a good fit when you need both warehouse simplicity and open-table interoperability.​

S70. Pipeline for 10 years of stock market data
-----------------------------------------------

I’d store raw historical data in GCS, curate it into partitioned BigQuery tables, and create summary tables for backtesting workloads. Since historical data is huge, I’d optimise for partition pruning, compression, and pre-aggregated time windows. If the model needs tick-level data, I’d separate raw archival storage from analytical marts.

S71. Data product serving batch analytics and real-time API requests
--------------------------------------------------------------------

Use a dual-path architecture: batch data lands in BigQuery for analytics, while a streaming path publishes the same events into a low-latency serving store. Make sure both paths share the same business definitions so the API and the dashboard agree. That avoids the classic “real-time and batch numbers don’t match” problem.

S72. Scale a startup platform from 0 to 1B events/month
-------------------------------------------------------

Start serverless and simple: Pub/Sub, Dataflow, BigQuery, and Cloud Run or Composer only when needed. Add cost controls early, because growth usually arrives unevenly. Design for replay, observability, and schema evolution from day one so the platform can absorb spikes without a redesign.​

S73. Self-healing pipeline
--------------------------

A self-healing pipeline detects common failures, retries safely, and quarantines bad data instead of stopping everything. I’d use idempotent loads, dead-letter handling, automated rollback, and alerting on repeated failures. The important part is distinguishing transient errors from true data quality problems.

S74. Federated query across BigQuery, Cloud SQL, and Bigtable
-------------------------------------------------------------

Use each system for what it is best at. BigQuery handles large analytical joins, Cloud SQL holds transactional data, and Bigtable serves low-latency key lookups. I’d minimise runtime federated joins and instead materialise the most commonly used integration layer into BigQuery.

S75. Process unstructured PDFs and load extracted data into BigQuery
--------------------------------------------------------------------

I’d use OCR or document extraction first, then normalise the output into structured fields. After extraction, apply validation and confidence thresholds before writing to BigQuery. Keep the raw document and the extracted text so the process is auditable and reprocessable.

Advanced Architecture
---------------------

S76. Sell data products to external clients
-------------------------------------------

Build a productised data sharing model with contracts, SLAs, curated datasets, and strict access control. Expose data through authorized views or controlled exports, and make usage measurable for billing and support. Treat the consumer experience as a product, not just a database.

S77. Feature pipeline for ML training with point-in-time correctness
--------------------------------------------------------------------

Store feature snapshots with timestamps and generate training datasets using the feature values available at that time, not the future. This prevents label leakage and keeps offline training aligned with online serving. BigQuery is often the best offline store for this pattern.

S78. Event-driven microservices data platform
---------------------------------------------

Use Eventarc or Pub/Sub to capture service events, Cloud Run for lightweight processing, and BigQuery for analytical storage. Keep services decoupled and make every consumer idempotent. This gives low operational overhead and good extensibility.

S79. Correlate logs with business metrics
-----------------------------------------

Export logs to BigQuery or use log-based metrics, then join operational signals with business tables such as orders, revenue, or conversion. This is useful for answering questions like “Did the outage affect revenue?” in a measurable way. The key is consistent timestamps and good incident tagging.

S80. Data mesh architecture for 10 business domains
---------------------------------------------------

Use domain-owned datasets and pipelines, with shared platform standards for IAM, CI/CD, cataloguing, and quality checks. Centralise governance, not ownership. If you do this well, each domain can move independently without breaking company-wide standards.

S81. Cost attribution system
----------------------------

Enable billing export to BigQuery, require job labels, and aggregate costs by team, environment, and application. Then publish chargeback reports and alerts for abnormal usage. This makes cost visible and changes team behaviour quickly.

S82. Pipeline resilient to regional outage
------------------------------------------

Design for regional failover with replicated storage, reproducible infrastructure, and defined recovery runbooks. Keep critical datasets and backups in a secondary region and test failover regularly. Resilience is not only technology; it also depends on whether the team has practised recovery.

S83. Synthetic data generation pipeline
---------------------------------------

Generate realistic but non-sensitive data using business rules and distributions that match production patterns. Use it for development, testing, and load validation. Synthetic data is especially useful when real data is restricted by privacy or compliance.

S84. Bank regulatory reporting pipeline
---------------------------------------

Separate raw ingestion, controlled transformations, and immutable reporting outputs. Every report should be reproducible, auditable, and traceable back to source data and logic. For regulators, lineage and versioning matter as much as result accuracy.

S85. Structured CSV and semi-structured JSON from the same source
-----------------------------------------------------------------

Land both formats in the raw zone, then normalise them into a common canonical model. JSON fields can be captured in a flexible structure while CSV maps into fixed columns. A canonical model keeps downstream consumers from dealing with source quirks.

S86. Streaming aggregation without a database
---------------------------------------------

Use streaming windows and stateful aggregation in Dataflow, then write periodic results to a durable store. Keep the state small and the aggregation logic simple. This is good for rolling counters, near-real-time dashboards, and operational metrics.

S87. Build observability from scratch using open-source tools on GCP
--------------------------------------------------------------------

Combine logs, metrics, and traces with structured events, then push them to Cloud Logging, Cloud Monitoring, and Cloud Trace. Use open-source instrumentation like OpenTelemetry for consistency. Good observability tells you what broke, where, and why.

S88. Handle 100 GB files arriving in GCS
----------------------------------------

Do not process the whole file in a single memory-bound step. Split, stream, or chunk the data, then process it with distributed workers such as Dataflow. Large-file processing should be designed around parallelism and failure recovery.

S89. Multi-environment platform with Terraform and CI/CD
--------------------------------------------------------

Use reusable Terraform modules and separate state for dev, staging, and prod. Promote changes through Git-based CI/CD with approvals and tests. That gives repeatability, auditability, and fewer environment drift problems.

S90. Black Friday data platform
-------------------------------

Plan for 5x to 10x traffic and define the burst path before the event. Increase autoscaling limits, pre-warm critical jobs, and monitor lag and slot usage closely. You want graceful degradation, not a platform collapse.

S91. Detect statistical anomalies in KPIs
-----------------------------------------

Track daily metrics against rolling baselines and trigger alerts when deviation crosses a threshold such as a z-score of 3. Pair this with business context, because some “anomalies” are expected seasonal changes. The goal is to detect genuine incidents, not create alert fatigue.

S92. Data governance framework for 50 engineers across 5 teams
--------------------------------------------------------------

Define ownership, naming standards, security controls, data contracts, and quality gates centrally. Let teams build independently inside that framework. Governance should reduce ambiguity, not slow everything down.

S93. Incrementally sync a 10TB Cloud SQL table to BigQuery
----------------------------------------------------------

Use CDC through Datastream or a similar log-based approach rather than repeated full extracts. Then apply deduplication and merge logic in BigQuery. This keeps latency low and avoids huge reprocessing costs.

S94. Real-time logistics dashboard for 10,000 trucks
----------------------------------------------------

Use streaming ingestion for truck telemetry, then aggregate by geography, trip, and status in near real time. Add partitioning and clustering for the historical warehouse layer, and keep a fast serving store for the live map view. The dashboard should prioritise freshness and reliability over perfect historical detail.

S95. Join streaming IoT data with historical BigQuery data
----------------------------------------------------------

Do the join where it makes sense: real-time enrichment for operational needs, historical joins for analytical reporting. Often the best pattern is to enrich stream events with a small reference lookup and leave heavier joins to batch. That avoids making the streaming pipeline fragile.

S96. Data quality framework with SLAs, alerting, and escalation
---------------------------------------------------------------

Define freshness, completeness, validity, and reconciliation checks for each critical dataset. Alert on failures quickly, route them to the right owner, and stop downstream propagation when the quality gate fails. This is how you turn data quality into an operational discipline.

S97. Canary deployment for a critical transformation
----------------------------------------------------

Release the new transformation to a small subset of partitions, tenants, or message keys first. Compare outputs against the old path before full cutover. If metrics drift, rollback immediately.

S98. Retroactive GDPR consent changes
-------------------------------------

Keep consent state versioned over time, not just current state. When consent changes, reprocess historical data according to the effective date and policy. This is easier if your raw data and transformation logic are both replayable.

S99. Pipeline cost forecasting model using billing export
---------------------------------------------------------

Use billing export data to identify seasonality, spikes, and per-team trends. Then forecast by service and workload type so finance and engineering can plan capacity. Cost forecasting is most useful when combined with labels and workload ownership.

S100. Ideal modern GCP data platform stack for 2026
---------------------------------------------------

A strong default stack is Pub/Sub for events, Dataflow for streaming/ETL, GCS for open storage, BigQuery for analytics, Composer for orchestration, Terraform for IaC, and Data Catalog plus policy tags for governance. Add dbt for transformation, Cloud Monitoring and OpenTelemetry for observability, and Vertex AI for ML integration. This aligns well with modern GCP delivery patterns and managed scaling features.

