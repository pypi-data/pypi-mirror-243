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

ql_setup_kwargs = {'name': 'epic-bitstore', 'description': 'Multi-tiered cloud-backed blob storage system', 'long_description': {'filename': 'README.md', 'content_type': 'text/markdown'}, 'author': 'Yonatan Perry, Uri Sternfeld, Assaf Ben-David', 'license': 'MIT License', 'url': 'https://github.com/Cybereason/epic-bitstore', 'python_requires': '>=3.10', 'top_packages': ['epic'], 'version_module_paths': ['epic/bitstore'], 'install_requires': ['epic-common', 'epic-logging'], 'extras_require': {'aws': ['boto3'], 'gcp': ['requests', 'google-auth', 'google-cloud-storage']}, 'classifiers': ['Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: POSIX :: Linux', 'Operating System :: MacOS :: MacOS X', 'Operating System :: Microsoft :: Windows', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10']}    

quicklib.setup(
    **ql_setup_kwargs
)
