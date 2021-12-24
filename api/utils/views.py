from django.http import JsonResponse

def error404(request, exception):
    message=('This endpoint does not exist')
    response=JsonResponse(data={'message':message, 'status_code':404})
    response.status_code = 404
    return response

def error500(request):
    message=('The task with that id does not exist in the database.')
    response=JsonResponse(data={'message': message, 'status_code':500})
    response.status_code = 500
    return response