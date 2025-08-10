# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
#
#
# def generate_activation_link(request, user):
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)
#     domain = get_current_site(request).domain
#     path = reverse("member-activate", kwargs={"uidb64": uid, "token": token})
#     return f"http://{domain}{path}"
#
#
# def decode_uid(uidb64):
#     return force_str(urlsafe_base64_decode(uidb64))
