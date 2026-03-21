AI Architect Interview Preparation Guide — Datacom ANZ
======================================================

This is your complete preparation toolkit covering 200 interview questions with answers (split across difficulty levels), scenario-based architecture questions, behavioral preparation strategy, and enterprise AI architecture blueprints for banking/finance.

Part 1: 200 Interview Questions & Answers
-----------------------------------------

🟢 Simple (65 Questions)
------------------------

**Foundational AI & LLM Concepts**

**Q1. What is the difference between a basic LLM application and an AI agent?**

A basic LLM app takes input → produces output in a single pass. An AI agent uses the LLM as its "brain" with tools, memory, and a loop: it perceives state, reasons about it, takes actions (tool calls), observes results, and iterates until the goal is achieved.​

**Q2. What is RAG (Retrieval-Augmented Generation)?**

RAG grounds an LLM response in enterprise-specific data by retrieving relevant chunks from a knowledge store (vector DB, search index) at query time and injecting them into the prompt context, reducing hallucinations and improving accuracy without retraining the model.​

**Q3. What is a vector database, and why is it used in AI?**

A vector database stores high-dimensional embeddings — numerical representations of text, images, or structured data — and supports approximate nearest-neighbor (ANN) search. Used in AI to find semantically similar content for RAG, recommendation engines, and deduplication. Examples: Pinecone, Weaviate, pgvector, OpenSearch.

**Q4. What is prompt engineering?**

The practice of crafting LLM inputs (system prompts, few-shot examples, instruction framing) to steer model behavior toward desired output quality, format, and safety boundaries.

**Q5. What is prompt injection?**

An attack where malicious instructions embedded in user input or retrieved content override the system prompt, causing the LLM to deviate from intended behavior. Mitigated by input sanitization, instruction hierarchy enforcement, and output guardrails.​

**Q6. What is fine-tuning vs. in-context learning?**

Fine-tuning adjusts model weights on domain-specific data (requires GPU compute, longer iteration). In-context learning (few-shot prompting) teaches the model via examples in the prompt without weight updates — faster and cheaper but limited by context window.

**Q7. What is a foundation model?**

A large ML model pre-trained on broad data capable of general tasks, which can be adapted (fine-tuned, prompted, or RAG-augmented) for specific applications. Examples: GPT-4o, Claude, Gemini, Mistral.​

**Q8. What is semantic search vs. keyword search?**

Keyword search matches exact terms. Semantic search uses embeddings to match meaning, so "car accident" and "vehicle collision" are treated as similar. Semantic search is essential for enterprise AI where terminology varies.

**Q9. What is the difference between LangChain and Semantic Kernel?**

LangChain is a Python-centric orchestration library focused on chaining LLM calls and tools with extensive integrations. Semantic Kernel is Microsoft's SDK (C#/Python/Java) that treats AI as a "kernel" of skills/plugins, better suited for enterprise .NET and Azure OpenAI environments.

**Q10. What is tokenization in LLMs?**

The process of breaking input text into tokens (sub-words or characters) that the model processes numerically. Token count determines context window usage and directly impacts API cost and latency.

**Q11. What is a context window?**

The maximum number of tokens (input + output) an LLM can process in a single call. Critical for architect decisions around chunking strategy in RAG and long-document processing.

**Q12. What is temperature in LLM inference?**

A parameter (0–2) controlling output randomness. Low temperature (0–0.3) = deterministic, factual responses. High temperature (0.7–1.5) = creative, varied outputs. Architects set this based on use case: near-zero for compliance tasks, higher for creative content.

**Q13. What is top-p sampling?**

Nucleus sampling — the model only considers tokens whose cumulative probability reaches p (e.g., 0.9). Used alongside temperature to balance diversity and coherence.

**Q14. What is embeddings vs. completion API?**

Embeddings API converts text → vectors (for search/similarity). Completion/chat API generates text responses. Both are core primitives used together in RAG pipelines.

**Q15. What is an AI guardrail?**

A safety layer (prompt-level, model-level, or output-level) that prevents harmful, non-compliant, or off-topic responses. Implemented via system prompt instructions, output classifiers, or services like Azure Content Safety and AWS Bedrock Guardrails.

**Q16. What is model drift?**

Degradation of model performance over time as real-world data distribution shifts from training data. Requires monitoring pipelines comparing live outputs against reference baselines.​

**Q17. What is hallucination in LLMs?**

When an LLM generates plausible-sounding but factually incorrect content. Key mitigation: RAG (ground responses in retrieved facts), citation enforcement, and output validation layers.

**Q18. What is Responsible AI?**

A framework ensuring AI systems are fair, reliable, safe, private, inclusive, transparent, and accountable. Includes bias testing, explainability, human-in-the-loop governance, and regulatory compliance.​

**Q19. What is the difference between AI and ML?**

AI is the broad discipline of building systems that mimic intelligent behavior. ML is a subset where systems learn from data. Deep Learning and LLMs are further subsets of ML.

**Q20. What is supervised vs. unsupervised learning?**

Supervised: model trained on labeled input-output pairs (e.g., fraud = yes/no). Unsupervised: model finds patterns in unlabeled data (e.g., customer clustering, anomaly detection).

**Cloud & Infrastructure Basics**

**Q21. What is a managed AI service?**

Cloud-provider-hosted model serving endpoints requiring no infrastructure management. Examples: Azure OpenAI, AWS Bedrock, GCP Vertex AI. Key for architect build-vs-buy decisions.

**Q22. What is serverless compute for AI?**

On-demand compute that auto-scales to zero (e.g., Cloud Run, Lambda, Azure Functions). Used for inference endpoints, webhook handlers, and event-driven AI pipelines with unpredictable traffic.

**Q23. What is a GPU and why does AI need it?**

Graphics Processing Units perform massive parallel matrix computations — the core operation of neural network inference and training. Without GPU acceleration, LLM inference is 10–100x slower.

**Q24. What is Infrastructure as Code (IaC)?**

Managing cloud infrastructure via declarative code (Terraform, CDK, Pulumi) rather than manual console clicks. Ensures reproducibility, version control, and auditability — critical for enterprise AI environments.

**Q25. What is a container registry?**

A repository for Docker container images (e.g., GCP Artifact Registry, AWS ECR, Azure ACR). AI workloads are packaged as containers for consistent deployment across environments.

**Q26. What is Kubernetes used for in AI?**

Orchestrating containerized AI workloads — managing GPU node pools, scaling inference deployments, running batch training jobs, and enforcing resource quotas across teams.

**Q27. What is GitOps?**

