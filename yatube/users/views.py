from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordResetView

from .forms import ContactForm, CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordReset(PasswordResetView):
    success_url = reverse_lazy('users:prd')
    template_name = 'users/password_reset_form.html'


def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.cleaned_data['name']
            form.cleaned_data['email']
            form.cleaned_data['subject']
            form.cleaned_data['body']
            form.save()
            return redirect('/thank-you/')
        return render(request, 'contact.html', {'form': form})
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})
