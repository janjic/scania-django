from django import forms
from django.contrib import admin
from django.db import models as django
from django.shortcuts import redirect
from django.utils.text import Truncator
from django.utils.html import mark_safe, format_html
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from . import models

admin.site.site_url = None
# class CountryTabularInline(admin.TabularInline):
#     fields = ('code', 'name', )
#     model = models.Country
#
#     class CountryInlineFormset(forms.models.BaseInlineFormSet):
#         def clean(self):
#             super(CountryTabularInline.CountryInlineFormset, self).clean()
#             if not hasattr(self, 'cleaned_data'):
#                 return
#
#             for form_data in self.cleaned_data:
#                 code = form_data.get('code', None)
#                 if code and len(code) < 2:
#                     raise forms.ValidationError('One of the countries code is invalid')
#                 return self.cleaned_data
#
#     formset = CountryInlineFormset
#
#     def has_add_permission(self, request):
#         return False
#
#
# class CityStackedInline(admin.TabularInline):
#     model = models.City
#     readonly_fields = ('wiki', )
#
#     wiki_link_template = "<a href='https://en.wikipedia.org/wiki/{}' target='_blank'>" \
#                          " <i style='padding-left:20px;margin-top:15px' class='material-icons left'>search</i>" \
#                          "</a>"
#
#     def wiki(self, city):
#         if city.id:
#             return mark_safe(self.wiki_link_template.format(city.name))
#         return ""
#     wiki.short_description = _('wiki')
#
#
# class SeaStackedInline(admin.StackedInline):
#     extra = 0
#     fields = ('name', 'area', 'avg_depth', 'max_depth')
#     model = models.Sea
#     readonly_fields = ('avg_depth', 'max_depth')
#
#     class SeaInlineFormset(forms.models.BaseInlineFormSet):
#         def clean(self):
#             super(SeaStackedInline.SeaInlineFormset, self).clean()
#             if not hasattr(self, 'cleaned_data'):
#                 return
#
#             for form_data in self.cleaned_data:
#                 name = form_data['name']
#                 if len(name) < 2:
#                     raise forms.ValidationError('One of the seas name is too short')
#                 return self.cleaned_data
#
#     formset = SeaInlineFormset
#
#
# class ContinentTabularInline(admin.TabularInline):
#     model = models.Continent.oceans.through
#     extra = 1
#
#
# @admin.register(models.Ocean)
# class OceanAdmin(admin.ModelAdmin):
#     icon = '<i class="fa fa-tint"></i>'
#     actions = None
#     exclude = ('area', )
#     readonly_fields = ('map', )
#     inlines = [ContinentTabularInline, SeaStackedInline]
#     list_display = ('name', 'area', 'short_description', 'map',)
#     prepopulated_fields = {'slug': ('name', )}
#
#     def map(self, ocean):
#         if ocean.map_url:
#             return format_html('<div class="col s12 center-align"><img src="{}" width="200" /></div>', ocean.map_url)
#         return ""
#     map.short_description = _('map')
#
#     def short_description(self, ocean):
#         return Truncator(ocean.description).words(100, truncate=' ...')
#     short_description.short_description = _('short description')
#
#     def has_add_permission(self, request):
#         return True
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#
# @admin.register(models.Sea)
# class SeaAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">bubble_chart</i>'
#     fields = (('name', 'parent'),
#               'ocean',
#               ('area', 'avg_depth', 'max_depth'),
#               'basin_countries')
#     filter_horizontal = ('basin_countries', )
#     list_display = ('name', 'parent', 'ocean', 'sea_area', )
#     list_filter = ('parent', 'ocean', )
#
#     def sea_area(self, sea):
#         return None if sea.area == 0 else sea.area
#     sea_area.short_description = _('sea area')
#     sea_area.empty_value_display = '?'
#
#
# @admin.register(models.Continent)
# class ContinentAdmin(admin.ModelAdmin):
#     icon = '<i class="fa fa-globe"></i>'
#     actions_selection_counter = False
#     fieldsets = (
#         (None, {
#             'fields': ('name',)}),
#         (_('Details'), {
#             'fields': ('area', ('oceans', 'hemisphere'),
#                        ('population', 'population_density'))}),
#         (_('Fun facts'), {
#             'fields': ('largest_country', 'biggest_mountain',
#                        ('biggest_city', 'longest_river', ))})
#     )
#     inlines = [CountryTabularInline]
#     list_display = (
#         'name', 'surrounded_oceans', 'countries_count',
#         'area', 'population', )
#     list_filter = ('oceans', )
#     ordering = ['population']
#     raw_id_fields = ('oceans', )
#     readonly_fields = ('biggest_city', 'longest_river', )
#
#     def surrounded_oceans(self, contintent):
#         return ', '.join(ocean.name for ocean in contintent.oceans.all())
#     surrounded_oceans.short_description = _('surrounded oceans')
#
#     def countries_count(self, contintent):
#         return contintent.countries.count()
#     countries_count.short_description = _('countries count')
#
#
# class CountryForm(forms.ModelForm):
#     class Meta:
#         model = models.Country
#         fields = '__all__'
#
#     def clean(self):
#         cleaned_data = super(CountryForm, self).clean()
#         code = cleaned_data.get('code')
#         if code and len(code) < 2:
#             raise forms.ValidationError('The country code is invalid')
#         return self.cleaned_data
#
#
# @admin.register(models.Country)
# class CountryAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">flag</i>'
#     date_hierarchy = 'independence_day'
#     form = CountryForm
#     inlines = [CityStackedInline]
#     list_display = (
#         'tld', 'name', 'continent',
#         'became_independent_in_20_century',
#         'gay_friendly')
#     list_display_links = ('tld', 'name', )
#     list_filter = ('continent', )
#     list_per_page = 50
#     list_select_related = ('continent', )
#     search_fields = ('code', 'name', )
#
#     def tld(self, country):
#         return '.' + country.code.lower()
#     tld.short_description = 'TLD'
#     tld.admin_order_field = 'code'
#
#     def became_independent_in_20_century(self, country):
#         if country.independence_day:
#             return 1900 <= country.independence_day.year <= 2000
#     became_independent_in_20_century.short_description = _('became independent in XX century')
#     became_independent_in_20_century.boolean = True
#
#
# @admin.register(models.City)
# class CityAdmin(admin.ModelAdmin):
#     icon = '<i class="fa fa-building"></i>'
#     list_display = ('name', 'country', 'population')
#     list_filter = ('is_capital', 'country', (
#         'country__continent', admin.RelatedOnlyFieldListFilter))
#     search_fields = ('name', )
#     formfield_overrides = {
#         django.IntegerField: {
#             'widget': forms.NumberInput(attrs={'min': 0})},
#     }
#     show_full_result_count = False
#     raw_id_fields = ('country', )
#     readonly_fields = ('became_independent_in_20_century', )
#
#     def became_independent_in_20_century(self, city):
#         if city.country_id is not None and city.country.independence_day:
#             return 1900 <= city.country.independence_day.year <= 2000
#     became_independent_in_20_century.short_description = _('became independent in XX century')
#     became_independent_in_20_century.boolean = True


