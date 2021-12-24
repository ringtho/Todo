from rest_framework.serializers import ModelSerializer
from base.models import Task

# Create your models here.
class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"