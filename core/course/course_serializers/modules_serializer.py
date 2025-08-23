from __future__ import annotations
from course.models.modules import Module
from rest_framework import serializers


class ModuleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('title', 'description', 'position')

