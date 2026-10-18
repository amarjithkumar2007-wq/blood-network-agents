# Blood Network agents (Fetch-A-Thon 3.0 Round 1 prototype)

Three Fetch.ai uAgents: Seeker -> Matcher -> Facility -> Seeker.

- Seeker: turns a free-text request into a structured one (rule-based now; ASI:One planned) and rejects spam / money asks.
- Matcher: ranks compatible donors past their cooldown (blood 90d, plasma 28d, platelets 14d), exact group first, nearest first.
- Facility A: asks donors one at a time, moves on after a decline, only uses its own facility's donors (no referrals).

Demo data is synthetic (donors.py). Donor replies are scripted. No real messages are sent.
Status: runs locally with uAgents (Bureau). Not yet hosted on Agentverse. ASI:One not wired in.
Built with AI coding assistance.

Run: pip install uagents pytest; python agents_demo.py "O positive blood chahiye urgent"; pytest -q
