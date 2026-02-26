# OpenClawMD - Skill Generator

**AI Skill Creation Platform**

Generate OpenClaw-compatible skills for AI agents (Claude, Gemini, Qwen, Codex, OpenCode) in seconds.

## Quick Start

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Start API Service

```bash
python3 openclaw_api_service.py
```

Server starts on: `http://localhost:5000`

### 3. Open Website

Open `openclaw_website.html` in your browser, or serve it:

```bash
python3 -m http.server 8080
```

Then visit: `http://localhost:8080/openclaw_website.html`

---

## API Endpoints

### Health Check
```bash
GET /
```

### List Templates
```bash
GET /skills/templates
```

**Response:**
```json
{
  "templates": {
    "build-exact": {
      "name": "Build:Exact",
      "description": "Complete development framework",
      "pattern": "protocol",
      "category": "development"
    }
  },
  "patterns": ["cli-wrapper", "python-script", "protocol"],
  "categories": ["development", "tools", "diagnosis", "optimization", "collaboration"]
}
```

### Generate Skill
```bash
POST /skills/generate
Content-Type: application/json

{
  "name": "Consistency Checker",
  "slug": "consistency-checker",
  "version": "1.0.0",
  "description": "Auto-check for skill compatibility",
  "pattern": "python-script",
  "ownerId": "my-team",
  "author": "John Doe",
  "script_name": "consistency_check"
}
```

**Response:**
```json
{
  "success": true,
  "skill_id": "abc123def456",
  "download_url": "/skills/download/abc123def456",
  "preview": {
    "name": "Consistency Checker",
    "slug": "consistency-checker",
    "version": "1.0.0",
    "pattern": "python-script"
  },
  "spec_prompt": "name: consistency-checker\nslug: consistency-checker\n..."
}
```

### Download Skill
```bash
GET /skills/download/:skill_id
```

Returns ZIP file with:
- `SKILL.md`
- `_meta.json`
- `scripts/*.py` (if applicable)
- `README.md`

---

## Patterns

### CLI Wrapper
For wrapping existing CLI tools.

**Required fields:**
- `install_steps` (semicolon-separated)

**Example:**
```
kind=brew,bins=rtk,label=Install RTK; kind=pip,bins=jq,label=Install jq
```

### Python Script
For custom Python automation.

**Required fields:**
- `script_name` (optional, auto-generated if missing)

**Output:**
- `scripts/{script_name}.py`

### Protocol
For workflows and processes.

**No additional fields required**

---

## Website Features

### Input Form
- Skill name, slug, description
- Owner ID and author
- Version (default: 1.0.0)
- Pattern selection (CLI/Python/Protocol)
- Pattern-specific fields
- Examples

### Output
- Live SPEC preview
- ZIP download link
- Success/error messages

---

## Deployment

### Local Development
```bash
# Terminal 1: API
python3 openclaw_api_service.py

# Terminal 2: Website
python3 -m http.server 8080
```

### Production (Vercel)

1. Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    { "src": "openclaw_api_service.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "openclaw_api_service.py" }
  ]
}
```

2. Deploy:
```bash
vercel deploy --prod
```

### Production (Docker)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python3", "openclaw_api_service.py"]
```

Build and run:
```bash
docker build -t openclawmd .
docker run -p 5000:5000 openclawmd
```

---

## Integration with Agent Deck

Generated skills can be directly used with Agent Deck:

```bash
# Download skill
curl -O http://localhost:5000/skills/download/abc123def456

# Extract to skill-db
unzip abc123def456.zip -d ~/.agent-deck/skill-db/official/

# Update registry
~/.agent-deck/skill-db/skill-db.sh sync
```

---

## Example Usage

### cURL Example
```bash
curl -X POST http://localhost:5000/skills/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "RTK Token Saver",
    "slug": "rtk-token-saver",
    "version": "1.0.0",
    "description": "Wrapper for RTK CLI",
    "pattern": "cli-wrapper",
    "ownerId": "agent-deck-team",
    "install_steps": "kind=cargo,bins=rtk,label=Install RTK"
  }'
```

### JavaScript Example
```javascript
const response = await fetch('http://localhost:5000/skills/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'My Skill',
    slug: 'my-skill',
    description: 'Does something cool',
    pattern: 'protocol',
    ownerId: 'my-team'
  })
});

const result = await response.json();
console.log(result.download_url);
```

---

## Business Model

### Free Tier
- 3 skills per month
- Basic patterns
- ZIP download

### Pro Tier (€9/month)
- Unlimited skills
- Custom patterns
- API access
- Priority support

### Enterprise Tier (€49/month)
- White-label
- Custom domain
- Team access
- Analytics

---

## Roadmap

- [ ] User authentication
- [ ] Skill marketplace
- [ ] Payment integration (Stripe)
- [ ] Analytics dashboard
- [ ] Custom pattern builder
- [ ] Team collaboration
- [ ] Version history
- [ ] Skill validation API

---

## License

MIT License

## Credits

Based on Claude Superpowers framework and OpenClaw specification.

Built for openclawmd.com
