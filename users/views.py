from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging

logger = logging.getLogger('__name__')

class SignUp(generic.CreateView):
    form_class =  CustomUserCreationForm
    success_url =  reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def user_list(request):
    UserModel = get_user_model()
    users = UserModel.objects.all() 

    return render(request, 'registration/user_list.html', {'users': users})

@login_required
def user_remove(request, pk):
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, pk=pk)
    if(request.user.is_staff):
        user.delete()
        messages.warning(request,"Usuario removido com sucesso")
    else:
        logger.error("Usuario não autorizado tentando fazer remoção de usuario")

    return redirect('user_list')

@login_required
def user_edit(request, pk):
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, pk=pk)
    if request.method == "POST":
         form = CustomUserChangeForm(request.POST, instance=user)
         if form.is_valid():
             form.save()
             logger.info("Usuario editado com sucesso")
             messages.success(request,"Usuario editado com sucesso")
             return redirect('user_list')
    else:
         form = CustomUserChangeForm(instance=user)
    return render(request, 'registration/user_edit.html', {'form': form})
