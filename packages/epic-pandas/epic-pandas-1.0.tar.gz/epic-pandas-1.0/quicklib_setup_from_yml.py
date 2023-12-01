# -------- quicklib direct/bundled import, copy pasted --------------------------------------------
import sys as _sys, glob as _glob, os as _os
is_packaging = not _os.path.exists("PKG-INFO")
if is_packaging:
    import quicklib
else:
    zips = _glob.glob("quicklib_incorporated.*.zip")
    if len(zips) != 1:
        raise Exception("expected exactly one incorporated quicklib zip but found %s" % (zips,))
    _sys.path.insert(0, zips[0]); import quicklib; _sys.path.pop(0)
# -------------------------------------------------------------------------------------------------

ql_setup_kwargs = {'name': 'epic-pandas', 'description': 'Extra treats for the data-oriented', 'long_description': {'filename': 'README.md', 'content_type': 'text/markdown'}, 'author': 'Assaf Ben-David, Yonatan Perry, Uri Sternfeld', 'license': 'MIT License', 'url': 'https://github.com/Cybereason/epic-pandas', 'python_requires': '>=3.10', 'top_packages': ['epic'], 'version_module_paths': ['epic/pandas'], 'install_requires': ['numpy>=1.21.5', 'pandas>=1.4.4', 'scipy>=1.7.3', 'matplotlib>=3.5.2', 'networkx', 'toolz', 'decorator', 'ultima', 'epic-common'], 'classifiers': ['Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: POSIX :: Linux', 'Operating System :: MacOS :: MacOS X', 'Operating System :: Microsoft :: Windows', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10']}    

quicklib.setup(
    **ql_setup_kwargs
)
