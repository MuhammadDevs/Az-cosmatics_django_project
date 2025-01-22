from django.shortcuts import redirect

def auth_middleware(get_response):
    def middleware(request):
        print(request.session.get('customer'))
        if not request.session.get('customer'):  # Corrected 'Customer' to 'customer'
            request.session['return_url'] = request.path  # Store the current path
            return redirect('login_page')
        response = get_response(request)
        return response

    return middleware
