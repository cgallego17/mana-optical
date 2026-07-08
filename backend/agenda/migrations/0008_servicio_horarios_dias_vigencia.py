from django.db import migrations, models


def migrar_horarios_por_dia(apps, schema_editor):
    Servicio = apps.get_model('agenda', 'Servicio')
    for s in Servicio.objects.all():
        if s.hora_inicio and s.hora_fin:
            dias = s.dias_disponibles if s.dias_disponibles else list(range(7))
            inicio = s.hora_inicio.strftime('%H:%M')
            fin = s.hora_fin.strftime('%H:%M')
            s.horarios_dias = {str(d): {'inicio': inicio, 'fin': fin} for d in dias}
            s.save(update_fields=['horarios_dias'])


def revertir_horarios_por_dia(apps, schema_editor):
    Servicio = apps.get_model('agenda', 'Servicio')
    for s in Servicio.objects.all():
        if s.horarios_dias:
            primero = next(iter(s.horarios_dias.values()))
            s.hora_inicio = primero['inicio']
            s.hora_fin = primero['fin']
            s.save(update_fields=['hora_inicio', 'hora_fin'])


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0007_servicio_hora_fin_servicio_hora_inicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='horarios_dias',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='servicio',
            name='vigencia_desde',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='servicio',
            name='vigencia_hasta',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.RunPython(migrar_horarios_por_dia, revertir_horarios_por_dia),
        migrations.RemoveField(
            model_name='servicio',
            name='hora_inicio',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='hora_fin',
        ),
    ]
