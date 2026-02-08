import requests
import time
import sys
import urllib3

# --- Non-Functional Requirements: Documentation & Assumptions ---
# Assumption 1: The test container and nginx-server are in the same Docker network.
# Assumption 2: Ports 8080, 8081, and 443 are correctly exposed as per the assignment.
# Design Decision: Using the service name 'nginx-server' as the hostname, leveraging Docker's internal DNS.
# Trade-off: verify=False and disabling warnings is used to support self-signed certificates in a lab environment.
# This avoids the complexity of a private CA while still testing the SSL/TLS handshake.

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NGINX_HOST = "nginx-server"
ENDPOINTS = {
    "HTTP_MAIN": f"http://{NGINX_HOST}:8080",
    "HTTP_ERROR": f"http://{NGINX_HOST}:8081",
    "HTTPS_SECURE": f"https://{NGINX_HOST}:443"
}

def test_status_codes():
    """
    Checks if ports 8080 and 8081 return the expected status codes.
    Design Decision: Segregating the main server from the error server to test multi-port configuration.
    """
    print("--- Running Functional Status Code Tests ---")
    try:
        # Port 8080: Expected 200 OK
        r1 = requests.get(ENDPOINTS["HTTP_MAIN"], timeout=5)
        if r1.status_code == 200:
            print("[PASS] Port 8080: OK (200)")
        else:
            print(f"[FAIL] Port 8080: Expected 200, got {r1.status_code}")
            return False

        # Port 8081: Expected 500 Internal Server Error as required
        r2 = requests.get(ENDPOINTS["HTTP_ERROR"], timeout=5)
        if r2.status_code == 500:
            print("[PASS] Port 8081: Correctly returned error (500)")
        else:
            print(f"[FAIL] Port 8081: Expected 500, got {r2.status_code}")
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Status tests encountered a connection issue: {e}")
        return False

def test_https():
    """
    Validates HTTPS connectivity on port 443.
    Trade-off: verify=False is used because certificates are self-signed.
    """
    print("\n--- Running HTTPS Security Test ---")
    try:
        r = requests.get(ENDPOINTS["HTTPS_SECURE"], verify=False, timeout=5)
        if r.status_code == 200:
            print("[PASS] HTTPS: Handshake successful and returned OK (200)")
            return True
        else:
            print(f"[FAIL] HTTPS: Unexpected status code {r.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] HTTPS Connection failed: {e}")
        return False

def test_rate_limiting():
    """
    Validates Rate Limiting implementation (5r/s with burst=5).
    Design Decision: Sending 20 requests rapidly to ensure we exceed the burst limit and trigger a 503 error.
    """
    print("\n--- Running Rate Limiting Security Test ---")
    print("Simulating traffic spike (20 requests)...")
    throttled = False
    
    for _ in range(20):
        try:
            # We use the main HTTP port to test the rate limit zone
            r = requests.get(ENDPOINTS["HTTP_MAIN"], timeout=1)
            if r.status_code == 503:
                throttled = True
                break
        except:
            continue
            
    if throttled:
        print("[PASS] Rate limiting active: 503 Service Unavailable detected")
        return True
    
    print("[FAIL] Rate limiting not detected. Server allowed all 20 requests")
    return False

if __name__ == "__main__":
    # Assumption: Nginx needs a few seconds to initialize its listeners within the container.
    time.sleep(2) 
    
    results = [test_status_codes(), test_https(), test_rate_limiting()]
    
    # Final verdict for CI/CD Pipeline
    if all(results):
        print("\n🏆 VERDICT: ALL TESTS PASSED")
        sys.exit(0) # Exit code 0 signals success to GitHub Actions
    else:
        print("\n❌ VERDICT: SOME TESTS FAILED")
        sys.exit(1) # Exit code 1 signals failure to GitHub Actions