A deployment methodology where Git is the single source of truth for infrastructure and application state. Changes are applied via automated pipelines (ArgoCD, Flux) rather than manual kubectl apply.

**Q28. What is a CDN and is it relevant to AI?**

Content Delivery Network caches static content geographically. Relevant for AI-powered web apps to reduce frontend latency, but the AI inference layer requires direct low-latency routing to GPU endpoints.

**Q29. What is multi-tenancy in AI platforms?**

The ability to serve multiple customers (or teams) from shared infrastructure with proper isolation — separate data stores, prompt contexts, model endpoints, and billing. Critical for platforms like Datacom serving multiple enterprise clients.

**Q30. What is API Gateway in AI architecture?**

A managed entry point that handles authentication, rate limiting, logging, and routing for AI service APIs. Protects backend model endpoints from direct exposure and provides usage metering.

**Data & Storage**

**Q31. What is a data lake vs. data warehouse?**

Data lake: stores raw, unstructured/semi-structured data cheaply (S3, GCS, ADLS). Data warehouse: structured, optimized for SQL analytics (BigQuery, Redshift, Synapse). AI workloads often start in the lake, transform to warehouse-ready features.

**Q32. What is a feature store?**

A centralized repository of ML features (engineered data columns) that ensures consistency between training and inference environments. Prevents "training-serving skew."

**Q33. What is pgvector?**

A PostgreSQL extension that adds vector similarity search, allowing organizations to use their existing Postgres database as a vector store without adopting a new database system.

**Q34. What is chunking in RAG?**

Breaking documents into smaller segments before embedding. Chunking strategy (fixed-size, semantic, hierarchical) significantly impacts RAG retrieval quality. Chunks must be small enough for relevance but large enough to preserve context.

**Q35. What is metadata filtering in vector search?**

Adding structured attributes (document type, date, security classification) to vector records, enabling hybrid queries: "find semantically similar documents that are also from 2024 and classified as 'internal'."

**Architecture Basics**

**Q36. What is an Architectural Decision Record (ADR)?**

A lightweight document capturing an architectural decision, its context, the options considered, the choice made, and the rationale. Critical for knowledge transfer and governance in enterprise AI programs.

**Q37. What is event-driven architecture?**

A pattern where components communicate by publishing and consuming events (e.g., Pub/Sub, Kafka, EventBridge) rather than synchronous API calls. Enables decoupling and horizontal scale — valuable for AI pipelines processing high-volume data streams.

**Q38. What is a microservices architecture?**

An approach decomposing an application into small, independently deployable services. In AI: separate services for ingestion, embedding, retrieval, inference, and response formatting — each scalable independently.

**Q39. What is REST vs. GraphQL vs. gRPC?**

REST: stateless HTTP, resource-based, simple. GraphQL: flexible query language, client-specifies data shape, avoids over-fetching. gRPC: binary protocol (Protobuf), low-latency, strongly typed — preferred for internal high-throughput AI service communication.

**Q40. What is a service mesh?**

Infrastructure layer (Istio, Linkerd) handling service-to-service communication: mTLS encryption, traffic routing, circuit breaking, and observability without application code changes.

**Q41. What is blue-green deployment for AI models?**

Maintaining two production environments (blue = current, green = new). Traffic is shifted to green after validation. Enables zero-downtime model updates and instant rollback.

**Q42. What is canary deployment in AI?**

Routing a small percentage of traffic (e.g., 5%) to a new model version, monitoring quality metrics, and gradually increasing if safe. Reduces blast radius of bad model releases.

**Q43. What is an LLM evaluation framework?**

A systematic approach to measuring LLM output quality using metrics like faithfulness, relevance, completeness, and toxicity. Tools: RAGAS, LangSmith, PromptFlow. Essential for non-deterministic systems.​

**Q44. What is the difference between latency and throughput?**

Latency: time for one request to complete (milliseconds). Throughput: requests processed per second. AI architects must balance both — GPU batching improves throughput but may increase latency.

**Q45. What is caching in AI inference?**

Storing repeated LLM responses for identical or similar inputs (semantic caching) to reduce cost and latency. Tools: Redis, GPTCache. Particularly effective for FAQ-style AI applications.

**Security Basics**

**Q46. What is the principle of least privilege?**

Users and services should have only the minimum permissions required for their function. In AI: model serving pods should not have write access to training data stores.

**Q47. What is data masking in AI?**

Replacing sensitive data (PII, PCI) with anonymized equivalents before sending to LLM APIs. Critical in financial services to prevent customer data exposure to external model providers.

**Q48. What is OWASP LLM Top 10?**

OWASP's list of critical security risks for LLM applications: Prompt Injection, Insecure Output Handling, Training Data Poisoning, Model Denial of Service, Supply Chain Vulnerabilities, Sensitive Information Disclosure, Insecure Plugin Design, Excessive Agency, Overreliance, and Model Theft.

**Q49. What is a threat model for AI?**

A structured analysis of potential attack vectors against an AI system: data poisoning, adversarial inputs, prompt injection, model extraction, and output manipulation — used to design mitigations proactively.

**Q50. What is federated learning?**

A training approach where models are trained locally on distributed devices/nodes without centralizing raw data, only aggregating model updates. Valuable in banking for privacy-preserving collaborative model training.​

**Leadership & Communication Basics**

**Q51. What is a reference architecture?**

A reusable, opinionated blueprint for solving a class of problems (e.g., "Enterprise RAG on Azure") that teams can adapt. Encodes proven patterns, technology choices, and integration points.

**Q52. What is technical governance in AI?**

The process of reviewing, approving, and maintaining architectural decisions and standards across delivery teams. Includes architecture review boards (ARBs), design pattern libraries, and quality gates.

**Q53. What is a build-vs-buy decision?**

Evaluating whether to develop a capability in-house or purchase/license it. Factors: differentiation value, time-to-market, total cost, vendor lock-in risk, and customization needs.

**Q54. What is MLOps?**

The discipline combining ML and DevOps practices: automated model training pipelines, versioning, testing, deployment, monitoring, and retraining. Ensures AI systems behave reliably in production.

**Q55. What is LLMOps?**

MLOps adapted for LLM-based systems: prompt versioning, evaluation pipelines, deployment of chat/completion endpoints, context window management, and cost tracking per token.

**Q56. What is AgentOps?**

Observability and operational practices specifically for agentic AI systems: tracing multi-step tool call chains, monitoring agent loop iterations, detecting infinite loops, and auditing autonomous actions.​

**Q57. What is AI FinOps?**

