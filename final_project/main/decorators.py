from django.http import HttpResponse


# def allowed_groups(allowed_roles):
#     def decorator(view_func):
#         def wrapper(request, *args, **kwargs):
#             group = None
#             if request.groups.user.exists():
#                 group = request.user.groups.all()[0].name
#             if group in allowed_roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponse('You have to be a Trainer to enter this page')
#         return wrapper
#     return decorator
