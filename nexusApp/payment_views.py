"""
nexusApp/payment_views.py
─────────────────────────
Three views handle the entire Paystack payment cycle:

  1. checkout        — shows the plan summary + "Pay" button
  2. initiate_payment — calls Paystack API, redirects user to payment page
  3. payment_callback — Paystack returns here; we verify and save subscription
"""

import uuid
import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import PricingPlan, Subscription


# ─── Paystack base URL ────────────────────────────────────────────────────────
PAYSTACK_API = "https://api.paystack.co"


def _paystack_headers():
    """Authorization header used on every Paystack request."""
    return {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}", "Content-Type":  "application/json",}


# ─────────────────────────────────────────────────────────────────────────────
# VIEW 1 — Checkout
# URL: /pricing/checkout/<plan_id>/
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def checkout(request, plan_id):
    plan = get_object_or_404(PricingPlan, pk=plan_id)
    return render(request, "payment/checkout.html", {"plan": plan})


# ─────────────────────────────────────────────────────────────────────────────
# VIEW 2 — Initiate Payment
# URL: /pricing/initiate/<plan_id>/   (POST only)
# Calls Paystack's /transaction/initialize endpoint.
# Paystack returns an authorization_url — we redirect the user there.
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def initiate_payment(request, plan_id):

    if request.method != "POST":
        return redirect("checkout", plan_id=plan_id)
    
    plan = get_object_or_404(PricingPlan, pk=plan_id)

    reference = f"NEXUS-{uuid.uuid4().hex[:12].upper()}"

    # Paystack expects amount in KOBO (Naira × 100)
    amount_kobo = int(plan.price * 100)

    # The URL Paystack will redirect to after payment
    callback_url = request.build_absolute_uri("/pricing/callback/")

    payload = {
        "email":request.user.email, 
        "amount":amount_kobo, 
        "reference":reference, 
        "callback_url": callback_url,
        "metadata": {
            # Pass plan info through — available when we verify
            "plan_id":plan.pk, "plan_name": plan.name, "user_id":request.user.pk,
            },
    }

    try:
        response = requests.post(f"{PAYSTACK_API}/transaction/initialize", json=payload, headers=_paystack_headers(), timeout=10,)
        data = response.json()
    except requests.RequestException:
        messages.warning(request, "Could not connect to payment provider. Please try again.")
        return redirect("checkout", plan_id=plan_id)

    if not data.get("status"):
        messages.warning(request, "Payment initialisation failed. Please try again.")
        return redirect("checkout", plan_id=plan_id)

    # Store reference in session so callback can access it
    request.session["paystack_ref"]  = reference
    request.session["paystack_plan"] = plan.pk

    # Send user to Paystack's hosted payment page
    return redirect(data["data"]["authorization_url"])


# ─────────────────────────────────────────────────────────────────────────────
# VIEW 3 — Payment Callback
# URL: /pricing/callback/
# Paystack redirects here with ?reference=NEXUS-XXXX in the query string.
# We verify the transaction, then create/update the Subscription row.
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def payment_callback(request):
    reference = request.GET.get("reference") or request.session.get("paystack_ref")

    if not reference:
        messages.warning(request, "No payment reference found.")
        return redirect("pricing")

    # Verify the transaction with Paystack
    try:
        response = requests.get(f"{PAYSTACK_API}/transaction/verify/{reference}", headers=_paystack_headers(), timeout=10,)
        data = response.json()
    except requests.RequestException:
        messages.warning(request, "Could not verify payment. Contact support.")
        return redirect("pricing")

    if not data.get("status"):
        return redirect("payment_failed")

    tx = data["data"]
    status = tx.get("status")  # "success", "failed", "abandoned"

    if status != "success":
        # Save a failed subscription row so admin can see the attempt
        plan_id = request.session.get("paystack_plan")
        plan    = PricingPlan.objects.filter(pk=plan_id).first()
        Subscription.objects.update_or_create(
            user=request.user,
            defaults={"plan": plan, "status": Subscription.Status.FAILED, "paystack_ref": reference, "amount_paid":  0,},
        )
        return redirect("payment_failed")

    # ── Payment succeeded ─────────────────────────────────────────────────────
    plan_id = tx["metadata"].get("plan_id") or request.session.get("paystack_plan")
    plan    = PricingPlan.objects.filter(pk=plan_id).first()

    # Amount comes back in kobo — convert to Naira
    amount_naira = tx["amount"] / 100

    Subscription.objects.update_or_create(
        user=request.user,
        defaults={"plan": plan, "status": Subscription.Status.ACTIVE, "paystack_ref": reference, "amount_paid":  amount_naira,},)

    # Clear session keys
    request.session.pop("paystack_ref",  None)
    request.session.pop("paystack_plan", None)

    return redirect("payment_success")


# ─── Simple result pages ──────────────────────────────────────────────────────

@login_required
def payment_success(request):
    subscription = getattr(request.user, "subscription", None)
    return render(request, "payment/payment_success.html", {"subscription": subscription})


@login_required
def payment_failed(request):
    return render(request, "payment/payment_failed.html")