Cost management practices for AI workloads: tracking GPU utilization, per-token API costs, model serving expenses, and optimizing inference patterns (caching, batching, quantization) to meet cost targets.

**Q58. What is quantization in model serving?**

Reducing model weight precision (e.g., FP32 → INT8 or INT4) to decrease memory footprint and increase inference speed with acceptable accuracy loss. Enables running larger models on less expensive GPU hardware.

**Q59. What is model distillation?**

Training a smaller "student" model to mimic a larger "teacher" model's behavior. Produces smaller, faster models for production serving while retaining most capability.

**Q60. What is KV cache in LLM inference?**

A mechanism that caches key-value attention matrices for previously processed tokens, avoiding recomputation on repeated prefixes. Reduces latency for long conversations or documents with shared preambles.

**Q61. What is semantic caching?**

Caching LLM responses keyed by embedding similarity rather than exact string match — so semantically identical questions ("What's my balance?" vs "What is my account balance?") return cached responses.

**Q62. What is the difference between synchronous and asynchronous AI inference?**

Synchronous: request waits for response (low latency, suitable for real-time chat). Asynchronous: request is queued, response delivered via callback/webhook (higher throughput, suitable for batch document processing).

**Q63. What is a knowledge graph vs. vector store in AI?**

Vector store: similarity-based retrieval of unstructured text chunks. Knowledge graph: structured entities and relationships (Neo4j, Neptune). Graph RAG combines both for relational reasoning — powerful for fraud network analysis.​

**Q64. What is the difference between AI observability and monitoring?**

Monitoring tracks infrastructure metrics (latency, error rate, GPU%). Observability captures the "why" — tracing individual LLM calls, inputs/outputs, tool call sequences, and reasoning chains to diagnose quality issues.

**Q65. What is responsible AI in the context of Australian regulation?**

Australia's AI Ethics Framework and Privacy Act mandate transparency, human oversight, fairness, and privacy protection for AI systems. Architects must design explainability into models and maintain audit trails, particularly for decisions affecting individuals (lending, insurance).

🟡 Medium (65 Questions)
------------------------

**Agentic AI & Orchestration**

**Q66. What are the key components of an AI agent?**

An agent consists of: (1) **Perception** — input from user or environment; (2) **Memory** — short-term (context window), long-term (vector DB), and episodic (conversation history); (3) **Planning** — decomposing goals into subtasks; (4) **Tool use** — calling external APIs, databases, or compute; (5) **Action** — executing decisions; (6) **Reflection** — evaluating outcomes and self-correcting.​

**Q67. What is the ReAct pattern?**

ReAct (Reasoning + Acting) interleaves "Thought: I need to check X" with "Action: call tool Y" and "Observation: result Z" in a loop. This makes agent reasoning transparent and auditable — critical for enterprise compliance.​

**Q68. What is the difference between orchestrator and sub-agent?**

In multi-agent systems, the orchestrator receives the task, decomposes it, delegates to specialized sub-agents (retrieval agent, calculation agent, compliance agent), and synthesizes their outputs. The orchestrator maintains overall goal state while sub-agents have narrow expertise.​

**Q69. How do you prevent agent infinite loops?**

Implement: (1) maximum iteration limits; (2) step budget tracking; (3) loop detection (same tool + same input); (4) timeout circuits; (5) reflection prompts that force the agent to assess whether progress is being made before continuing.​

**Q70. What is the difference between ReAct, Plan-and-Execute, and Reflexion?**

*   **ReAct**: Interleaved reasoning and acting, single pass.
    
*   **Plan-and-Execute**: Creates a full plan upfront, then executes each step — better for predictable multi-step tasks.
    
*   **Reflexion**: Agent generates output, then critiques its own output and iterates — improves quality via self-reflection.
    

**Q71. What is tool-calling vs. function-calling?**

Function calling (OpenAI term) = tool calling — the LLM selects a structured function to invoke based on its parameters definition and the user's intent, returning structured JSON the application executes. The model doesn't execute code; it produces the call specification.

**Q72. How do you handle tool failures in agentic systems?**

Implement retry logic with exponential backoff, fallback tools (alternative API for same data), graceful degradation (partial answers with caveats), and error injection into context so the agent can reason about the failure and try an alternative strategy.​

**Q73. What is Human-in-the-Loop (HITL) in agentic AI?**

Inserting human approval checkpoints at high-stakes decision points — e.g., before an agent sends an email, executes a transaction, or modifies data. Critical for financial services where autonomous actions carry regulatory and financial risk.​

**Q74. What is agent memory architecture?**

*   **In-context (short-term)**: current conversation window.
    
*   **External semantic (long-term)**: vector DB with past interactions/facts.
    
*   **Episodic**: structured summaries of past sessions retrieved as needed.
    
*   **Procedural**: tools, skills, and prompt libraries the agent knows how to use.
    

**Q75. What is the difference between single-agent and multi-agent architectures?**

Single-agent handles all tasks sequentially in one loop — simpler but bottlenecked. Multi-agent parallelizes specialized agents, enabling concurrent execution and separation of concerns. Multi-agent is harder to debug and requires explicit coordination protocols.​

**Q76. What is AutoGen / CrewAI / LangGraph and when would you choose each?**

*   **AutoGen** (Microsoft): Multi-agent conversation framework, strong for code-generation agents.
    
*   **CrewAI**: Role-based agent crews with task delegation, easier to configure.
    
*   **LangGraph**: Graph-based agent orchestration with explicit state machines — best for complex enterprise workflows requiring reliable state management and conditional branching.
    

**Q77. How do you version prompts in production?**

Store prompts in a dedicated prompt registry (LangSmith, PromptLayer, or a simple Git-backed YAML store) with semantic versioning, evaluation test results per version, and A/B deployment capability. Never hard-code prompts in application code.​

**Q78. What is chain-of-thought (CoT) prompting?**

Instructing the model to show reasoning steps before providing an answer ("Let me think step by step..."). Dramatically improves performance on multi-step reasoning tasks. Zero-shot CoT works with the instruction alone; few-shot CoT provides worked examples.

**Q79. What is self-consistency in LLM reasoning?**

Generating multiple reasoning paths (higher temperature) and selecting the most frequent conclusion. Increases accuracy for complex reasoning at the cost of 3–5x inference overhead. Used where answer quality justifies compute cost.

**Q80. What is a router agent?**

An agent (or an LLM call) that classifies incoming requests and routes them to the appropriate specialized handler or sub-agent. For a bank: "Is this a fraud query? → Fraud agent. Balance query? → Core banking agent."

