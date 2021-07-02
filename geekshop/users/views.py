from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import FormView
from django.utils.decorators import method_decorator


from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User
from baskets.models import Basket


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'GeekShop - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {
        'title': 'GeekShop - Регистрация',
        'form': form
    }
    return render(request, 'users/register.html', context)


@login_required()
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=user)
    context = {
        'title': 'GeekShop - Личный кабинет',
        'form': form,
        'baskets': Basket.objects.filter(user=user)
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


# class GeekShopLogin(LoginView):
#     authentication_form = UserLoginForm
#     template_name = 'users/login.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(GeekShopLogin, self).get_context_data()
#         context['title'] = 'GeekShop - Авторизация'
#         return context
#
#
# class GeekShopRegister(CreateView):
#     model = User
#     template_name = 'users/register.html'
#     form_class = UserRegisterForm
#     success_url = reverse_lazy('users:login')
#
#     def get_context_data(self, **kwargs):
#         context = super(GeekShopRegister, self).get_context_data()
#         context['title'] = 'GeekShop - Регистрация'
#         return context
#
#
# class GeekShopProfile(UpdateView):
#     model = User
#     template_name = 'users/profile.html'
#     form_class = UserProfileForm
#     # success_url = reverse_lazy('users:profile')
#
#     def get_context_data(self, object_list=None, **kwargs):
#         context = super(GeekShopProfile, self).get_context_data()
#         context.update({
#             'title': 'GeekShop - Личный кабинет',
#             'baskets': Basket.objects.filter(user=self.request.user)
#         })
#         # context['title'] = 'GeekShop - Личный кабинет'
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('users:profile', args=(self.object.id,))
#
#     @method_decorator(login_required())
#     def dispatch(self, request, *args, **kwargs):
#         return super(GeekShopProfile, self).dispatch(request, *args, **kwargs)


class GeekShopLogout(LogoutView):
    next_page = 'index'