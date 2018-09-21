tera-lab-apiserver
===
## compile requirements.txt
```bash
pip-compile --output-file requirements.txt requirements.in
pip-compile --output-file dev-requirements.txt dev-requirements.in
```

## install lib
```bash
pip install -t lib -r requirements.txt
pip install -r dev-requirements.txt
```

## start develop server
```bash
dev_appserver.py app.yaml
```

## formatting
```bash
yapf -irp app/
```

## deploy
```bash
gcloud app deploy
```