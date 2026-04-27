from django.contrib import admin
from .models import Testimonial, PricingPlan, PlanFeature, FAQ, TeamMember, ContactMessage,Subscription


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ("author_name", "author_role", "rating", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter   = ("is_active",)
    search_fields = ("author_name", "quote")


class PlanFeatureInline(admin.TabularInline):
    model  = PlanFeature
    extra  = 1
    fields = ("label", "order")


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display  = ("name", "price", "billing_period", "is_featured", "order")
    list_editable = ("is_featured", "order")
    inlines       = [PlanFeatureInline]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display  = ("question", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display  = ("name", "role", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display    = ("full_name", "email", "status", "created_at")
    list_filter     = ("status",)
    list_editable   = ("status",)
    readonly_fields = ("full_name", "email", "message", "ip_address", "created_at")
    date_hierarchy  = "created_at"

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display  = ("user", "plan", "status", "paystack_ref", "amount_paid")
    search_fields = ("user", "status", "paystack_ref")
    readonly_fields = ("user", "plan", "paystack_ref", "amount_paid")

 