alembic upgrade head
# check if migrations are up to date
if [ $? -eq 0 ]; then
    echo "Migrations are up to date"
else
    echo "Migrations are not up to date"
    exit 1
fi
python main.py
