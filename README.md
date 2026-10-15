# Campus Customs Desk (HW 5)

A team of five AI agents (Boss, Inventory Ina, Accounting Ama, Facilities Father, Customer Service Jervis) works the shop's three open tickets (101, 102, 103). They read the shop through an MCP server, and a React board lets a human watch them and approve or deny any payment.

```
data/          the shop database: campus_customs.db (original) and campus_customs_new.db (working copy)
mcp_server/    the MCP server every agent uses to read the shop (server.py, shop_db.py)
backend/       FastAPI routes (main.py), data types (models.py), the five agents, prompts/<agent>.md
frontend/      the React + Vite + TypeScript board
output/        harness.md, design.md, desk_tickets.html, resolved_tickets.json, resolved_board.html,
               audit_trail.json, mcp_smoke.json, github_url.txt, screenshots/ (the board images)
```

## One-time setup

1. Python packages (Python 3.14 was used). Keep the virtual environment outside iCloud-synced folders, or syncing makes everything very slow:
   ```bash
   python3 -m venv ~/venvs/hw5
   ~/venvs/hw5/bin/pip install -r requirements.txt
   ```
2. Your key: copy `.env.example` to `.env` (in this folder or the parent folder) and set `PORTKEY_API_KEY`. Never commit `.env`.
3. The board's packages:
   ```bash
   cd frontend && npm install
   ```
4. `.mcp.json` has absolute paths to this machine's Python and `server.py`. Edit them if you move the project (only needed if you want Claude Code itself to connect to the MCP server).

## Clean run: reset the database first

Always reset before a full three-ticket run, so cash starts at $3,400.00 and every ticket starts open. Any one of these does it:

- Copy the original over the working copy:
  ```bash
  cp data/campus_customs.db data/campus_customs_new.db
  ```
- Or press **Fresh start** on the board, or call `POST http://localhost:8000/reset` (the backend does the same copy through the MCP server).

## Start everything

1. **MCP server.** `mcp_server/server.py` is started for you: the backend launches it itself when it boots. To run it by hand (it speaks MCP over stdio):
   ```bash
   ~/venvs/hw5/bin/python mcp_server/server.py
   ```
2. **FastAPI backend** (http://localhost:8000):
   ```bash
   cd backend
   ~/venvs/hw5/bin/uvicorn main:app --reload --port 8000
   ```
   It takes a little while to start because it boots the MCP server.
3. **React board** (http://localhost:5173), in a second terminal:
   ```bash
   cd frontend
   npm run dev
   ```

## Run the three tickets

1. Reset the database (above).
2. On the board, pick ticket 101 and press **Start the team**. When the Boss asks for a payment, a slip appears: press **Approve & pay** or **Deny**. Only Approve moves cash.
3. Run again after an approved payment so the Boss can finish the ticket (a ticket resolves when a run ends with nothing waiting on you). Repeat for 102 and 103.
4. Every agent step is appended to `output/audit_trail.json`. It is never wiped.

No terminal version is needed, but `python run_tickets.py` (from this folder, with the venv's Python) does a reset and then runs the tickets, asking you before each payment.

## Safety rules in short

Human approval for any payment; the pay tools refuse if cash is short; no real emails or calls; no card details, SSNs or passwords; customer money only for what they bought. The full list is in `output/harness.md`.
