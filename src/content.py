class BaseContent:
    
    def get_gitignore():
        return """.idea
.ipynb_checkpoints
.mypy_cache
.vscode
__pycache__
.pytest_cache
htmlcov
dist
site
.coverage
coverage.xml
.netlify
test.db
log.txt
Pipfile.lock
env3.*
env
.env
docs_build
venv
docs.zip
archive.zip

logs/*

# vim temporary files
*~
.*.sw?"""