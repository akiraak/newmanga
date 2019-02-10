# newmanga

## setup

## Start server

```
$ FLASK_APP=newmanga.py FLASK_ENV=development flask run --host=0.0.0.0 --port=5001
```

# Update books
Add to crontab
0 * * * * /home/akiraak/projects/newmanga/fetchbooks_pro.sh