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

ql_setup_kwargs = {'name': 'epic-lab', 'description': 'Opinionated research lab management tools', 'long_description': {'filename': 'README.md', 'content_type': 'text/markdown'}, 'author': 'Yonatan Perry, Assaf Ben-David, Uri Sternfeld', 'license': 'MIT License', 'url': 'https://github.com/Cybereason/epic-lab', 'python_requires': '>=3.10', 'top_packages': ['epic'], 'version_module_paths': ['epic/lab'], 'manifest_extra': ['recursive-include epic/lab/scripts *', 'recursive-include epic/lab/vmsetup *'], 'classifiers': ['Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: POSIX :: Linux', 'Operating System :: MacOS :: MacOS X', 'Operating System :: Microsoft :: Windows', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10'], 'scripts': ['epic/lab/scripts/epic-synccode', 'epic/lab/scripts/epic-notebook'], 'entry_points': {'console_scripts': ['epic-lab = epic.lab.main:main']}}    

quicklib.setup(
    **ql_setup_kwargs
)
