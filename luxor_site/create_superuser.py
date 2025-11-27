from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

try:
    User = get_user_model()

    if not User.objects.filter(username="postgres").exists():
        User.objects.create_superuser(
            username="postgres",
            email="admin@mail.com",
            password="DjangoWeb2"
        )
        print("Superuser created")
    else:
        print("Superuser already exists")

except OperationalError:
    print("Database not available, try again after migrations")