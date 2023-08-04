from .views_base import DataTableMixin
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.core.serializers import serialize
from django.http import JsonResponse
from erp.models import Vehicle, Brand, Vehicle_model, Vehicle_model_variant, Vehicle_image,  Vehicle_cost_type, Vehicle_cost
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.forms.widgets import CheckboxInput
import json

class VehicleListView(DataTableMixin, TemplateView):
    template_name = 'erp/default_list.html'

    def get_data_table(self):
        dataTableColumns = [_("Vehicle"), _("Year"), _("Color"), _("Purchase price"), _("Sale price"), _("Sold")]
        rows = []
        for vehicle in Vehicle.objects.all():
            vehicleValues = []
            vehicleValues.append(vehicle.vehicle_variant)
            vehicleValues.append(vehicle.model_year)
            vehicleValues.append(vehicle.color)
            vehicleValues.append(vehicle.purchase_price_formatted)
            vehicleValues.append(vehicle.sale_value_formatted)
            vehicleValues.append(vehicle.sold_as_checkbox)
            vehicleValues.append(self.mountEditIcon(reverse('vehicle_edit', kwargs={'pk': vehicle.pk})))
            vehicleValues.append(self.mountDeleteIcon(reverse('vehicle_delete', kwargs={'pk': vehicle.pk})))
            rowsValue = {"values":vehicleValues}
            rows.append(rowsValue)

        data_table = {
            'columns': dataTableColumns,
            'rows': rows,
            'insertViewURL':reverse_lazy('vehicle_create'),
            'editViewURL':'vehicle_edit',
            'deleteViewURL':'vehicle_delete'
        }
        return data_table

class VehicleBaseView:
    model = Vehicle
    fields = ['vehicle_variant', 
                'model_year', 
                'manufacture_year',
                'color', 
                'transmission',
                'mileage',
                'fuel_type',
                'number_of_doors',
                'license_plate',
                'purchase_price', 
                'sale_value',
                'sold',
                'salesman_observation']
                
    template_name = 'erp/forms/vehicle_edit.html'
    success_url = reverse_lazy('vehicle_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        form = self.get_form()

        fields_manually_created = ['vehicle_variant', 'salesman_observation']

        for field_name, field in form.fields.items():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check'               
            else:
                field.widget.attrs['class'] = 'form-control'

        automatic_fields  = [field for field in form if field.name not in fields_manually_created]
        context['automatic_fields'] = automatic_fields

        manual_fields = []
        for field in form:
            if field not in automatic_fields:
                manual_fields.append(field)


        context['manual_fields'] = manual_fields

        return context
    

class VehicleCreateView(VehicleBaseView, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all() 

        cost_types = Vehicle_cost_type.objects.all()
        context['cost_types'] = cost_types 

        return context


    def form_valid(self, form):
        response = super().form_valid(form)
        vehicle = self.object

        inserted_files = self.request.FILES.getlist('inserted_files')  # Get the list of uploaded files

        for index, image_file in enumerate(inserted_files):
            vehicle_image = Vehicle_image(vehicle=vehicle, file=image_file, index=(index + 1))
            vehicle_image.save()

        vehicle_cost_data = json.loads(self.request.POST.get('vehicle_cost_data'))
    
        for cost in vehicle_cost_data:
            vehicle_cost_type = Vehicle_cost_type.objects.get(pk=cost["cost_type_id"])

            vehicle_cost = Vehicle_cost(vehicle=vehicle, 
                                        cost_type=vehicle_cost_type, 
                                        cost_name=cost["cost_name"], 
                                        expense_date=cost["expense_date"],
                                        value=cost["cost_value"])
            
            vehicle_cost.save()

        return response    

class VehicleUpdateView(VehicleBaseView, UpdateView):    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.get_object()  # Get the current vehicle object
        vehicle_brand = vehicle.vehicle_variant.vehicle_model.brand  # Access the brand through the relationships
        context['vehicle_brand'] = vehicle_brand  # Pass the brand to the template context

        cost_types = Vehicle_cost_type.objects.all()
        context['cost_types'] = cost_types 

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        
        self.handleImageFiles()
        
        self.handleVehicleCost()

        return response    

    def handleImageFiles(self):
        existing_files_ids_string = self.request.POST.get('existing_files_ids', '')

        # Split the string by commas and remove any leading/trailing whitespace
        existing_files_ids = [id.strip() for id in existing_files_ids_string.split(',') if id.strip()]

        # Validate the IDs to ensure they are valid integers
        try:
            existing_files_ids = [int(id) for id in existing_files_ids]
        except ValueError:
            return HttpResponseBadRequest("Invalid input: existing_files_ids must be a comma-separated list of integers.")

        vehicle = self.get_object()
        vehicle_images = vehicle.images.all()
        
        for image in vehicle_images:
            if not image.pk in existing_files_ids:
                image.delete() 

        inserted_files = self.request.FILES.getlist('inserted_files')  # Get the list of uploaded files

        for index, image_file in enumerate(inserted_files):
            vehicle_image = Vehicle_image(vehicle=vehicle, file=image_file, index=(index + 1))
            vehicle_image.save()

    def handleVehicleCost(self):
        try:
            vehicle_cost_data = json.loads(self.request.POST.get('vehicle_cost_data'))
            vehicle = self.get_object()
        
            vehicle.costs.all().delete()

            for cost in vehicle_cost_data:
                vehicle_cost_type = Vehicle_cost_type.objects.get(pk=cost["cost_type_id"])

                vehicle_cost = Vehicle_cost(vehicle=vehicle, 
                                            cost_type=vehicle_cost_type, 
                                            cost_name=cost["cost_name"], 
                                            expense_date=cost["expense_date"],
                                            value=cost["cost_value"])
                
                vehicle_cost.save()
        except ValueError:
            print(ValueError)
class VehicleDeleteView(VehicleBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)