**Solution Architecture**

**Q81. How do you design a RAG pipeline for enterprise?**

Stages: (1) **Ingestion**: extract documents → chunk → embed → store in vector DB with metadata; (2) **Retrieval**: embed query → ANN search → metadata filter → re-rank results; (3) **Generation**: inject retrieved chunks into system prompt → LLM response → citation extraction; (4) **Evaluation**: faithfulness, relevance, completeness metrics. All stages must be monitored and tunable.​

**Q82. What is hybrid search?**

Combining dense (vector/semantic) search with sparse (BM25/keyword) search using a fusion algorithm (RRF — Reciprocal Rank Fusion). Hybrid search consistently outperforms either alone, particularly for domain-specific queries with precise terminology.​

**Q83. What is Graph RAG and when should you use it?**

Graph RAG enriches retrieval with knowledge graph traversal — finding not just similar documents but related entities and their relationships. Use when queries require relational reasoning: "Show all transactions linked to this merchant and its parent company".​

**Q84. How do you design for AI observability?**

Instrument every LLM call with: input/output logging, latency, token count, model version, and a trace ID. For agents: log every tool call and result in a trace. Use OpenTelemetry + a backend (Langfuse, Phoenix, Datadog LLM Observability) for visualization and alerting .

**Q85. What is semantic re-ranking in RAG?**

After ANN retrieval returns the top-k candidates, a cross-encoder re-ranker (e.g., Cohere Rerank, BGE-reranker) scores each chunk against the query more accurately (but more expensively). This two-stage approach balances speed (ANN) with precision (re-ranker).

**Q86. How do you handle multi-tenant data isolation in a RAG system?**

Options: (1) separate vector collections per tenant (strong isolation, higher cost); (2) shared collection with tenant metadata filter applied at query time (efficient, requires careful access control); (3) separate vector DB instances for high-security tenants (banks). Always combine with IAM enforcement.

**Q87. What is the difference between fine-tuning and RAG for enterprise knowledge?**

Fine-tuning bakes knowledge into model weights — fast inference but knowledge becomes stale and requires retraining for updates. RAG retrieves fresh knowledge at runtime — more expensive per query but always current. For frequently changing enterprise knowledge (policies, pricing), RAG is preferred.

**Q88. How do you design an AI solution for compliance in financial services?**

Key elements: (1) data residency controls (no customer PII to external APIs); (2) audit logging of all AI decisions; (3) explainability layer (can you explain why the model made this decision?); (4) human escalation paths; (5) model risk management (MRM) framework alignment; (6) PCI-DSS/APRA CPS 234 compliance.​

**Q89. What is the strangler fig pattern for AI adoption?**

Gradually wrapping a legacy system with AI capabilities — new features route through AI while the legacy core remains. Over time, AI handles more until the legacy component is replaced. Reduces risk vs. big-bang replacement.

**Q90. What is an AI gateway pattern?**

A dedicated service sitting in front of all LLM API calls, providing: unified authentication, cost tracking per tenant, rate limiting, prompt/response logging, guardrail enforcement, and failover between model providers. Prevents direct coupling to any single LLM vendor.

**Q91. How would you design a document intelligence pipeline?**

Stages: OCR/document extraction (Azure DI, AWS Textract) → layout-aware chunking → embedding + vector store → RAG retrieval → LLM extraction with structured output (JSON mode) → validation against schema → output to downstream systems.

**Q92. What is context window management in production agents?**

Strategies to avoid exceeding limits: rolling message compression (summarize older turns), selective context injection (retrieve only relevant memories), priority-based context pruning (drop low-relevance tool outputs), and model selection based on task context length requirements.

**Q93. What is structured output and why does it matter for enterprise AI?**

Forcing LLM responses into a defined JSON schema (using OpenAI JSON mode, Instructor library, or Pydantic models) ensures downstream systems can reliably parse AI outputs. Critical for integrating LLM responses into existing enterprise APIs and workflows.

**Q94. What is streaming in LLM APIs?**

Server-Sent Events (SSE) delivery of LLM tokens as they are generated rather than waiting for completion. Dramatically improves perceived performance for chat UIs. Requires token-by-token processing in the application layer.

**Q95. How do you handle LLM cost at enterprise scale?**

Strategies: (1) model tiering (use GPT-4o-mini for classification, GPT-4o for complex reasoning); (2) semantic caching for repeated queries; (3) prompt compression to reduce input tokens; (4) batching async workloads; (5) self-hosted OSS models for high-volume, non-sensitive tasks; (6) per-feature cost attribution.​

**Cloud & AI Infrastructure**

**Q96. When would you use Vertex AI vs. Azure OpenAI vs. AWS Bedrock?**

*   **Vertex AI**: best for GCP-native data stacks (BigQuery, GCS), Gemini models, and MLOps with Vertex Pipelines.
    
*   **Azure OpenAI**: best for enterprise Microsoft stacks, GPT-4o with data residency guarantees, Microsoft Fabric integration.
    
*   **Bedrock**: best for AWS-native environments, Claude/Titan models, and strong IAM integration with existing AWS infrastructure.
    

**Q97. What is vLLM and when would you use it?**

An open-source inference engine using PagedAttention to efficiently manage KV cache memory, enabling high-throughput serving of open-source models (Llama, Mistral) at 3–10x throughput vs. naive serving. Use when self-hosting OSS models for cost or data sovereignty reasons.

**Q98. What is a vector database's HNSW index?**

Hierarchical Navigable Small World — a graph-based ANN index structure offering O(log n) search complexity with high recall. The dominant algorithm in production vector databases (Pinecone, Weaviate, pgvector with HNSW option) due to its speed/recall balance.

**Q99. What is a sidecar pattern in Kubernetes for AI?**

Deploying auxiliary containers alongside the main AI service container in the same Pod: e.g., a logging sidecar capturing all LLM I/O, a secrets-injection sidecar, or a metrics exporter. Keeps the AI application container clean and focused.

**Q100. What is spot/preemptible instance strategy for AI?**

Using cheap interruptible cloud VMs (AWS Spot, GCP Spot) for fault-tolerant AI workloads like batch embedding generation or model training. Not suitable for real-time inference SLA workloads. Requires checkpoint-and-resume design.

**Q101. What is an embedding model, and how do you choose one?**

An encoder model converting text → fixed-dimension vectors. Selection criteria: (1) benchmark performance on your domain (MTEB leaderboard); (2) supported context length (for long documents); (3) multilingual capability; (4) inference cost and latency; (5) update frequency. Popular: text-embedding-3-large, Cohere Embed v3, BGE-large.

