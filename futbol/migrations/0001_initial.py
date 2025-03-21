# Generated by Django 4.2 on 2025-02-28 15:07

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, unique=True)),
                ('any_fundacio', models.IntegerField()),
                ('estadi', models.CharField(blank=True, max_length=100, null=True)),
                ('ciutat', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Lliga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, unique=True)),
                ('pais', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Partit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(blank=True, null=True)),
                ('equip_local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partits_locals', to='futbol.equip')),
                ('equip_visitant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partits_visitants', to='futbol.equip')),
                ('lliga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partits', to='futbol.lliga')),
            ],
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('posicio', models.CharField(choices=[('PT', 'Porter'), ('DF', 'Defensa'), ('MC', 'Migcampista'), ('DL', 'Davanter')], max_length=50)),
                ('dorsal', models.IntegerField()),
                ('nacionalitat', models.CharField(max_length=50)),
                ('equip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jugadors', to='futbol.equip')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipus_esdeveniment', models.CharField(choices=[('gol', 'Gol'), ('targeta_groga', 'Targeta Groga'), ('targeta_vermella', 'Targeta Vermella'), ('substitucio', 'SubstituciÃ³')], max_length=50)),
                ('minut', models.IntegerField()),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='futbol.jugador')),
                ('partit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='futbol.partit')),
            ],
        ),
        migrations.AddField(
            model_name='equip',
            name='lliga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equips', to='futbol.lliga'),
        ),
        migrations.CreateModel(
            name='Usuari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telefon', models.CharField(max_length=14)),
                ('equips', models.ManyToManyField(to='futbol.equip')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
