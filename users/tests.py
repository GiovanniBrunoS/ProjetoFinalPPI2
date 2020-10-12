from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import CustomUser

def create_user(name):
    UserModel = get_user_model()
    if not UserModel.objects.filter(username=name).exists():
        user = UserModel.objects.create_user(name, password='!@SDRDsada55')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class UserTestCase(TestCase):

    def setUp(self):
        admin = create_user('testeUser')

    def test_user(self):
        usuario = CustomUser.objects.get(username='testeUser')
        self.assertEqual(str(usuario), 'testeUser')

