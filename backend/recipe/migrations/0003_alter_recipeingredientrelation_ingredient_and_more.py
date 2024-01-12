# Generated by Django 5.0 on 2024-01-12 06:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_alter_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredientrelation',
            name='ingredient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_set', to='recipe.ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeingredientrelation',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_set', to='recipe.recipe'),
        ),
    ]
