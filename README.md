tera-lab-apiserver
===
## compile requirements.txt
```bash
pip-compile --output-file requirements.txt requirements.in
```

## install lib
```bash
pip install --target lib --requirement requirements.txt
```

## start develop server
```bash
dev_appserver.py app.yaml
```

## deploy
```bash
gcloud app deploy
```