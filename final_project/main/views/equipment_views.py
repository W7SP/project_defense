from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic as views
from final_project.accounts.models import Profile
from final_project.main.models import Equipment


# Create New Equipment (requires some permissions)
class CreateEquipmentView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Equipment
    fields = ('name', 'price', 'description', 'warranty',)
    template_name = 'equipment/create_equipment.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('main.add_courses'):
            return HttpResponse('You must be a trainer to create new courses!')

        return super(CreateEquipmentView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


# Edit Equipment View (requires Trainer's permissions)
class EditEquipmentView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Equipment
    fields = ('name', 'price', 'description',)
    template_name = 'equipment/edit_equipment.html'
    success_url = reverse_lazy("user's listings")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('main.change_equipment'):
            return HttpResponse('You must be the trainer to edit the equipment!')

        return super(EditEquipmentView, self).dispatch(request, *args, **kwargs)


# Delete Equipment View (requires Author's permissions)
class DeleteEquipmentView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Equipment
    fields = ()
    template_name = 'equipment/delete_equipment.html'
    success_url = reverse_lazy("user's listings")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('main.delete_equipment'):
            return HttpResponse('You must be the trainer to delete the equipment!')

        return super(DeleteEquipmentView, self).dispatch(request, *args, **kwargs)


# Show Equipment Shop items
class EquipmentShopView(views.ListView):
    model = Equipment
    template_name = 'marketplace/equipment_shop.html'
    context_object_name = 'equipments'


# Buy Equipment
class BuyEquipmentView(views.UpdateView):
    model = Equipment
    fields = ()
    template_name = 'marketplace/buy_equipment.html'
    success_url = reverse_lazy('index')

    def get(self, *args, **kwargs):
        result = super().get(*args, **kwargs)
        equipment = self.object
        user = self.request.user.id
        profile = Profile.objects.get(user_id=user)
        if profile.account_balance >= equipment.price:
            profile.account_balance -= equipment.price
            profile.save()
            equipment.owners.add(profile)
        else:
            return HttpResponse('u poor')

        return result