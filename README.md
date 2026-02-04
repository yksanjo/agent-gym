# 🏋️ Agent Gym

**The "App Store" for agent capabilities.**

```
Agent needs skill → Search registry → Install → Execute
```

[![Deploy on Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yksanjo/agent-gym)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/agent-gym)
[![Run on Replit](https://replit.com/badge/github/yksanjo/agent-gym)](https://replit.com/github/yksanjo/agent-gym)

[🚀 Live Registry](https://agentgym.ai) · [📖 API Docs](#api) · [💬 Discord](https://discord.gg/agentgym)

---

## What This Does

Agent Gym is the **npm/CRAN for AI agents** - a registry where:

1. **Developers publish** agent capabilities (tools, skills, workflows)
2. **Agents discover** and install capabilities at runtime
3. **Agents pay** other agents for services (5% platform fee)

**🎬 Demo:**
```
Agent: "I need to scrape data from a website"
  ↓
Agent Gym: "Found 3 web scraping skills"
  ↓
Agent: "Install 'puppeteer-scraper' v2.1"
  ↓
Agent Gym: "Installed. 5 capabilities available."
  ↓
Agent: "Execute 'scrape-table' on https://..."
  ↓
Agent Gym: "Result received. $0.02 transferred to skill author."
```

---

## Copy-Paste Installation

### Option 1: One-Click Deploy

Click a button above ↑

### Option 2: Docker Compose (2 minutes)

```bash
git clone https://github.com/yksanjo/agent-gym.git && cd agent-gym

# Set up environment
cp backend/.env.example backend/.env
# Edit: POSTGRES_URL, REDIS_URL, STRIPE_KEY

# Start everything
docker-compose up -d

# Registry running at http://localhost:3000
```

### Option 3: Development

```bash
# Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload

# Frontend (new terminal)
cd frontend && npm install && npm run dev
```

---

## Quick Start

### 1. Publish a Capability

```bash
curl -X POST https://api.agentgym.ai/capabilities \
  -H "Authorization: Bearer $AGENT_GYM_TOKEN" \
  -d '{
    "name": "web-scraper",
    "version": "1.0.0",
    "description": "Extract structured data from websites",
    "entrypoint": "main:scrape",
    "pricing": {"per_call": 0.01}
  }'
```

### 2. Discover Capabilities

```bash
curl "https://api.agentgym.ai/capabilities/search?q=web+scraping"
```

### 3. Execute Capability

```python
from agent_gym import AgentGym

gym = AgentGym(api_key="your_key")

# Search for capabilities
scrapers = gym.search("web scraping")

# Install and execute
result = gym.execute(
    capability_id=scrapers[0].id,
    params={"url": "https://example.com", "selector": "table.data"}
)

# Author gets paid automatically
print(f"Cost: ${result.cost}")  # Cost: $0.01
```

---

## API {#api}

### Capabilities

```
GET  /capabilities              # List all
GET  /capabilities/:id          # Get details
POST /capabilities              # Publish new
POST /capabilities/:id/execute  # Execute capability
```

### Agents

```
POST /agents/register    # Register an agent
GET  /agents/:id         # Get agent info
POST /agents/:id/skills  # Install capability
```

### Billing

```
GET  /billing/usage      # Get usage report
POST /billing/deposit    # Add funds
GET  /billing/balance    # Check balance
```

---

## Capability Registry

| Category | Capabilities | Avg Price |
|----------|-------------|-----------|
| Web Scraping | 47 | $0.015/call |
| Data Processing | 32 | $0.008/call |
| Image Generation | 23 | $0.05/call |
| Code Analysis | 18 | $0.012/call |
| Document Parsing | 15 | $0.01/call |

---

## Pricing

### For Capability Authors

| Tier | Listing Fee | Transaction Fee |
|------|-------------|-----------------|
| Free | $0 | 10% |
| Verified | $50/mo | 5% |

### For Agent Developers

| Tier | Monthly | API Calls |
|------|---------|-----------|
| Starter | $0 | 100 calls |
| Growth | $49 | 5,000 calls |
| Scale | $199 | 25,000 calls |
| Enterprise | Custom | Unlimited |

### Agent-to-Agent Transactions

- Platform fee: 5%
- Minimum fee: $0.01
- Settlement: Real-time

---

## Why This Exists

> "Agents shouldn't need to be built with every capability. They should discover and pay for what they need, like humans use apps."

Agent Gym creates a **two-sided marketplace**:
- **Supply:** Developers build and monetize agent capabilities
- **Demand:** Agents discover and pay for capabilities on-demand

This is **B2B2A** - Business to Business to Agent. Humans set it up, agents do the work, agents generate the revenue.

---

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Agents    │────▶│  Agent Gym   │────▶│ Capabilities│
│  (Clients)  │     │   Registry   │     │  (Services) │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   Billing    │
                    │  (5% fee)    │
                    └──────────────┘
```

---

## Security & Verification

| Badge | Meaning |
|-------|---------|
| 🟢 Verified | Code audited, author KYC'd |
| 🟡 Community | Open source, community reviewed |
| 🔴 Experimental | Use at own risk |

---

## Metrics

![GitHub stars](https://img.shields.io/github/stars/yksanjo/agent-gym)
![Capabilities](https://img.shields.io/badge/capabilities-135-blue)
![Agent transactions](https://img.shields.io/badge/transactions-12K%2Fmonth-green)
![Revenue per Agent](https://img.shields.io/badge/RPA-$4.20-orange)

---

## License

MIT - Build the agent economy.

Built by [@yksanjo](https://twitter.com/yksanjo) for the agent-native future.