**Q102. What is semantic chunking vs. fixed-size chunking?**

Fixed-size: split every N tokens with overlap — simple, predictable. Semantic: split at natural boundaries (sentence, paragraph, section) — better preserves meaning but variable chunk sizes. Hierarchical chunking stores both summary (parent) and detail (child) chunks for multi-granularity retrieval.

**Q103. What is OpenTelemetry and why does it matter for AI?**

A vendor-neutral observability standard for distributed tracing, metrics, and logs. For AI: instrument every LLM call as a span in a trace, enabling end-to-end latency breakdown (retrieval time, LLM time, post-processing time) and correlation with application errors.

**Q104. What is model endpoint autoscaling?**

Configuring inference endpoints to scale GPU/CPU replicas based on request queue depth or latency. Cloud services (Vertex AI, SageMaker, Azure ML) support this natively. Architects must define scale-to-zero policies vs. warm baseline for cost vs. cold-start trade-offs.

**Q105. What is the difference between batch inference and online inference?**

Online inference: real-time, low-latency, synchronous (< 1s). Batch inference: high-volume, scheduled, asynchronous (hours acceptable). Document intelligence, nightly analytics, and bulk classification are batch. Customer-facing chat is online.

**Security & Governance**

**Q106. What is AI model card and why do regulators care?**

A documentation artifact describing a model's purpose, training data, performance across demographic groups, known limitations, and intended use. Australian APRA and ASIC increasingly expect model cards for AI systems making consequential decisions.

**Q107. What is differential privacy in AI?**

A mathematical technique ensuring that removing any single record from a training dataset has negligible effect on the model's output distribution, providing provable privacy guarantees for training data. Used in federated learning scenarios for banking.​

**Q108. What is adversarial robustness testing?**

Evaluating AI models against inputs specifically designed to fool them — using techniques like FGSM, PGD attacks for ML models, or jailbreak prompts for LLMs. Part of the AI security validation process before production deployment.

**Q109. How do you implement output filtering in an AI system?**

Post-generation classifiers check responses for: PII (regex + NER), toxicity (Perspective API), competitor mentions, off-topic content, and confidential data patterns. Failed checks trigger either response blocking, redaction, or human review routing.

**Q110. What is model risk management (MRM)?**

A banking regulatory framework (OCC guidance, APRA CPG 234) requiring: model validation before deployment, ongoing performance monitoring, model inventory maintenance, documented assumptions and limitations, and independent validation for high-impact models.

**Leadership & Delivery**

**Q111. How do you run an architecture review for an AI solution?**

Structure: (1) solution brief review (requirements, constraints); (2) architecture walkthrough (data flow, component diagram); (3) non-functional requirements assessment (scale, latency, cost, security); (4) risk identification; (5) ADR review; (6) decision: approve / approve with conditions / reject. Document all decisions with rationale.

**Q112. How do you communicate AI architecture to a non-technical executive?**

Use business outcome framing: "This architecture ensures customer queries are answered in under 2 seconds, costs $X per 1,000 conversations, and ensures no customer data leaves Australia." Avoid jargon. Use diagrams with swim lanes showing customer journey, not infrastructure.

**Q113. What is a PoC vs. MVP vs. Production in AI delivery?**

*   **PoC**: validates technical feasibility, minimal scope, throwaway code.
    
*   **MVP**: smallest deployable product with core value, real users, some production-grade features.
    
*   **Production**: full NFRs met (availability, security, observability, scale). Architects must define the criteria for graduation between each stage.
    

**Q114. What is "AI-ready data architecture"?**

Data infrastructure designed to support AI: clean, versioned, well-governed data with lineage tracking; feature stores for ML; vector stores for LLM applications; streaming pipelines for real-time model inputs; and data contracts ensuring schema stability between producers and AI consumers.

**Q115. How do you establish AI engineering standards for a delivery team?**

Document: (1) approved model list and providers; (2) prompt management practices; (3) evaluation requirements before production; (4) observability standards; (5) security controls (data masking, output filtering); (6) cost budgets per feature; (7) testing patterns for non-deterministic outputs. Enforce via PR templates and ARB gates.

**Q116. What is the AI Architecture Maturity Model?**

A framework assessing organizational AI sophistication across five levels:

*   **L1** – Experimental (ad-hoc PoCs)
    
*   **L2** – Managed (basic MLOps, manual deployments)
    
*   **L3** – Defined (standardized pipelines, evaluation frameworks)
    
*   **L4** – Quantitatively managed (cost tracking, quality SLAs)
    
*   **L5** – Optimizing (continuous improvement, autonomous retraining).​
    

**Q117. What frameworks support AI governance in Australia?**

APRA CPS 234 (information security), APRA CPG 229 (climate financial risk, increasingly applied to AI risk), ASIC regulatory guide on digital advice, Privacy Act 1988 (APP principles), and the Australian AI Ethics Framework published by DISR.

**Q118. What is prompt management at scale?**

A system for: versioning prompt templates (Git or dedicated tool), A/B testing prompt variants, associating evaluation scores with each version, managing prompt dependencies across agents, and deploying prompt changes independently of application code releases.

**Q119. What is a capability map for enterprise AI?**

A strategic artifact showing which business capabilities exist, which are AI-enabled, which are candidates for AI transformation, and the dependency relationships. Used by AI architects to prioritize investment and identify reusable AI components.

**Q120. How do you evaluate vendors for AI services?**

Criteria: (1) data residency and sovereignty (critical for ANZ); (2) model quality benchmarks on domain tasks; (3) API reliability and SLA; (4) pricing model and cost predictability; (5) security certifications (ISO 27001, SOC 2); (6) vendor lock-in risk and exit strategy; (7) roadmap alignment with your use cases.

**Practical Engineering**

**Q121. What is LangSmith and how does it support AI development?**

LangChain's observability and evaluation platform — traces LLM calls, stores datasets for regression testing, runs automated evaluations against test sets, and supports human annotation. Provides the feedback loop needed to improve AI quality systematically.

**Q122. How do you test a non-deterministic AI system?**

Use: (1) deterministic assertions for structured outputs (JSON schema validation); (2) LLM-as-judge evaluation for quality (have a second LLM score outputs against a rubric); (3) reference datasets with expected answer ranges; (4) regression testing with temperature=0 for reproducibility during CI/CD.​

**Q123. What is RAGAS?**

An open-source framework for evaluating RAG pipelines, measuring: Faithfulness (answer grounded in retrieved context), Answer Relevance (answer addresses the question), Context Precision (retrieved context is on-topic), and Context Recall (all relevant information retrieved).

