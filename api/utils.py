def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_param(request, name):
    val = request.GET.get(name)
    if val is None and request.method == "POST":
        val = request.POST.get(name)

    return val


def get_user(request):
    if not hasattr(request, 'user'):
        return None

    return request.user.id
    # id = request.session.get('wx_id')
    # request.session['wx_id'] = 1
    # return id if id else 1


def set_user(request, id):
    request.session['wx_id'] = id
