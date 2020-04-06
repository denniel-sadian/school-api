from rest_framework.views import APIView

from serializers import UserEmployeeSerializer


class CreateUserEmployeeView(APIView):

    def post(self, request):
        data = UserEmployeeSerializer(data=request.POST)
