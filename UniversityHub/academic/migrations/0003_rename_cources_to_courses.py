from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0002_rename_heaad_of_dept_department_head_of_dept'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='cources',
            new_name='courses',
        ),
    ]