class CustomerResource(resources.ModelResource):

    class Meta:
        model = models.Customer
        fields = ('id', 'nav_cust_name', 'nav_cust_search_name', 'mds_cust_id', 'nav_vat', 'source')
        export_order = ('id', 'nav_cust_name', 'nav_cust_search_name', 'mds_cust_id', 'nav_vat', 'source')

@admin.register(models.Customer)
class CustomerAdmin(ImportExportModelAdmin):
    icon = '<i class="material-icons">account_balance</i>'
    search_fields = ('id', 'nav_cust_search_name', 'mds_cust_id', 'nav_vat', 'source')
    list_display = ('id', 'nav_cust_search_name', 'mds_cust_id', 'nav_vat', 'source')
    list_filter = ('source',)
    ordering = ['-nav_cust_search_name']
    resource_class = CustomerResource

    #
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     """Limit choices for 'picture' field to only your pictures."""
    #     if db_field.name == 'picture':
    #         if not request.user.is_superuser:
    #             kwargs["queryset"] = Picture.objects.filter(
    #                 owner=request.user)
    #     return super(CustomerAdmin, self).formfield_for_foreignkey(
    #         db_field, request, **kwargs)


class PreCalculationStackedInline(admin.StackedInline):
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('chassis_no_trade_in', 'other')}),
        (_('PDI/R'), {
            'fields': ('pdi', 'r_servis',)}),
        (_('Discounts'), {
            'fields': ('discount_1', 'discount_2',)}),
        (_('Details'), {
            'fields': ('extra_support', 'painting', 'air_condition', 'warranty', 'trade_in',
                       'jacket_and_presents', 'radio', 'tachograph', 'adaptation_rup', 'estimated_tender_costs',
                       'driver_training', 'sales_price', )}),
        (_('Results'), {
            'fields': ('dealer_purchase_price', 'total_cost', 'dealer_net_purchace_price_cost',
                       'price_gain_loss', 'dealer_final_margin',)})
    )
    readonly_fields = ('dealer_purchase_price', 'total_cost', 'dealer_net_purchace_price_cost',
                       'price_gain_loss', 'dealer_final_margin',)
    model = models.PreCalculation

