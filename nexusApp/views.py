from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Testimonial, PricingPlan, FAQ, TeamMember
from .forms import ContactForm, SignUpForm, EmailLoginForm
from django.contrib import messages, auth
from django.core.cache import cache
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required


# ─── Home ──────────────────────────────────────────────────────────────────────

def home(request):
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    return render(request, "home.html", {"testimonials": testimonials, "active_page":  "home",})


# ─── Pricing ───────────────────────────────────────────────────────────────────

@login_required
def pricing(request):
    """prefetch_related avoids N+1 — one extra query fetches all features."""
    plans = PricingPlan.objects.prefetch_related("features").all()
    faqs  = FAQ.objects.filter(is_active=True)

    user_subscription = None
    if request.user.is_authenticated:
        user_subscription = getattr(request.user, "subscription", None)

        if user_subscription and not user_subscription.is_active:
            user_subscription = None

    return render(request, "pricing.html", {"plans": plans, "faqs": faqs, "active_page": "pricing", "user_subscription": user_subscription,})
# ─── About ─────────────────────────────────────────────────────────────────────

def about(request):
    team = TeamMember.objects.filter(is_active=True)
    return render(request, "about.html", {"team": team, "active_page": "about", })


# ─── Contact ───────────────────────────────────────────────────────────────────

RATE_LIMIT  = 3
RATE_WINDOW = 60 * 60   # 1 hour


def _get_client_ip(request):
    """Returns the real client IP, respecting proxy headers."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _is_rate_limited(ip):
    """
    Returns True if the IP has exceeded RATE_LIMIT submissions
    within RATE_WINDOW seconds. Uses Django cache as counter store.
    """
    cache_key = f"contact_rate_{ip}"
    count = cache.get(cache_key, 0)

    if count >= RATE_LIMIT:
        return True

    if count == 0:
        cache.set(cache_key, 1, timeout=RATE_WINDOW)
    else:
        cache.incr(cache_key)

    return False


def contact(request):
    if request.method == "POST":
        ip   = _get_client_ip(request)
        form = ContactForm(request.POST)

        if _is_rate_limited(ip):
            messages.warning(request, "You've sent too many messages. Please wait an hour before trying again.",)
            return render(request, "contact.html", { "form": form, "active_page": "contact", })

        if form.is_valid():
            form.save()
            messages.success(request,"Message received! We'll be in touch within 1–2 business days.",)
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form, "active_page": "contact",})


# ─── Sign-up ───────────────────────────────────────────────────────────────────

def signup(request):
    """
    Registers a new user with username, email, and password.
    On success the user is logged in automatically and redirected home.
    """
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the backend so Django doesn't have to guess when multiple
            login(request, user, backend="nexusApp.backends.EmailBackend")
            messages.info(request, f"Welcome to Nexus, {user.username}!")
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


# ─── Login ─────────────────────────────────────────────────────────────────────

def login_view(request):
    """
    Email + password login.
    Authentication is delegated to EmailBackend via EmailLoginForm.
    """
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            user     = form.get_user()
            next_url = request.GET.get("next") or "home"
            login(request, user)
            return redirect(next_url)
    else:
        form = EmailLoginForm()

    return render(request, "registration/login.html", {"form": form})


# ─── Logout ────────────────────────────────────────────────────────────────────

def logout(request):
    auth_logout(request)
    return redirect("home")


# ─── Legal ─────────────────────────────────────────────────────────────────────

def legal_page(request):
    return render(request, "legal.html")
