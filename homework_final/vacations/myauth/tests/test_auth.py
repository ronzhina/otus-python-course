import os

import django
import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacations.settings")
django.setup()
from ..models import Department, Position


class AuthTest(TestCase):

    @classmethod
    @pytest.mark.django_db
    def setUpClass(cls):
        super().setUpClass()
        Department.objects.get_or_create(name='УР')
        Position.objects.get_or_create(name='программист')
        cls.user_data = {
            'username': 'pol',
            'name': 'ivan',
            'surname': 'ivanov',
            'patronymic': 'ivanovich',
            'department': Department.objects.get(name='УР').pk,
            'position': Position.objects.get(name='программист').pk,
            'password1': 'OtusOtus',
            'password2': 'OtusOtus',
        }
        cls.user_invalid_password = {
            'username': 'pol',
            'name': 'ivan',
            'surname': 'ivanov',
            'patronymic': 'ivanovich',
            'department': Department.objects.get(name='УР').pk,
            'position': Position.objects.get(name='программист').pk,
            'password1': 'OtusOtus',
            'password2': 'Otus',
        }
        cls.user_with_not_existing_data = {
            'username': 'pol',
            'name': 'ivan',
            'surname': 'ivanov',
            'patronymic': 'ivanovich',
            'department': 'notexist',
            'position': 'notexist',
            'password1': 'OtusOtus',
            'password2': 'OtusOtus',
        }

    def test_success_register(self):
        response = self.client.post(
            reverse('myauth:register'),
            data=self.user_data
        )
        print(response.content.decode())
        assert response.status_code == 302

        new_user = get_user_model().objects.get(
            username=self.user_data['username']
        )

        assert self.user_data['name'] == new_user.name

    def test_fail_register_with_password_mismatch(self):
        response = self.client.post(
            reverse('myauth:register'),
            data=self.user_invalid_password,
            follow=True
        )
        print(response.content.decode())
        assert response.status_code == 200

        assert len(response.context_data['form'].errors) == 1
        assert response.context_data['form'].errors['password2'] == [_(
            'The two password fields didn’t match.')]

    def test_fail_register_with_empty_data(self):
        response = self.client.post(
            reverse('myauth:register'),
            data={},
            follow=True
        )
        print(response.context_data['form'].errors)
        assert response.status_code == 200
        assert len(response.context_data['form'].errors) == 8
        for field in ['username', 'name', 'surname', 'patronymic', 'department', 'position', 'password1', 'password2']:
            assert response.context_data['form'].errors[field] == ['Обязательное поле.']

    def test_fail_register_with_not_existing_department_and_position(self):
        response = self.client.post(
            reverse('myauth:register'),
            data=self.user_with_not_existing_data,
            follow=True
        )
        print(response.context_data['form'].errors)
        assert response.status_code == 200
        assert len(response.context_data['form'].errors) == 2

        for field in ['department', 'position']:
            assert response.context_data['form'].errors[field] == [
                'Выберите корректный вариант. Вашего варианта нет среди допустимых значений.']
