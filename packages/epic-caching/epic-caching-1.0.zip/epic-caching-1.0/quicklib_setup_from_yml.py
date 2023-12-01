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

ql_setup_kwargs = {'name': 'epic-caching', 'description': 'Utilities for caching', 'long_description': {'filename': 'README.md', 'content_type': 'text/markdown'}, 'author': 'Assaf Ben-David, Uri Sternfeld, Yonatan Perry', 'license': 'MIT License', 'url': 'https://github.com/Cybereason/epic-caching', 'python_requires': '>=3.10', 'top_packages': ['epic'], 'version_module_paths': ['epic/caching'], 'install_requires': ['decorator'], 'classifiers': ['Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: POSIX :: Linux', 'Operating System :: MacOS :: MacOS X', 'Operating System :: Microsoft :: Windows', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10']}    

quicklib.setup(
    **ql_setup_kwargs
)
