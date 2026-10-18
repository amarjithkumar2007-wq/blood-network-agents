from logic import parse_request, rank
def test_parse():
    r = parse_request("O positive blood chahiye Dilsukhnagar urgent")
    assert r["ok"] and r["group"] == "O+" and r["urgent"]
def test_spam_money():
    assert not parse_request("O+ needed, send money on paytm first")["ok"]
def test_no_group():
    assert not parse_request("need a donor")["ok"]
def test_rank_cooldown_and_compat():
    ids = [d.id for d in rank(parse_request("O positive urgent"))]
    assert "donor-3" not in ids      # donated 30 days ago, blood cooldown is 90
    assert "donor-4" not in ids      # A+ cannot give to O+
    assert ids[0] == "donor-1"       # exact group, nearest eligible
def test_platelet_cooldown_shorter():
    ids = [d.id for d in rank(parse_request("O positive platelets"))]
    assert "donor-3" in ids          # 30 days >= 14
