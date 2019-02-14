from distutils.version import LooseVersion
import blocksci

if LooseVersion(blocksci.VERSION) < LooseVersion("0.6"):
    raise ImportError("BlockSci Utils require BlockSci v0.6 or newer.")
