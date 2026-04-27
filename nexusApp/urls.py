from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, payment_views


# ─── Password-reset view kwargs ───────────────────────────────────────────────
_PR_KWARGS = dict(
    template_name = "registration/password_reset_form.html",
    email_template_name = "registration/password_reset_email.html",
    subject_template_name = "registration/password_reset_subject.txt",
    extra_email_context = {"site_name": "Nexus"},
)

urlpatterns = [
    # ── Main pages ────────────────────────────────────────────────────────────
    path("",views.home,name="home"),
    path("pricing/",views.pricing,name="pricing"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),

    # ── Auth ──────────────────────────────────────────────────────────────────
    path("accounts/login/",views.login_view,name="login"),
    path("accounts/signup/",views.signup,name="signup"),
    path("accounts/logout/",views.logout,name="logout"),

    # ── Password reset (Django built-ins + custom templates) ──────────────────
    path("accounts/password-reset/", auth_views.PasswordResetView.as_view(**_PR_KWARGS),name="password_reset",),
    path("accounts/password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html",),name="password_reset_done",),
    path("accounts/password-reset/confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html",),name="password_reset_confirm",),
    path("accounts/password-reset/complete/",auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html",),name="password_reset_complete",),

    # ── Legal ─────────────────────────────────────────────────────────────────
    path("legal/",          views.legal_page, name="legal"),
    path("legal/privacy/",  views.legal_page, name="privacy"),
    path("legal/terms/",    views.legal_page, name="terms"),

     # ── Payment routes ────────────────────────────────────────────────────────
    path("pricing/checkout/<int:plan_id>/", payment_views.checkout,         name="checkout"),
    path("pricing/initiate/<int:plan_id>/", payment_views.initiate_payment,  name="initiate_payment"),
    path("pricing/callback/",               payment_views.payment_callback,   name="payment_callback"),
    path("pricing/success/",               payment_views.payment_success,    name="payment_success"),
    path("pricing/failed/",                payment_views.payment_failed,     name="payment_failed"),
]
