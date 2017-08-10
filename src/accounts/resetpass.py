from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import FormView
from .forms import PasswordResetRequestForm, SetPasswordForm
from .models import StudentProfile


class ResetPasswordRequestView(FormView):
    template_name = 'accounts/forgot_pass.html'
    success_url = '/accounts/login-site/'
    form_class = PasswordResetRequestForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'error_404.html')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'error_404.html')
        form = self.form_class(request.POST)
        if not form.is_valid():
            messages.error(request, 'Invalid Input')
            return self.form_invalid(form)
        student_id = form.cleaned_data.get('student_id')
        users = StudentProfile.objects.filter(student_id=student_id)
        if not users.exists():
            messages.error(request,
                           'This username does not exist in the system.')
            return self.form_invalid(form)
        user = users[0]
        if not user.private_email:
            messages.error(request,
                           """This user hasn't register any private email
                           ,please contact Administrator to reset your password""")
            return self.form_invalid(form)
        content = {
            'email': user.private_email,
            'domain': 'http://127.0.0.1:8000',
            'site_name': 'SIS',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        subject_template_name = 'accounts/password_reset_subject.html'
        email_template_name = 'accounts/password_reset_email.html'
        subject = loader.render_to_string(subject_template_name, content)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, content)
        send_mail(subject, email, settings.DEFAULT_FROM_EMAIL,
                  [user.private_email],
                  fail_silently=False)
        messages.success(request,
                         """Email has been sent to {}'s email address.
                          Please check its inbox to 
                          continue reseting password.""".format(user.name))
        return self.form_valid(form)


class PasswordResetConfirmView(FormView):
    template_name = 'accounts/forgot_pass.html'
    success_url = '/accounts/login-site'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = StudentProfile._default_manager.get(pk=uid)
        except (
                TypeError, ValueError, OverflowError,
                StudentProfile.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user,
                                                        token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request,
                               'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request,
                           'The reset password link is no longer valid.')
            return self.form_invalid(form)
