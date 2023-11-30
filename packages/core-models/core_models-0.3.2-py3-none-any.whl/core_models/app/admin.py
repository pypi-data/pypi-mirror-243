from django.contrib import admin
from django import forms
from django.contrib.admin import SimpleListFilter
from safedelete import HARD_DELETE

from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .. import constants


class CustomActionForm(forms.Form):
    action = forms.CharField(
        widget=forms.HiddenInput, initial='delete_selected',
        label='Delete Selected'
    )
    select_across = forms.BooleanField(
        label='', required=False, initial=0,
        widget=forms.HiddenInput({'class': 'select-across'}),
    )
    fake_label = forms.CharField(
        widget=forms.TextInput({
            'readonly': True, 'placeholder': 'Delete Selected'
        }),
        label='Delete Selected',
        required=False
    )


class CompanyInline(admin.StackedInline):
    model = Company
    can_delete = False
    fk_name = 'user'


class UserConfigInline(admin.StackedInline):
    model = UserConfiguration
    can_delete = False
    fk_name = 'user'


class BankAccountInline(admin.TabularInline):
    model = BankAccount
    can_delete = False
    fk_name = 'created_by'
    extra = 0


class UserAdmin(BaseUserAdmin):
    action_form = CustomActionForm
    inlines = (CompanyInline, BankAccountInline, UserConfigInline)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "job_role", "phone_number", "onboarding_stage", "is_onboarding_complete", "notification_tokens")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_type",
                    "email_verified"
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "phone_number", "job_role", "user_type", "is_staff", "is_superuser")
    list_filter = ("user_type", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone_number")
    ordering = ("email", "first_name", "last_name", "phone_number", "created_at")

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.delete(force_policy=HARD_DELETE)

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.delete(force_policy=HARD_DELETE)

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.save()
            UserConfiguration.objects.create(user=obj)
        else:
            obj.save()


class CompanyDocumentInline(admin.TabularInline):
    model = CompanyDocument
    can_delete = False
    fk_name = 'company'
    extra = 0


class CompanyIncorporationInline(admin.StackedInline):
    model = CompanyIncorporation
    can_delete = False
    fk_name = 'company'
    extra = 0


class CommercialInformationInline(admin.StackedInline):
    model = CommercialInformation
    can_delete = False
    fk_name = 'company'
    extra = 0


class VertoConfigInline(admin.StackedInline):
    model = VertoConfig
    can_delete = False
    fk_name = 'company'
    extra = 0


class WalletInline(admin.TabularInline):
    model = Wallet
    can_delete = False
    fk_name = 'company'
    extra = 0


class CompanyProfileTypeFilter(SimpleListFilter):
    title = "Company Type"
    parameter_name = "company_type"

    def lookups(self, request, model_admin):
        return [
            ("S", "Seller"),
            ("F", "Financier"),
            ("B", "Buyer"),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__user_type=self.value())
        return queryset


class CompanyAdmin(admin.ModelAdmin):
    action_form = CustomActionForm
    inlines = (CompanyDocumentInline, CompanyIncorporationInline,
               CommercialInformationInline, VertoConfigInline, WalletInline)
    list_display = (
        "user", "name", 'company_type', "registration_number",
        "address_line1", "country", "is_verified",
        "date_verified", "created_at", "updated_at", "deleted"
    )
    list_filter = ("is_verified", "country", "deleted", CompanyProfileTypeFilter)
    search_fields = ("user", "name", "registration_number")
    ordering = ("name", "created_at", "date_verified")

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.delete(force_policy=HARD_DELETE)

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.delete(force_policy=HARD_DELETE)

    def company_type(self, obj):
        d = {
            "F": "Financier",
            "B": "Buyer",
            "S": "Seller",
            "A": "All"
        }
        return d.get(obj.user.user_type)

    company_type.short_description = "Company Type"
    company_type.admin_order_field = "company_type"
    company_type.boolean = False


class ContractDocumentItemInline(admin.TabularInline):
    model = ContractDocument
    can_delete = False
    fk_name = 'contract'
    extra = 0


class ContractStatusLogInline(admin.TabularInline):
    model = ContractStatusLog
    can_delete = False
    fk_name = 'contract'
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class ContractInformationInline(admin.StackedInline):
    model = ContractInformation
    can_delete = False
    fk_name = 'contract'
    extra = 0


class ContractAdmin(admin.ModelAdmin):
    action_form = CustomActionForm
    inlines = (ContractDocumentItemInline, ContractInformationInline, ContractStatusLogInline)
    list_display = (
        "reference", "seller", "buyer", "document",
        "status", "buyer_accepted_on", "buyer_accepted_via",
        "created_at", "updated_at", "deleted"
    )
    list_filter = ("status", )
    search_fields = ("reference", "seller", "buyer")
    ordering = ("reference", "created_at", "buyer_accepted_on")

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.delete(force_policy=HARD_DELETE)

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.delete(force_policy=HARD_DELETE)

    def save_model(self, request, obj, form, change):
        obj.save(request=request)


class BankAccountAdmin(admin.ModelAdmin):
    action_form = CustomActionForm
    list_display = (
        "created_by", "bank_name", "account_number", "sort_code",
        "created_at", "updated_at", "deleted"
    )
    search_fields = ("created_by", "account_number")
    ordering = ("bank_name", "created_at")

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.delete(force_policy=HARD_DELETE)

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.delete(force_policy=HARD_DELETE)


class CurrencyAdmin(admin.ModelAdmin):
    action_form = CustomActionForm
    list_display = (
        "created_by", "name", "code", "symbol", "created_at", "updated_at", "deleted"
    )
    search_fields = ("code", "name", "symbol")
    ordering = ("name", "created_at")

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super(CurrencyAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.delete(force_policy=HARD_DELETE)

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.delete(force_policy=HARD_DELETE)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    can_delete = False
    fk_name = 'invoice'
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    can_delete = False
    fk_name = 'invoice'
    extra = 0


class InvoiceTransactionInline(admin.TabularInline):
    model = InvoiceTransaction
    can_delete = False
    fk_name = 'invoice'
    extra = 0


class InvoiceAdmin(admin.ModelAdmin):
    action_form = CustomActionForm
    inlines = (InvoiceItemInline, PaymentInline, InvoiceTransactionInline)
    list_display = (
        "seller", "buyer", "financier", "currency", "reference",
        "invoice_number", "total", "interest_rate", "status", "invoice_date", "due_date",
        "created_at", "recurring", "deleted"
    )
    search_fields = ("reference", "invoice_number")
    ordering = ("reference", "total", "invoice_date", "due_date")
    list_filter = ("deleted", "recurring", "status")

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super(InvoiceAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.delete(force_policy=HARD_DELETE)

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.delete(force_policy=HARD_DELETE)


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "liquify_fee", "liquify_fee_type",
        "last_updated_by", "last_updated_on"
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        count = Configuration.objects.count()
        return count == 0

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        super(ConfigurationAdmin, self).save_model(request, obj, form, change)


# class CompanyIncorporationInline2(admin.StackedInline):
#     model = CompanyIncorporation
#     can_delete = False
#     fk_name = 'company_incorporation'
#     extra = 0


class ProfileApplicationAdmin(admin.ModelAdmin):
    action_form = CustomActionForm
    list_display = (
        "first_name", "last_name", "company_name", "email",
        "phone_number", "country", "sector",
        "oecd_buyers", "non_oecd_buyers",
        "annual_turnover", "company_incorporation",
        "status", "rejection_reason", "created_at"
    )
    list_filter = ('status', )
    # inlines = (CompanyIncorporationInline2, )

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset().exclude(
            status=constants.APPROVED_PROFILE_STATUS
        )
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super(ProfileApplicationAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.delete(force_policy=HARD_DELETE)

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.delete(force_policy=HARD_DELETE)


class PaymentAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    list_display = (
        "invoice", "payer", "expected_amount", "reference",
        "gateway_reference", "amount", "status", "created_at", "updated_at"
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super(PaymentAdmin, self).save_model(request, obj, form, change)


User_ = get_user_model()

admin.site.register(User_, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Notification)
admin.site.register(Sector)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(ProfileApplication, ProfileApplicationAdmin)
admin.site.register(Payment, PaymentAdmin)
