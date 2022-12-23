'''from rest_framework import serializers

from .models import LNMOnline


class LNMOnlineSerializer(serializers.ModelSerializer):
    metadata = serializers.JSONField(allow_null=True)
    class Meta:
        model = LNMOnline
        fields = ('id','metadata',)
'''