from django.db import models


class Employee(models.Model):
    phone_number = models.CharField(max_length=250, verbose_name='номер телефона')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.phone_number


class EmployeeGeoPosition(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='geo_positions', verbose_name='сотрудник')
    latitude = models.CharField(max_length=300, verbose_name='широта')
    longitude = models.CharField(max_length=300, verbose_name='долгота')

    class Meta:
        verbose_name = 'Геопозиция сотрудника'
        verbose_name_plural = 'Геопозиция сотрудников'


class Branch(models.Model):
    branch_name = models.CharField(max_length=250,  verbose_name='название филиала')
    latitude = models.CharField(max_length=300,  verbose_name='широта')
    longitude = models.CharField(max_length=300,  verbose_name='долгота')

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.branch_name


class JobRequest(models.Model):
    # deal_id
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='job_requests')
    employee_position = models.CharField(blank=True, null=True, max_length=300, verbose_name='должность')
    request_type = models.CharField(blank=True, null=True, max_length=250, verbose_name='тип заявки')
    date_start = models.DateField(blank=True, null=True, verbose_name='дата начала периода')
    date_end = models.DateField(blank=True, null=True, verbose_name='дата окончания периода')
    shift_date = models.DateField(blank=True, null=True, verbose_name='дата смены')
    shift_hours = models.DateTimeField(blank=True, null=True, verbose_name='время смены')
    number_of_employees = models.CharField(max_length=3, blank=True, null=True, verbose_name='количество сотрудников')
    request_comment = models.TextField(blank=True, null=True, verbose_name='комментарий')

    class Meta:
        verbose_name = 'Заявка на сотрудников'
        verbose_name_plural = 'Заявки на сотрудников'

    def __str__(self):
        return f'{self.request_type} - {self.branch}'


class JobRequestAssignment(models.Model):
    job_request = models.ForeignKey(JobRequest, on_delete=models.CASCADE, related_name='assignments', verbose_name='заявка на сотрудника')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assignments', verbose_name='сотрудник')

    class Meta:
        verbose_name = 'Назначение сотрудников'
        verbose_name_plural = 'Назначения сотрудников'