@admin.register(models.Calculation)
class CalculationAdmin(admin.ModelAdmin):
    icon = '<i class="fa fa-building"></i>'
    readonly_fields = ('salesman', 'id')
    list_display = ('order_no', 'ch_type', 'delivery_place', 'dealer', 'customer')
    search_fields = ('id', 'order_no', 'salesman', 'customer', 'salesman2', 'order_stock')
    list_filter = ('dealer', 'salesman2', 'order_stock',)
    fieldsets = (
        (None, {
            'fields': ('id', 'order_no',  'sport_distribution_order_id', 'email', 'ch_type', 'delivery_place',)}),
        (_('Numeric'), {
            'fields': ('order_security', 'quantity', )}),
        (_('Details'), {
            'fields': ('dealer', 'financing', 'application', 'order_stock', 'customer', 'salesman2', 'salesman')}),
        (_('Dates'), {
            'fields': ('bodybuilder_crd', 'agreed_delivery_date', 'date', )}),

    )

    inlines = ()

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/polls/calculation/' + str(obj.id) + '/change/#/tab/inline_0/')

    def response_change(self, request, obj):
        return redirect('/admin/polls/calculation/' + str(obj.id) + '/change/#/tab/inline_0/')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = (PreCalculationStackedInline,)
        return super(CalculationAdmin, self).change_view(request, object_id)

    def save_model(self, request, obj, form, change):
        is_new = False
        if getattr(obj, 'salesman', None) is None:
            obj.salesman = request.user
            is_new = True
        obj.save()
        if is_new:
            pre_calculation = models.PreCalculation()
            pre_calculation.calculation = obj
        else:
            pre_calculation = models.PreCalculation.objects.get(calculation=obj)
            pre_calculation.dealer_purchase_price = pre_calculation.dealer_purchase_price - pre_calculation.discount_1 - pre_calculation.discount_2 - pre_calculation.extra_support
            pre_calculation.total_cost = pre_calculation.pdi + pre_calculation.r_servis + pre_calculation.painting + pre_calculation.air_condition + pre_calculation.warranty + pre_calculation.trade_in + pre_calculation.jacket_and_presents + pre_calculation.radio + pre_calculation.tachograph + pre_calculation.adaptation_rup + pre_calculation.estimated_tender_costs + pre_calculation.driver_training
            pre_calculation.dealer_net_purchace_price_cost = pre_calculation.total_cost + pre_calculation.dealer_purchase_price
            pre_calculation.price_gain_loss = pre_calculation.sales_price - pre_calculation.dealer_net_purchace_price_cost
            try:
                pre_calculation.dealer_final_margin = (
                                                                  pre_calculation.price_gain_loss / pre_calculation.sales_price) * 100
            except ZeroDivisionError:
                pass
            if getattr(pre_calculation, 'salesman', None) is None:
                pre_calculation.salesman = request.user

        pre_calculation.save()

    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(CalculationAdmin, self).get_queryset(request)
        if request.user.groups.filter(name='ADMIN_SUPER').exists():
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(salesman=request.user)

    # def has_delete_permission(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return True
    #     elif getattr(obj, 'salesman', None) is not None and getattr(obj, 'salesman', None).id == request.user.id
    #         return True
    #     else:
    #         return False


@admin.register(models.PreCalculation)
class PreCalculationAdmin(admin.ModelAdmin):
    icon = '<i class="fa fa-building"></i>'
    list_display = ('id', 'dealer_purchase_price', 'total_cost', 'dealer_net_purchace_price_cost',
                       'price_gain_loss', 'dealer_final_margin',)
    fieldsets = (
        (None, {
            'fields': ('chassis_no_trade_in', 'other', 'calculation')}),
        (_('PDI/R'), {
            'fields': ('pdi', 'r_servis',)}),
        (_('Discounts'), {
            'fields': ('discount_1', 'discount_2',)}),
        (_('Details'), {
            'fields': ('extra_support', 'painting', 'air_condition', 'warranty', 'trade_in',
                       'jacket_and_presents', 'radio', 'tachograph', 'adaptation_rup', 'estimated_tender_costs',
                       'driver_training', 'sales_price',)}),
        (_('Results'), {
            'fields': ('dealer_purchase_price', 'total_cost', 'dealer_net_purchace_price_cost',
                       'price_gain_loss', 'dealer_final_margin',)})
    )
    readonly_fields = ('dealer_purchase_price', 'total_cost', 'dealer_net_purchace_price_cost',
                       'price_gain_loss', 'dealer_final_margin', 'calculation')

    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(PreCalculationAdmin, self).get_queryset(request)
        if request.user.groups.filter(name='ADMIN_SUPER').exists():
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(salesman=request.user)

    def save_model(self, request, obj, form, change):
            obj.dealer_purchase_price = obj.dil_purchase_price_sport - obj.discount_1 - obj.discount_2 - obj.extra_support
            obj.total_cost = obj.pdi + obj.r_servis + obj.painting + obj.air_condition + obj.warranty + obj.trade_in + obj.jacket_and_presents + obj.radio + obj.tachograph + obj.adaptation_rup + obj.estimated_tender_costs + obj.driver_training
            obj.dealer_net_purchace_price_cost = obj.total_cost + obj.dealer_purchase_price
            obj.price_gain_loss = obj.sales_price - obj.dealer_net_purchace_price_cost
            try:
                obj.dealer_final_margin = (obj.price_gain_loss / obj.sales_price) * 100
            except ZeroDivisionError:
                pass
            if getattr(obj, 'salesman', None) is None:
                obj.salesman = request.user

            obj.save()

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/polls/precalculation/' + str(obj.id) + '/change/#/tab/module_4/')

    def response_change(self, request, obj):
        return redirect('/admin/polls/precalculation/' + str(obj.id) + '/change/#/tab/module_4/')