**Q124. What is the difference between retrieval precision and recall?**

Precision: of retrieved chunks, how many are relevant (quality). Recall: of all relevant chunks in the store, how many were retrieved (completeness). For RAG, both matter — low precision adds noise to the LLM context; low recall means incomplete answers.

**Q125. What is a shadow deployment for AI models?**

Running a new model version alongside production, receiving the same traffic but not serving responses to users. Compare outputs of shadow vs. production to validate quality before cutover — zero user impact testing.

**Q126. What is token budget management in agents?**

Explicitly tracking and limiting token consumption within a single agent run: reserving tokens for system prompt, retrieved context, tool outputs, and response generation. Prevents context overflow by dynamically truncating or summarizing lower-priority content.

**Q127. What is instruction hierarchy in LLM systems?**

The priority ordering of instruction sources: System prompt > Developer injections > User input > Retrieved content. Enforcing this hierarchy prevents prompt injection attacks from overriding system-level instructions.​

**Q128. What is semantic versioning for AI models?**

Applying Major.Minor.Patch versioning to models: Major = breaking change in output behavior; Minor = significant quality improvement; Patch = minor fix. Enables consumers to pin to stable versions while new versions are validated.

**Q129. What is the difference between an embedding model and a generative model?**

Embedding models are encoder-only (BERT-family) — map input → vector, no text generation. Generative models are decoder-only (GPT-family) — generate token sequences. Modern systems use both: embed for retrieval, generate for response.

**Q130. What is LlamaIndex (now LlamaCloud)?**

A data framework for building LLM applications over enterprise data — specializes in complex indexing strategies (hierarchical, knowledge graph, multi-modal) and query engines. Complements LangChain (which focuses more on chaining/agents) with deeper data indexing capabilities.

🔴 Hard (70 Questions)
----------------------

**Advanced Agentic Architecture**

**Q131. Design a multi-agent system for financial report generation. What are the agents and coordination protocol?**

Agents: (1) Data Extraction Agent — queries financial databases/APIs; (2) Calculation Agent — validates figures, computes ratios; (3) Narrative Agent — generates written sections from structured data; (4) Compliance Agent — validates content against regulatory disclosure requirements; (5) Orchestrator — manages task graph, handles failures, assembles final document. Coordination: LangGraph state machine with explicit node transitions, shared state object, and HITL checkpoint before Compliance Agent sign-off.​

**Q132. How do you architect an agentic system that must operate within 200ms P99 latency in payments?**

Key strategies: (1) Pre-compute and cache embeddings for common query patterns; (2) Use semantic cache (Redis + vector similarity) for repeated agent paths; (3) Constrain agent to single-turn (no multi-step loop) for time-sensitive flows; (4) Deploy fine-tuned smaller model (Mistral 7B) on dedicated GPU for low-latency inference; (5) Pre-load tool schemas to avoid runtime schema resolution; (6) Use gRPC for inter-service calls; (7) Stream first token within 50ms using speculative decoding.​

**Q133. How would you prevent an agent from taking irreversible actions in a production financial system?**

Architecture controls: (1) **Semantic guardrail layer** — classifier detecting action type (read vs. write vs. irreversible); (2) **Action approval queue** — all write operations buffered and human-reviewed before execution; (3) **Capability scoping** — agent tools only expose idempotent reads by default, write tools require explicit capability grant per session; (4) **Dry-run mode** — all actions simulated first, outputs reviewed; (5) **Audit log** — immutable event stream of every agent action with reasoning trace; (6) **Circuit breaker** — auto-halt if anomalous action frequency detected.​

**Q134. How do you architect a multi-agent system that handles 10,000 concurrent sessions in financial services?**

Architecture: (1) Stateless agent workers deployed on Kubernetes with HPA scaling on request queue depth; (2) Session state externalized to Redis (short-term context) and vector DB (long-term memory); (3) Kafka for async agent task queuing; (4) Agent pool with worker-type routing (simple query → lightweight agent, complex analysis → heavy agent); (5) GPU inference served via vLLM with continuous batching; (6) Separate agent execution from LLM inference layer for independent scaling; (7) Cell-based architecture (tenant isolation at infrastructure level).​

**Q135. What is the "lost in the middle" problem in LLMs and how do you architect around it?**

LLMs attend more strongly to content at the beginning and end of the context window, with degraded performance for content in the middle. Mitigations: (1) Re-rank retrieved chunks so the most relevant are at the start and end; (2) Use hierarchical RAG — high-level summary first, detailed evidence second; (3) Compress middle content using a summarization step; (4) Use models specifically fine-tuned for long-context (Gemini 1.5, Claude 3.5 Sonnet) that demonstrate improved mid-context attention.

**Q136. How do you design an AI evaluation framework for a production financial AI system?**

Components: (1) **Offline evaluation**: curated golden dataset (question + ground truth answer + source docs) evaluated against RAGAs metrics + LLM-as-judge; (2) **Online evaluation**: real-user session sampling → human annotation pipeline → quality score tracking over time; (3) **Automated regression tests**: run on every model/prompt change in CI/CD; (4) **Adversarial test suite**: injection attempts, edge cases, hallucination probes; (5) **Business KPI tracking**: task completion rate, escalation rate, customer satisfaction; (6) **Evaluation cadence**: automated on every PR, human review weekly, full audit quarterly.​

**Q137. What is a planning agent and when is it superior to ReAct?**

A planning agent (HTN — Hierarchical Task Network, or LLM-based plan-then-execute) generates a complete multi-step plan before taking any actions. Superior to ReAct when: (1) task requires global optimization (ordering actions to minimize API calls); (2) tool calls have side effects requiring careful sequencing; (3) you need to validate the plan with a human before execution; (4) tasks are long-horizon (20+ steps) where reactive approaches diverge. Downside: brittle to unexpected observations mid-execution .

**Q138. How do you architect a "debate" pattern between agents for high-stakes decisions?**

Two or more agents independently generate answers. A judge agent evaluates their reasoning and evidence quality, flags disagreements, and either synthesizes a consensus or escalates to human review when confidence is low. Used for medical diagnosis, legal document review, and high-value financial advice. Pattern inspired by Constitutional AI and ensemble methods.

**Q139. What is the actor-critic pattern in agentic AI?**

Actor agent generates actions/responses; Critic agent evaluates them against quality criteria (correctness, completeness, safety). Critic's feedback is injected back into Actor's context for revision. Multiple revision cycles until Critic's threshold is met or max iterations reached — a self-refinement loop.

