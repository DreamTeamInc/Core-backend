from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from skimage.segmentation import felzenszwalb



def index(request):
    return HttpResponse("Hello World!")

@csrf_exempt
def loadphoto(request):
    if request.method == "POST":
        photo = request.FILES['file']
        segments = felzenszwalb(photo, scale=50, sigma=10, min_size=100)  # return numpy.ndarray
        lists = segments.tolist()
        json_str = json.dumps(lists)
        return JsonResponse({'segments': json_str})
    else:
        return HttpResponse("<h2>No photo yet</h2>")