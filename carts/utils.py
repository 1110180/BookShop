from carts.models import Cart


def get_user_carts(req):
    if req.user.is_authenticated:
        return Cart.objects.filter(user=req.user).select_related('product')
    
    if not req.session.session_key:
        req.session.create()
    return Cart.objects.filter(session_key=req.session.session_key).select_related('product')