from baseTestCase import baseTestCase
from django.urls import reverse
from django.utils.safestring import SafeString
from django.utils.translation import gettext_lazy as _
from erp.models import Vehicle
from erp.views import DataTableMixin, VehicleListView

class DataTableMixinTestCase(baseTestCase):
    def test_get_data_table(self):
        mixin = DataTableMixin()
        with self.assertRaises(NotImplementedError):
            mixin.get_data_table()

class VehicleListViewTestCase(baseTestCase):
    def test_get_data_table(self):
        view = VehicleListView()
        data_table = view.get_data_table()

        # Assert the expected keys are present in the data_table dictionary
        self.assertIn('columns', data_table)
        self.assertIn('rows', data_table)
        self.assertIn('insertViewURL', data_table)

    def test_mount_edit_icon(self):
        view = VehicleListView()
        view_url = '/some-url/'
        icon_html = view.mountEditIcon(view_url)

        # Assert the return value is a SafeString object
        self.assertIsInstance(icon_html, SafeString)

        # Assert the HTML contains the expected elements
        self.assertIn('<a href="' + view_url + '">', str(icon_html))
        self.assertIn('class="fas fa-lg fa-edit"', str(icon_html))

    def test_get_data_table(self):
        self.maxDiff = None
        view = VehicleListView()

        expected_data_table = {
            'columns': [_('Vehicle'), _('Year'), _('Color'), _("Purchase price"), _("Sale price")],
            'rows': [
                {'values': [self.vehicle1.vehicle_variant, 
                            self.vehicle1.model_year, 
                            self.vehicle1.color, 
                            self.vehicle1.purchase_price_formatted, 
                            self.vehicle1.sale_value_formatted, 
                            view.mountEditIcon(reverse('vehicle_edit', kwargs={'pk': self.vehicle1.pk}))]},

                {'values': [self.vehicle2.vehicle_variant, 
                            self.vehicle2.model_year, 
                            self.vehicle2.color, 
                            self.vehicle2.purchase_price_formatted, 
                            self.vehicle2.sale_value_formatted, 
                            view.mountEditIcon(reverse('vehicle_edit', kwargs={'pk': self.vehicle2.pk}))]},
            ],
            'insertViewURL': reverse('vehicle_create'),
        }

        context = view.get_context_data()

        # Assert the context dictionary contains the expected values
        self.assertEqual(context['dataTable'], expected_data_table)

    def test_view_response(self):
        response = self.client.get(reverse('vehicle_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'datatable.html')


class VehicleListViewIntegrationTestCase(baseTestCase):
    def test_view_response(self):
        response = self.client.get(reverse('vehicle_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'datatable.html')

