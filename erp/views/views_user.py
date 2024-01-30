from .views_base import BaseView, DataTableListView
from django.views.generic import UpdateView, CreateView, DeleteView
from accounts.models import CustomUser
from accounts.management.commands import createcustomuser
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

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
    pass

class UserUpdateView(UserBaseView, UpdateView):
    pass

class UserDeleteView(UserBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)