from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from skimage.segmentation import felzenszwalb
from .models import User


def index(request):
    return HttpResponse("Hello World!")


@csrf_exempt
def loadphoto(request):
    if request.method == "POST":
        photo = request.FILES['file']
        # segments = felzenszwalb(photo, scale=50, sigma=10, min_size=100)  # return numpy.ndarray
        # lists = segments.tolist()
        # json_str = json.dumps(lists)
        return HttpResponse(photo, content_type = "multipart/form-data")
    else:
        return HttpResponse("<h2>No photo yet</h2>")


def get_all_users(request):
    result = []
    users = User.objects.all()
    for user in users:
        result.append({
            'id': user.id,
            'first_name': user.first_name,
            'second_name': user.second_name,
            'patronymic': user.patronymic,
            'bitrh_date': user.birth_date,
            'email': user.email,
            'password': user.password,
            'company': user.company,
            'position': user.position,
            'sex': user.sex,
            'is_su': user.is_su,
            'created_date': user.created_date,
        })
    return JsonResponse(result, safe=False)
