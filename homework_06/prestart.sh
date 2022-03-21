set -e

echo "Apply migrations"

flask db upgrade

echo "migrations ok"

exec "$@"