from rest_framework.viewsets import ModelViewSet

from .models import Exam
from .models import Item
from .models import Choice
from .models import Session
from .serializers import ExamSerializer
from .serializers import ItemSerializer
from .serializers import ChoiceSerializer
from .serializers import SessionSerializer


class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ChoiceViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ChoiceSerializer
