from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    
    if User.objects.filter(username="admin_managing_Double88").exists():
        return 

    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin_managing_Double88",
            email="admin@example.com",
            password="Q7#vL9!xZ2@pR8$kT6"
        )
