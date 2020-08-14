
## Installation

```bash
# flask
conda activate imtr
cd pipeline_runner
pip install -r requirements.txt

# redis
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
cp src/redis-server /nfs/users/nfs_c/cellgeni-su/local/bin
cp src/redis-cli /nfs/users/nfs_c/cellgeni-su/local/bin
```

## To start

```
# flask
conda activate imtr
cd pipeline_runner
export FLASK_APP=app.py
export FLASK_DEBUG=1
nohup flask run --host=0.0.0.0 &

# redis
nohup redis-server &

# celery
cd ..
celery -A pipeline_runner.celery_app:celery_app worker -l info
```

## To end
```bash
# flask
lsof -ti:5000 | xargs kill -9

# celery
 pkill -f "celery worker"
```