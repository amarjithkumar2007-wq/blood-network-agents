"""Blood Network agent team on Fetch.ai uAgents: Seeker -> Matcher -> Facility -> Seeker."""
import sys
from uagents import Agent, Bureau, Context, Model
from logic import parse_request, rank
from donors import DONORS

class RawRequest(Model):
    text: str
class StructuredRequest(Model):
    group: str
    component: str
    urgent: bool
    facility: str
class Shortlist(Model):
    request: StructuredRequest
    donor_ids: list[str]
class Outcome(Model):
    ok: bool
    message: str
    log: list[str]

seeker = Agent(name="bn-seeker", seed="bn-demo-seeker-seed", port=8101, endpoint=["http://127.0.0.1:8101/submit"])
matcher = Agent(name="bn-matcher", seed="bn-demo-matcher-seed", port=8102, endpoint=["http://127.0.0.1:8102/submit"])
facility = Agent(name="bn-facility-a", seed="bn-demo-facility-seed", port=8103, endpoint=["http://127.0.0.1:8103/submit"])
REQUEST_TEXT = " ".join(sys.argv[1:]) or "O positive blood chahiye Dilsukhnagar urgent"
RESULT = {}

@seeker.on_event("startup")
async def start(ctx: Context):
    ctx.logger.info(f"family says: {REQUEST_TEXT!r}")
    p = parse_request(REQUEST_TEXT)
    if not p["ok"]:
        ctx.logger.info(f"rejected: {p['reason']}")
        RESULT["done"] = p["reason"]
        return
    await ctx.send(matcher.address, StructuredRequest(group=p["group"], component=p["component"], urgent=p["urgent"], facility=p["facility"]))
    ctx.logger.info(f"structured request sent to matcher: {p}")

@matcher.on_message(StructuredRequest)
async def match(ctx: Context, sender: str, msg: StructuredRequest):
    ids = [d.id for d in rank(msg.model_dump())]
    ctx.logger.info(f"ranked donors (compatible, past cooldown, nearest first): {ids}")
    await ctx.send(facility.address, Shortlist(request=msg, donor_ids=ids))

@facility.on_message(Shortlist)
async def ask(ctx: Context, sender: str, msg: Shortlist):
    log = []
    by_id = {d.id: d for d in DONORS}
    for did in msg.donor_ids:
        d = by_id[did]
        if d.facility != "Facility A":      # rule 3: only its own facility, no referrals
            log.append(f"{did}: skipped (belongs to {d.facility})")
            continue
        ctx.logger.info(f"asking {did} (one at a time)")
        if d.will_accept:                    # scripted demo reply
            log.append(f"{did}: accepted")
            await ctx.send(seeker.address, Outcome(ok=True, message=f"{did} accepted, donate at Facility A", log=log))
            return
        log.append(f"{did}: declined, moving to next")
    await ctx.send(seeker.address, Outcome(ok=False, message="no donor at Facility A accepted; family should call the blood bank", log=log))

@seeker.on_message(Outcome)
async def done(ctx: Context, sender: str, msg: Outcome):
    ctx.logger.info(f"RESULT ok={msg.ok}: {msg.message}")
    for l in msg.log: ctx.logger.info(f"  {l}")
    RESULT["done"] = msg.message

if __name__ == "__main__":
    bureau = Bureau()
    for a in (seeker, matcher, facility): bureau.add(a)
    print("ADDRESSES", seeker.address, matcher.address, facility.address)
    import asyncio, threading, os, time
    def stop():
        for _ in range(60):
            time.sleep(0.5)
            if "done" in RESULT: time.sleep(1); os._exit(0)
        os._exit(1)
    threading.Thread(target=stop, daemon=True).start()
    bureau.run()
