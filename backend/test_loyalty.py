import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "http://127.0.0.1:8000"

def test(path, method="GET", data=None, token=None):
    url = BASE + path
    try:
        req = urllib.request.Request(url, method=method)
        if data:
            req.add_header("Content-Type", "application/json")
            req.data = json.dumps(data).encode()
        if token:
            req.add_header("Authorization", "Bearer " + token)
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()[:130]
            print(f"[OK]   {method:6} {path} -> {resp.status} | {body}")
            return json.loads(body + "...") if "..." in body else json.loads(resp.read().decode() or body)
    except Exception as e:
        print(f"[FAIL] {method:6} {path} -> {e}")
        if hasattr(e, "read"):
            print("       ->", e.read().decode()[:200])
        return None

# 1. Get token
req = urllib.request.Request(BASE + "/api/v1/auth/login", method="POST")
req.add_header("Content-Type", "application/json")
req.data = json.dumps({"email": "customer@agrixanh.vn", "password": "customer123"}).encode()
with urllib.request.urlopen(req) as resp:
    tok = json.loads(resp.read())["access_token"]
    print("Token:", tok[:40], "...")

print("\n--- Loyalty Endpoints ---")
test("/api/v1/loyalty/profile",       token=tok)
test("/api/v1/loyalty/addresses",     token=tok)
test("/api/v1/loyalty/points",        token=tok)
test("/api/v1/loyalty/tiers")
test("/api/v1/loyalty/transactions",  token=tok)

print("\n--- Add Address ---")
test("/api/v1/loyalty/addresses", "POST",
     {"recipient_name": "Trần Thị Hoa", "phone": "0901234567", "address_line": "123 Nguyễn Huệ", "ward": "P. Bến Nghé", "district": "Q. 1", "province": "TP. HCM", "is_default": True},
     tok)

print("\n--- List Addresses again ---")
test("/api/v1/loyalty/addresses", token=tok)

print("\n--- Redeem Preview ---")
test("/api/v1/loyalty/points/redeem", "POST",
     {"order_amount": 250000, "points_to_use": 50},
     tok)

print("\nAll tests done!")
