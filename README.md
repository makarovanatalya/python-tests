# python-tests

### image for testing

to run server:
```
docker run -d -p 4111:4111 --name nbank nobugsme/nbank:with_validation_fix
```

swagger:
```
http://localhost:4111/swagger-ui/index.html
```

to install dependencies:
```
pip install -r requirements.txt
```

to run all tests:
```
python -m pytest
```

run linter after changing the code:
```
ruff check .
```