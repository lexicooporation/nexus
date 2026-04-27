from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField 

 
# Create your models here.
 
# ─── Testimonial ───────────────────────────────────────────────────────────────────

class Testimonial(models.Model):
    """
    use to create reviews which are displayed on the home page.
    """
    author_name = models.CharField(max_length=150)
    author_role = models.CharField(max_length=200) 
    quote       = models.TextField(max_length=200)
    rating      = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)],)
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        ordering = ["order"]
 
    def __str__(self):
        return f"{self.author_name} — {self.quote[:60]}"
 
    @property
    def stars(self):
        """
        Used in my template for: {% for _ in t.stars %}★{% endfor %}
        Returns a range object matching the rating value.
        """
        return range(self.rating)

# ─── PRICING PLAN ───────────────────────────────────────────────────────────────────

class PricingPlan(models.Model):
    """
    One row per pricing tier (e.g. Starter, Growth, Scale).
    Features are stored as child PlanFeature rows so you can add/remove
    them per plan from the Admin inline without touching the plan itself.
    """
    name           = models.CharField(max_length=100)
    price          = models.DecimalField(max_digits=8, decimal_places=2)
    billing_period = models.CharField(max_length=20, default="month")
    tagline        = models.CharField(max_length=200, help_text="Short line under the price, e.g. 'For startups and growing businesses'",)
    is_featured    = models.BooleanField(default=False, help_text="Marks this plan with a 'Most Popular' badge in the template.",)
    cta_label      = models.CharField(max_length=80, default="Get Started")
    order          = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        ordering = ["order"]
 
    def __str__(self):
        return f"{self.name} — ${self.price}/{self.billing_period}"



# ─── PLAN FEATURE ───────────────────────────────────────────────────────────────
 
class PlanFeature(models.Model):
    """
    Uses the pricingplan model as foreignkey 
    so kind of a subclass of the actual pricingplan
    """
    plan  = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, related_name="features",)
    label = models.CharField(max_length=150)
    order = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        ordering = ["order"]
 
    def __str__(self):
        return f"{self.plan.name} › {self.label}"



# ─── FAQ ───────────────────────────────────────────────────────────────────
 
class FAQ(models.Model):
    """
    model that loads the frequently asked questions on the pricing page
    """
    question  = models.CharField(max_length=300)
    answer    = models.TextField()
    is_active = models.BooleanField(default=True)
    order     = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        ordering            = ["order"]
        verbose_name        = "FAQ"
        verbose_name_plural = "FAQs"
 
    def __str__(self):
        return self.question
    
# ─── About ───────────────────────────────────────────────────────────────────
 
class TeamMember(models.Model):
    """
    One card in the team grid on the About page.
    Upload photos via Django Admin — if no photo is set the template
    falls back to the 👤 emoji placeholder.
    """
    name      = models.CharField(max_length=150)
    role      = models.CharField(max_length=150)
    photo     = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order     = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        ordering = ["order"]
 
    def __str__(self):
        return f"{self.name} — {self.role}"

# ─── Contact ───────────────────────────────────────────────────────────────────

class ContactMessage(models.Model):
    """Stores every submission from the Contact page."""

    class Status(models.TextChoices):
        NEW     = "new",     "New"
        READ    = "read",    "Read"
        REPLIED = "replied", "Replied"

    full_name  = models.CharField(max_length=200)
    email      = models.EmailField(max_length=254)
    message    = models.TextField(max_length=2000)
    status     = models.CharField(max_length=10,choices=Status.choices,default=Status.NEW,)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering            = ["-created_at"]
        verbose_name        = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.full_name} <{self.email}> — {self.created_at:%Y-%m-%d}"
    


# ─── Subscription ──────────────────────────────────────────────────────────────

class Subscription(models.Model):
    """
    Records a user's active plan after a successful Paystack payment.
    One subscription per user (OneToOne) — upgrading overwrites the existing row.
    """

    class Status(models.TextChoices):
        ACTIVE   = "active",   "Active"
        INACTIVE = "inactive", "Inactive"
        FAILED   = "failed",   "Failed"

    user              = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    plan              = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True, related_name="subscriptions")
    status            = models.CharField(max_length=10, choices=Status.choices, default=Status.INACTIVE)
    # Paystack fields — stored so you can reconcile payments later
    paystack_ref      = models.CharField(max_length=100, unique=True, help_text="Paystack transaction reference")
    amount_paid       = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in Naira")

    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering            = ["-created_at"]
        verbose_name        = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.user.email} → {self.plan} [{self.status}]"

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE
