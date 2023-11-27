import pkg_resources

try:
    version = pkg_resources.require("versionix")[0].version
except: #pragma: no cover
    version = ">=0.1.0"
