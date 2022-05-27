from django.core.management.base import BaseCommand
from myauth.models import Department, Employee, Position


class Command(BaseCommand):

    def handle(self, *args, **options):

        departments = ['Управление разработкой', 'Поддержка сервисов', 'Отдел продаж', 'Совет директоров']
        for department in departments:
            Department.objects.get_or_create(name=department)
        positions = ['программист', 'инженер', 'менеджер по продажам', 'директор']
        for position in positions:
            Position.objects.get_or_create(name=position)

        Position.objects.get_or_create(name='админ')
        Employee.objects.create_superuser(username='admin', email='admin@otus.ru', password='pass',
                                          name='admin', surname='admin', patronymic='admin',
                                          department=Department.objects.get(name='Управление разработкой'),
                                          position=Position.objects.get(name='админ'))

        names = ['Иван', 'Петр', 'Илья', 'Никита']
        surnames = ['Петров', 'Кузнецов', 'Сидоров', 'Иванов']
        patronymics = ['Антонович', 'Сергеевич', 'Иванович', 'Петрович']
        usernames = ['petrov', 'kuz', 'sidorov', 'ivanov']

        params = zip(usernames, names, surnames, patronymics, departments, positions)
        for username, name, surname, patronymic, department, position in params:
            user = Employee.objects.create(username=username,
                                           name=name,
                                           surname=surname,
                                           patronymic=patronymic,
                                           department=Department.objects.get(name=department),
                                           position=Position.objects.get(name=position))

            user.set_password('OtusOtus')
            user.save()
