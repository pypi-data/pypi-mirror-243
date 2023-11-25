# Generated by Django 4.2.1 on 2023-10-23 14:26

from django.db import IntegrityError, migrations, models, transaction

import lnschema_bionty.ids


def forwards_func(apps, schema_editor):
    """Replace strings in registry and registries."""
    Organism = apps.get_model("lnschema_bionty", "Organism")
    db_alias = schema_editor.connection.alias
    # see https://stackoverflow.com/a/23326971
    try:
        with transaction.atomic():
            try:
                # human
                record = Organism.objects.using(db_alias).get(name="human")
                record.uid = "EeBGvIYd"
                record.ontology_id = "NCBITaxon:9606"
                record.save()
            except Organism.DoesNotExist:
                pass
            try:
                # mouse
                record = Organism.objects.using(db_alias).get(name="mouse")
                record.uid = "Is9wp9mQ"
                record.ontology_id = "NCBITaxon:10090"
                record.save()
            except Organism.DoesNotExist:
                pass
            try:
                # yeast
                record = Organism.objects.using(db_alias).get(name="saccharomyces cerevisiae")
                record.uid = "XapD5kLk"
                record.ontology_id = "NCBITaxon:559292"
                record.save()
            except Organism.DoesNotExist:
                pass
    except IntegrityError:
        pass


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        (
            "lnschema_bionty",
            "0018_organism_rename_species_biontysource_organism_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="organism",
            old_name="taxon_id",
            new_name="ontology_id",
        ),
        migrations.AlterField(
            model_name="organism",
            name="ontology_id",
            field=models.CharField(db_index=True, default=None, max_length=32, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="organism",
            name="uid",
            field=models.CharField(default=lnschema_bionty.ids.ontology, max_length=8, unique=True),
        ),
        migrations.AddField(
            model_name="organism",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_bionty.organism"),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
