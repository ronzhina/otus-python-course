from django.core.management.base import BaseCommand

from claims.models import Department, Employee, Position


class Command(BaseCommand):

    def handle(self, *args, **options):
        departments = ['Управление разработкой', 'Поддержка сервисов', 'Отдел продаж', 'Совет директоров']
        for department in departments:
            Department.objects.get_or_create(name=department)
        positions = ['программист', 'инженер', 'менеджер по продажам', 'директор']
        for position in positions:
            Position.objects.get_or_create(name=position)

        names = ['Иван', 'Петр', 'Илья', 'Никита']
        surnames = ['Петров', 'Кузнецов', 'Сидоров', 'Иванов']
        patronymics = ['Антонович', 'Сергеевич', 'Иванович', 'Петрович']

        params = zip(names, surnames, patronymics, departments, positions)
        for name, surname, patronymic, department, position in params:
            Employee.objects.get_or_create(name=name,
                                           surname=surname,
                                           patronymic=patronymic,
                                           department=Department.objects.get(name=department),
                                           position=Position.objects.get(name=position))
