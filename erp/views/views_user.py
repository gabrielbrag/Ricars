from django.shortcuts import redirect
from .views_base import BaseView, DataTableListView
from django.views.generic import UpdateView, CreateView, DeleteView
from accounts.models import CustomUser
from accounts.management.commands import createcustomuser
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied


class UserListView(DataTableListView):
    model = CustomUser
    columns = ['document', 'name', 'email']
    insert_view_route_name = 'user_create'
    edit_view_route_name = 'user_edit'
    delete_view_route_name = 'user_delete'

class UserBaseView(BaseView):
    model = CustomUser
    fields = ['username', 'email', 'name', 'document', 'password']
    template_name = 'registration/user_edit.html'
    success_url = reverse_lazy('user_list')

class UserCreateView(UserBaseView, CreateView):
    def form_valid(self, form):
        user_creation_handler = createcustomuser.UserCreationHandler()
        print("oeee")
        try:
            user = user_creation_handler.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'],
                document=form.cleaned_data['document'],
                password=form.cleaned_data['password'],
            )
            
            return redirect(self.success_url)
        
        except ValueError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
    
class UserUpdateView(UserBaseView, UpdateView):
    pass

class UserDeleteView(UserBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        number_of_users = self.model.objects.count()
        if number_of_users > 1:
            return self.delete(request, *args, **kwargs)
        else:
            raise PermissionDenied("Cannot delete the last user.")