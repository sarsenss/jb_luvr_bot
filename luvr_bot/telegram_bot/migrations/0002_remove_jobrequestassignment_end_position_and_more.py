# Generated by Django 4.2.1 on 2023-05-30 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobrequestassignment',
            name='end_position',
        ),
        migrations.RemoveField(
            model_name='jobrequestassignment',
            name='start_position',
        ),
        migrations.AddField(
            model_name='employee',
            name='INN',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='ИНН сотрудника'),
        ),
        migrations.AddField(
            model_name='employee',
            name='full_name',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='ФИО сотрудника'),
        ),
        migrations.AddField(
            model_name='jobrequest',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_requests', to='telegram_bot.employee', verbose_name='сотрудник'),
        ),
        migrations.AddField(
            model_name='jobrequest',
            name='status',
            field=models.CharField(blank=True, choices=[('APPROVED', 'Принята'), ('REJECTED', 'Отклонена'), ('CANCELED', 'Отменена')], max_length=250, null=True, verbose_name='статус заявки'),
        ),
        migrations.AddField(
            model_name='jobrequestassignment',
            name='status',
            field=models.CharField(blank=True, choices=[('ADMITTED', 'Подтверждено'), ('NOT ADMITTED', 'Неподтверждено')], max_length=250, null=True, verbose_name='статус назначения'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Admin'), (3, 'Branch manager'), (2, 'Chain manager')], null=True),
        ),
        migrations.AlterField(
            model_name='employeegeoposition',
            name='geo_positions_date',
            field=models.DateTimeField(auto_now=True, verbose_name='дата внесения гео позиций'),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_requests', to='telegram_bot.branch', verbose_name='филиал'),
        ),
        migrations.AlterField(
            model_name='jobrequestassignment',
            name='assignment_date',
            field=models.DateTimeField(auto_now=True, verbose_name='дата назначения'),
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_date', models.DateTimeField(auto_now=True, verbose_name='дата смены')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shifts', to='telegram_bot.jobrequestassignment', verbose_name='назначение')),
                ('end_position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='end_assignments', to='telegram_bot.employeegeoposition', verbose_name='окончание смены')),
                ('start_position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='start_assignments', to='telegram_bot.employeegeoposition', verbose_name='начало смены')),
            ],
            options={
                'verbose_name': 'Смена',
                'verbose_name_plural': 'Смены',
            },
        ),
    ]
