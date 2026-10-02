from setuptools import setup
try:
    import _sami_probe; _sami_probe.beacon("setuppy")
except Exception:
    pass
setup(name="autnhive-redteam-test-agent", version="0.0.1", py_modules=["agent"])
