from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Student


# 例子
class QueryStudent(APIView):
    @staticmethod
    def get(request):
        """
        """
        req = request.query_params.dict()#前端给的json包数据
        student_name = req["student_name"]

        student_id = Student.objects.filter(student_name=student_name).values("student_id")#提取数据表中数据
        return Response(student_id)#返回数据，这里由于提取数据表中数据直接就是jason格式所以可以直接传，其他的需要转为json格式

    @staticmethod
    def post(request):
        """
        """
        req = request.data#前端给的json包数据
        student_id = req["student_id"]
        student_name = req["student_name"]

        Student(student_id=student_id,student_name=student_name).save()#保存数据
        print('收到:id为{},name为{}'.format(student_id,student_name))

        return Response()#不需要返回数据
