try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # for Python < 3.8
    from importlib_metadata import version, PackageNotFoundError 

__version__ = version("pymol-loader")