**Q140. How do you handle tool schema evolution in a production agentic system?**

Version tool schemas (v1, v2) and maintain backward compatibility for running sessions. Use an agent tool registry that serves schema versions by agent version. Deprecate old tool versions with telemetry-based usage tracking before removal. Store serialized tool call results with schema version metadata for replay/debugging.​

**RAG & Data Architecture**

**Q141. Design a production RAG system for a major Australian bank handling 50,000 queries/day across 10TB of policy and regulatory documents.**

Architecture layers:

*   **Ingestion**: Azure Data Factory/Glue → PDF/Word/HTML parsing (Azure Document Intelligence) → semantic chunking (512 tokens, 64 overlap) → embedding (text-embedding-3-large) → pgvector on Azure Database for PostgreSQL Flexible Server (with HNSW index) + metadata (doc type, jurisdiction, effective date, classification level).
    
*   **Retrieval**: Query embedding → hybrid search (dense + BM25) → metadata filter (security classification ≤ user clearance) → Cohere re-rank top-20 → top-5 injected into context.
    
*   **Generation**: Azure OpenAI GPT-4o (in-region, no data egress) → structured output with citations → output filtering (PII redaction, hallucination detection).
    
*   **Observability**: OpenTelemetry → Azure Monitor + LangSmith for trace analysis.
    
*   **Scale**: 50K queries/day ≈ 0.6 QPS average, peak 5 QPS → 3 replicas of GPT-4o Provisioned Throughput Units (PTUs).
    

**Q142. What is the difference between sparse, dense, and hybrid retrieval for financial documents?**

*   **Sparse (BM25)**: Exact term matching, high precision for regulatory terminology with exact phrases ("APRA Prudential Standard APS 112"). No semantic understanding.
    
*   **Dense (Vector)**: Semantic matching, finds relevant docs even with different terminology ("capital adequacy requirements" = "minimum capital levels"). Misses exact terms.
    
*   **Hybrid (RRF fusion)**: Combines both scores — best for financial documents combining regulatory citations (need sparse) with natural language queries (need dense). Consistently 10–15% better recall.​
    

**Q143. How do you architect a streaming data ingestion pipeline for real-time AI context updating?**

Architecture: Kafka event stream (trade events, price updates) → Kafka Streams consumer → embedding service (stateless, horizontally scalable) → upsert to vector DB (using doc ID for deduplication) → cache invalidation signal to semantic cache → downstream agents pick up fresh context on next query. Critical: use document IDs for idempotent upserts to prevent duplicate embeddings on replay.​

**Q144. What is knowledge graph augmented generation (KGAG) and design it for fraud detection?**

Augments vector RAG with a property graph (Neo4j) storing entities (customers, merchants, accounts, devices) and relationships (transacted\_with, shares\_device, same\_IP). For fraud detection: a RAG query for "suspicious activity on account X" triggers both: (1) vector search for similar fraud cases; (2) graph traversal finding all entities within 2 hops of account X — surfacing ring fraud patterns invisible to vector search alone.

**Q145. How do you handle document access control in a multi-tenant RAG system for a bank?**

*   **Row-level security**: Store tenant\_id and security\_classification in vector metadata. Apply mandatory filters on every query: WHERE tenant\_id = :current\_tenant AND classification\_level <= :user\_clearance.
    
*   **Tenant isolation**: Separate pgvector schemas per bank subsidiary for strong isolation.
    
*   **Pre-retrieval authorization**: Check user's data access permissions before query hits the vector store.
    
*   **Post-retrieval verification**: Secondary check ensuring no inadvertent cross-tenant data in retrieved chunks before LLM injection.
    
*   **Audit logging**: Log every document accessed per user session for compliance audit trail.
    

**Q146. What is the "chunking and retrieval" problem and how does contextual retrieval solve it?**

Standard RAG loses context when chunking — a chunk saying "The rate increased to 5.5%" is meaningless without knowing which rate. Anthropic's Contextual Retrieval pre-pends each chunk with an LLM-generated contextual summary ("This chunk discusses the RBA cash rate decision from November 2024...") before embedding, dramatically improving retrieval relevance at modest additional cost.

**Cloud Architecture**

**Q147. Compare Azure OpenAI, self-hosted Llama 3, and AWS Bedrock Claude for an Australian bank.**

DimensionAzure OpenAISelf-hosted Llama 3Bedrock ClaudeData ResidencyAustralia EastOwn DC/GCP/AWSap-southeast-2Cost at scalePTU commitmentGPU infra + opsPer-tokenCustomizationLimited fine-tuningFull fine-tune/LoRALimitedComplianceSOC 2, ISO 27001You own itSOC 2, ISO 27001Ops OverheadLowHighLowModel QualityGPT-4o (top tier)Llama 3.1 70B (very good)Claude 3.5 Sonnet

For an Australian bank: Azure OpenAI in Australia East + Bedrock as fallback is the recommended dual-provider strategy .

**Q148. How do you design GPU inference infrastructure for variable AI workloads?**

Architecture: (1) **Warm pool**: minimum 2 GPU replicas always running (handles baseline, eliminates cold start); (2) **Scale-out**: HPA on queue depth → provision additional GPU nodes (G4dn on AWS, A2 on GCP) within 90 seconds; (3) **Spot fleet**: 70% spot + 30% on-demand for cost optimization with checkpoint protection; (4) **Inference engine**: vLLM with continuous batching (groups concurrent requests to maximize GPU utilization); (5) **Model quantization**: INT8/INT4 GPTQ for 40–60% memory reduction enabling more concurrent requests per GPU .

**Q149. Design a disaster recovery architecture for an AI-powered customer service system.**

RPO: 1 hour, RTO: 15 minutes. Architecture: (1) Active-active across two Azure regions (Australia East + Southeast Asia); (2) Vector DB replicated with WAL streaming (pgvector on Azure Flexible Server with geo-redundant backup); (3) Azure OpenAI PTU in both regions with traffic manager routing; (4) Session state in geo-replicated Redis Enterprise; (5) Conversation history in Cosmos DB with multi-region write; (6) Automated failover tested monthly with chaos engineering.

**Q150. What is a LoRA adapter and how does it enable efficient multi-tenant fine-tuning?**

LoRA (Low-Rank Adaptation) freezes base model weights and trains small adapter matrices (rank 4–64) representing parameter-efficient domain adaptation. For multi-tenant: one shared base model + per-tenant LoRA adapters (100–500MB each vs. full model at 140GB). Adapters are swapped at inference time per tenant request — enabling personalized models without 100 separate full deployments.

