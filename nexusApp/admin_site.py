"""
Custom AdminSite that injects dashboard context into the index view.

HOW THE REGISTRY WORKS
───────────────────────
admin.py keeps using @admin.register() (the default admin.site).
NexusAdminSite overrides _registry as a property so it always reads
from admin.site._registry — the two sites share one registry automatically,
with no circular-import risk and no duplicate registrations.
"""
from django.contrib.admin import AdminSite
from django.contrib import admin as _default_admin


class NexusAdminSite(AdminSite):
    site_header = "Nexus"
    site_title  = "Nexus Admin"
    index_title = "Dashboard"

    # ------------------------------------------------------------------ #
    #  Share admin.site's registry — no @nexus_admin.register() needed   #
    # ------------------------------------------------------------------ #
    @property
    def _registry(self):
        return _default_admin.site._registry

    @_registry.setter
    def _registry(self, value):
        # Django's AdminSite.__init__ does self._registry = {}
        # We intercept that write and ignore it so our property stays in place.
        pass

    # ------------------------------------------------------------------ #
    #  Inject dashboard stats into the index template context             #
    # ------------------------------------------------------------------ #
    def index(self, request, extra_context=None):
        # Late import — models aren't safe to import at module load time
        from nexusApp.models import (ContactMessage, Testimonial, PricingPlan, PlanFeature, FAQ, TeamMember,)

        stats = {
            # Contact messages
            "total_messages":  ContactMessage.objects.count(),
            "unread_messages": ContactMessage.objects.filter(status=ContactMessage.Status.NEW).count(),
            "recent_messages": ContactMessage.objects.order_by("-created_at")[:5],
            # Testimonials
            "total_testimonials":  Testimonial.objects.count(),
            "active_testimonials": Testimonial.objects.filter(is_active=True).count(),
            # Pricing
            "total_plans":    PricingPlan.objects.count(),
            "total_features": PlanFeature.objects.count(),
            # FAQs
            "total_faqs":  FAQ.objects.count(),
            "active_faqs": FAQ.objects.filter(is_active=True).count(),
            # Team
            "team_members": TeamMember.objects.filter(is_active=True).order_by("order"),
        }

        extra_context = {**(extra_context or {}), **stats}
        return super().index(request, extra_context)


# Singleton instance — import this in urls.py only
nexus_admin = NexusAdminSite(name="nexus_admin")