# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
#
# from apps.payment.models.models import Orders
# from apps.payment.services.services import PlanService
# from apps.shared.utils.logger import logger
#
#
# @receiver(m2m_changed, sender=Orders.types.through)
# def order_types_changed(sender, instance, action, **kwargs):
#     """Order types changed signal"""
#     if action == "post_add":
#         plan = PlanService().get_plan()
#         instance.price = plan.price * instance.types.all().count()
#         instance.end_date = plan.quarter.end_date
#         instance.save(update_fields=["price", "end_date"])
#         logger.info(f"Order {instance.id} types changed")
