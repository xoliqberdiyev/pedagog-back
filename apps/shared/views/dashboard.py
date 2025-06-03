# import json
#
# from django.contrib.admin import site
# from django.contrib.auth.decorators import login_required
# from django.core.cache import cache
# from django.db.models import Count, Q, Sum
# from django.shortcuts import render
# from django.utils.decorators import method_decorator
# from django.utils.translation import gettext_lazy as _
# from django.views import View
#
# from apps.payment.models.models import Orders
# from apps.pedagog.models.feedback import Feedback
# from apps.pedagog.models.plan import Plan
# from apps.users.models.locations import Region
# from apps.users.models.user import User
#
#
# @method_decorator(login_required(login_url="/admin/"), name="dispatch")
# class DashboardView(View):
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.users = User.objects
#         self.feedback = Feedback.objects
#         self.plan = Plan.objects
#         self.orders = Orders.objects
#
#     def get_cards(self):
#         # Check cache first
#         cards = cache.get("dashboard_cards")
#         if not cards:
#             cards = [
#                 {
#                     "title": _("Foydalanuvchilar"),
#                     "value": self.users.all().count(),
#                 },
#                 {
#                     "title": _("Moderatorlar"),
#                     "value": self.users.filter(role="moderator").count(),
#                 },
#                 {
#                     "title": _("Ustozlar"),
#                     "value": self.users.filter(role="user").count(),
#                 },
#                 {
#                     "title": _("Kalendar tematik rejalar"),
#                     "value": self.plan.all().count(),
#                 },
#                 {
#                     "title": _("Barcha sharhlar"),
#                     "value": self.feedback.all().count(),
#                 },
#                 {
#                     "title": _("Javob berilgan sharhlar"),
#                     "value": self.feedback.filter(answered=True).count(),
#                 },
#                 {
#                     "title": _("Javob berilmagan sharhlar"),
#                     "value": self.feedback.filter(answered=False).count(),
#                 },
#                 {
#                     "title": _("Umumiy buyurtmalar"),
#                     "value": self.orders.all().count(),
#                 },
#                 {
#                     "title": _("Muvaffaqiyatli buyurtmalar"),
#                     "value": self.orders.filter(status=True).count(),
#                 },
#                 {
#                     "title": _("Muvaffaqiyatsiz buyurtmalar"),
#                     "value": self.orders.filter(status=False).count(),
#                 },
#             ]
#             # Cache the result for 5 minutes
#             cache.set("dashboard_cards", cards, 300)
#         return cards
#
#     def get_total_orders_price(self):
#         orders = cache.get("orders")
#         if not orders:
#             orders = [
#                 {
#                     "title": _("Umumiy buyurtmalar narxi"),
#                     "value": self.orders.aggregate(total=Sum("price"))["total"] or 0,
#                 },
#                 {
#                     "title": _("Muvaffaqiyatli buyurtmalar narxi"),
#                     "value": self.orders.filter(status=True).aggregate(
#                         total=Sum("price")
#                     )["total"]
#                     or 0,
#                 },
#                 {
#                     "title": _("Muvaffaqiyatsiz buyurtmalar narxi"),
#                     "value": self.orders.filter(status=False).aggregate(
#                         total=Sum("price")
#                     )["total"]
#                     or 0,
#                 },
#             ]
#             cache.set("orders", orders, 300)
#         return orders
#
#     def get(self, request):
#         context = dict(site.each_context(request))
#
#         # Add cards to context
#         context.update({"cards": self.get_cards()})
#         context.update({"orders": self.get_total_orders_price()})
#
#         # Fetch and process region user counts
#         # Check cache first
#         region_user_counts = cache.get("region_user_counts")
#         if not region_user_counts:
#             regions = Region.objects.all()
#             region_user_counts = User.objects.values("region_id").annotate(
#                 user_count=Count("id", filter=Q(role="user")),
#                 moderator_count=Count("id", filter=Q(role="moderator")),
#             )
#             region_user_counts_dict = {
#                 item["region_id"]: {
#                     "user_count": item["user_count"],
#                     "moderator_count": item["moderator_count"],
#                 }
#                 for item in region_user_counts
#             }
#             region_user_counts = [
#                 {
#                     "region_region": region.region,
#                     "user_count": region_user_counts_dict.get(region.id, {}).get(
#                         "user_count", 0
#                     ),
#                     "moderator_count": region_user_counts_dict.get(region.id, {}).get(
#                         "moderator_count", 0
#                     ),
#                 }
#                 for region in regions
#             ]
#             # Cache the result for 5 minutes
#             cache.set("region_user_counts", region_user_counts, 300)
#
#         labels = [region["region_region"] for region in region_user_counts]
#         user_data = [region["user_count"] for region in region_user_counts]
#         moderator_data = [region["moderator_count"] for region in region_user_counts]
#
#         # Update context with region user counts and moderator counts
#         context.update(
#             {
#                 "region_user_counts": region_user_counts,
#                 "labels": json.dumps(labels),
#                 "user_data": json.dumps(user_data),
#                 "moderator_data": json.dumps(moderator_data),
#             }
#         )
#
#         return render(request, "admin/dashboard.html", context)
