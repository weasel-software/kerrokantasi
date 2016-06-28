# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-23 12:23
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class InitialSectionType:
    INTRODUCTION = "introduction"
    PART = "part"
    SCENARIO = "scenario"
    CLOSURE_INFO = "closure-info"


INITIAL_SECTION_TYPE_DATA = [
    {
        'identifier': InitialSectionType.INTRODUCTION,
        'name_singular': 'johdanto',
        'name_plural': 'johdannot',
    },
    {
        'identifier': InitialSectionType.CLOSURE_INFO,
        'name_singular': 'sulkeutumistiedote',
        'name_plural': 'sulkeutumistiedotteet',
    },
    {
        'identifier': InitialSectionType.SCENARIO,
        'name_singular': 'vaihtoehto',
        'name_plural': 'vaihtoehdot',
    },
    {
        'identifier': InitialSectionType.PART,
        'name_singular': 'osa-alue',
        'name_plural': 'osa-alueet',
    },
]


def create_initial_section_types(section_type_model):
    for section in INITIAL_SECTION_TYPE_DATA:
        section_type_model.objects.update_or_create(identifier=section['identifier'], defaults=section)


def add_initial_section_types(apps, schema_editor):
    create_initial_section_types(apps.get_model('democracy', 'SectionType'))


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('democracy', '0008_comment_plugins'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='time of creation')),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of last modification')),
                ('published', models.BooleanField(db_index=True, default=True, verbose_name='public')),
                ('deleted', models.BooleanField(db_index=True, default=False, editable=False, verbose_name='deleted')),
                ('identifier', autoslug.fields.AutoSlugField(editable=False, populate_from='name_singular', unique=True)),
                ('name_singular', models.CharField(max_length=64)),
                ('name_plural', models.CharField(max_length=64)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sectiontype_created', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sectiontype_modified', to=settings.AUTH_USER_MODEL, verbose_name='last modified by')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(add_initial_section_types, lambda x, y: None),
        migrations.AlterField(
            model_name='section',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sections', to='democracy.SectionType'),
        ),
    ]