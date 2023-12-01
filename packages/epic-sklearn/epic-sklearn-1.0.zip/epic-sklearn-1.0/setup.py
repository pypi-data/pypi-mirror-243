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

ql_setup_kwargs = {'name': 'epic-sklearn', 'description': 'An expansion pack for scikit-learn', 'long_description': {'filename': 'README.md', 'content_type': 'text/markdown'}, 'author': 'Assaf Ben-David, Yonatan Perry, Uri Sternfeld', 'license': 'MIT License', 'url': 'https://github.com/Cybereason/epic-sklearn', 'python_requires': '>=3.10', 'top_packages': ['epic'], 'version_module_paths': ['epic/sklearn'], 'install_requires': ['numpy>=1.21.5', 'pandas>=1.4.4', 'scipy>=1.7.3', 'scikit-learn>=1.1.1', 'cytoolz', 'matplotlib', 'joblib', 'ultima', 'epic-logging', 'epic-common', 'epic-pandas'], 'classifiers': ['Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: POSIX :: Linux', 'Operating System :: MacOS :: MacOS X', 'Operating System :: Microsoft :: Windows', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10']}    

quicklib.setup(
    **ql_setup_kwargs
)
