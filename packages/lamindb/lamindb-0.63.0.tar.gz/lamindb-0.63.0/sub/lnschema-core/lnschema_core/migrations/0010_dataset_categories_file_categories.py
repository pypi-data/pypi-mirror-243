# Generated by Django 4.2.2 on 2023-07-21 07:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0009_remove_featureset_files_feature_unit_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="categories",
            field=models.ManyToManyField(related_name="datasets", to="lnschema_core.category"),
        ),
        migrations.AddField(
            model_name="file",
            name="categories",
            field=models.ManyToManyField(related_name="files", to="lnschema_core.category"),
        ),
        migrations.AddField(
            model_name="tag",
            name="description",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="tag",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_core.tag"),
        ),
        migrations.RenameField(
            model_name="run",
            old_name="external_id",
            new_name="reference",
        ),
        migrations.RenameField(
            model_name="run",
            old_name="name",
            new_name="reference_type",
        ),
        migrations.DeleteModel(
            name="Project",
        ),
        migrations.AddField(
            model_name="file",
            name="tags",
            field=models.ManyToManyField(related_name="files", to="lnschema_core.tag"),
        ),
        migrations.RunSQL("insert into lnschema_core_file_tags (id, file_id, tag_id) select id, file_id, tag_id from lnschema_core_tag_files"),
        migrations.RemoveField(
            model_name="tag",
            name="files",
        ),
        migrations.AddField(
            model_name="file",
            name="input_of",
            field=models.ManyToManyField(related_name="input_files", to="lnschema_core.run"),
        ),
        migrations.RunSQL("insert into lnschema_core_file_input_of (id, file_id, run_id) select id, file_id, run_id from lnschema_core_run_inputs"),
        migrations.RemoveField(
            model_name="run",
            name="inputs",
        ),
        migrations.AlterField(
            model_name="file",
            name="run",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="output_files", to="lnschema_core.run"),
        ),
    ]