**Security & Governance (Hard)**

**Q151. How do you architect a defense-in-depth strategy against prompt injection for a bank's AI system?**

Layers: (1) **Input layer**: sanitize input (strip special chars, detect injection signatures); (2) **Instruction hierarchy**: system prompt cannot be overridden by user content (use model-level system role strictly); (3) **Indirect injection detection**: scan all retrieved documents for embedded instructions before injecting into context; (4) **Constrained output**: use JSON mode / structured output to prevent free-form instruction execution; (5) **Output filter**: classify response for signs of instruction following vs. data disclosure; (6) **Agent capability restriction**: tool schemas explicitly limited — no exec\_code or send\_email available by default; (7) **Anomaly detection**: flag sessions where user input pattern matches known injection templates.​

**Q152. How do you implement model drift detection in production?**

(1) **Reference window**: maintain rolling baseline of output distributions (embeddings of responses, classification label distributions) from a "healthy" period; (2) **Statistical tests**: PSI (Population Stability Index) for input feature drift, Jensen-Shannon divergence for output distribution drift; (3) **LLM-as-judge drift**: periodically re-score a sample of live outputs against the golden evaluation rubric; (4) **Alerts**: trigger on >10% PSI threshold or >5% quality score degradation; (5) **Actions**: auto-revert to previous model version, notify team, trigger human evaluation sprint .

**Q153. What is RBAC vs. ABAC for AI system authorization and which fits financial services?**

*   **RBAC** (Role-Based): permissions tied to roles (Analyst, Trader, Compliance). Simple, auditable, but coarse-grained.
    
*   **ABAC** (Attribute-Based): permissions evaluated by policies combining user attributes (role, clearance, location, time) + resource attributes (doc classification, jurisdiction, sensitivity). For banking AI: ABAC is required because a Trader in Sydney should see different documents than a Trader in Auckland, even with the same role. Implement via OPA (Open Policy Agent) evaluated at the AI gateway layer.
    

**Q154. How do you design an immutable audit trail for AI decisions in a regulated environment?**

Architecture: (1) Every AI decision event (input, retrieved context, model output, tool calls, final response) written as an immutable event to Azure Event Hub → ADLS Gen2 in Parquet format (append-only, WORM storage); (2) Event schema includes: session\_id, user\_id, model\_version, prompt\_hash, response\_hash, timestamp, classification; (3) Query interface via Azure Synapse for compliance reporting; (4) Hash chain linking events (each event includes hash of previous) for tamper evidence; (5) Retention: 7 years for credit decisions per ASIC requirements.

**Q155. What is the MITRE ATLAS framework for AI security?**

MITRE ATLAS (Adversarial Threat Landscape for Artificial Intelligence Systems) is the AI-equivalent of the MITRE ATT&CK framework. It catalogs adversarial tactics and techniques targeting AI systems: reconnaissance (model extraction), resource development (adversarial ML tools), initial access (data poisoning), persistence (backdoor embedding), evasion (adversarial examples), and exfiltration (model inversion attacks). AI architects use it to conduct threat modeling sessions and design mitigations.

**Q156. How do you handle PII in a RAG system under Australian Privacy Act obligations?**

(1) **Pre-ingestion**: PII detection (Presidio, AWS Comprehend Medical) → entity substitution (replace names/TFNs with tokens before embedding); (2) **Token mapping vault**: encrypted store mapping tokens back to real values, accessed only by authorized downstream services; (3) **At retrieval**: re-substitute tokens before LLM injection only if user has PII access authorization; (4) **At output**: output scanner strips any PII that slipped through; (5) **Data minimization**: only ingest the minimum PII required for the use case; (6) **Retention**: automated deletion of PII embeddings when source record deleted (right to erasure compliance).

**Architecture Scenarios**

**Q157. How would you architect an AI-powered fraud detection system using agentic patterns?**

_(See Architecture Section below for full diagram)_Agents: (1) **Ingestion Agent**: real-time transaction stream from Kafka, feature extraction; (2) **Pattern Agent**: ML model scoring (XGBoost + LightGBM ensemble) for statistical anomaly detection; (3) **Investigation Agent**: for flagged transactions, performs graph traversal (related accounts/merchants/devices), RAG against fraud case knowledge base, device fingerprint lookup; (4) **Decision Agent**: synthesizes all signals, generates risk score + explanation; (5) **Action Agent**: routes to automated block (high confidence), human review queue (medium), or allow (low risk); (6) **Learning Agent**: periodically ingests confirmed fraud cases back into training pipeline.​

**Q158. Design an AI architecture for a bank's loan application processing.**

End-to-end flow: Document submission → Azure Document Intelligence extraction → Data normalization agent → Credit scoring agent (ensemble ML + LLM explanation) → Fraud check agent (cross-reference with fraud KB) → Compliance agent (responsible lending checks, IRFS 9 provisioning) → Risk pricing agent → Decision synthesis agent → HITL review for borderline cases → Decision output with explainability report → Audit log to WORM storage.​

**Q159. How would you architect a conversational AI system for a wealth management firm that must pass ASIC's digital advice regulations?**

Key requirements: SOI (Statement of Advice) generation, appropriate advice boundary detection, client suitability assessment, disclosure obligations. Architecture: (1) Suitability assessment agent (collects risk profile via structured dialogue); (2) Products RAG agent (searches approved product list with AFSL-aligned filtering); (3) Compliance guardrail layer (validates advice against RG 255 digital advice rules); (4) SOI generation agent (structured document with required disclosures); (5) HITL escalation for complex scenarios; (6) Full session audit trail. Critically: no advice on excluded financial products without licensed adviser in loop.

**Q160. How do you design an AI architecture for code review automation across a 500-developer engineering organization?**

Platform: (1) GitHub Actions trigger on PR → webhook to AI Review Service; (2) Diff extraction → chunking by file/function; (3) Language-aware RAG (retrieve coding standards, architectural patterns, security rules); (4) Code review agent generates: bugs, security issues, architecture violations, test coverage gaps; (5) Severity classifier routes critical findings to block merge, suggestions to advisory comments; (6) Feedback loop — developers accepting/rejecting suggestions trains classification quality; (7) Metrics: PR cycle time reduction, defect escape rate, developer satisfaction.

**Q161. Architect a multi-modal AI system for processing bank statements (PDFs + images + structured data).**

Pipeline: (1) Document type classifier (PDF text vs. scanned image vs. structured export); (2) Path A (digital PDF): direct text extraction → table parser → structured JSON.

