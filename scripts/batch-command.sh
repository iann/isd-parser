find . ! -path . -maxdepth 1 -type d -print | xargs -I {} python data-loader.py ish-history.csv {}
