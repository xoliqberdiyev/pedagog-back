# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from apps.pedagog.models.plan import Plan
# from apps.pedagog.models.schedule import ScheduleChoices, Schedule
# from apps.pedagog.models.weeks import Weeks
# from apps.pedagog.serializers.topic import TopicDetailSerializer
#
#
# class AlgorithmApiView(APIView):
#     def get(self, request):
#         science = request.query_params.get("science")
#         classes = request.query_params.get("classes")
#         week_name = request.query_params.get("week")
#         schedule_id = request.query_params.get("schedule_id")
#
#         if not science or not classes or not week_name or not schedule_id:
#             return Response(
#                 {"error": "science, classes, week va schedule_id parametrlari kerak"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         try:
#             # Week modelidan week_count ni olish
#             week = Weeks.objects.filter(id=week_name).first()
#             if not week:
#                 return Response(
#                     {"error": "Mos keladigan week topilmadi"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#
#             week_count = week.week_count
#
#             # Shu fan va sinfga mos keladigan Plan'ni topish
#             plan = Plan.objects.filter(science=science, classes=classes).first()
#             if not plan:
#                 return Response(
#                     {"error": "Mos keladigan Plan topilmadi"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#
#             # Shu Plan ichidan kerakli week_count ga mos keladigan topiclarni topish
#             topics = plan.topic.filter(weeks=week_count).order_by("sequence_number")
#             if not topics.exists():
#                 return Response(
#                     {"error": "Mos keladigan Topic topilmadi"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#
#             # Shu hafta uchun darslar sonini olish
#             schedule_choice = ScheduleChoices.objects.filter(
#                 user=request.user,
#                 week=week,
#                 schedule_template__schedules__science=science,
#                 schedule_template__schedules__classes=classes,
#             ).first()
#             if not schedule_choice:
#                 return Response(
#                     {"error": "Mos keladigan ScheduleChoice topilmadi"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#
#             total_classes = schedule_choice.schedule_template.schedules.count()
#             print(f"Total classes: {total_classes}")
#
#             # schedule_id orqali shu haftadagi nechinchi schedule ekanligini aniqlash
#             try:
#                 schedule = Schedule.objects.get(id=schedule_id)
#             except Schedule.DoesNotExist:
#                 return Response(
#                     {"error": "Mos keladigan Schedule topilmadi"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#
#             schedules = schedule_choice.schedule_template.schedules.order_by(
#                 "start_time", "weekday"
#             )
#             weekdays = schedules.values_list("weekday", flat=True).distinct()
#             print(f"Weekdays: {weekdays}")
#             print(f"Schedules: {schedules}")
#
#             if len(weekdays) == 1:
#                 schedule_position = (
#                     list(schedules.order_by("start_time")).index(schedule) + 1
#                 )
#             else:
#                 schedule_position = (
#                     list(schedules.order_by("weekday")).index(schedule) + 1
#                 )
#             print(f"Schedule position: {schedule_position}")
#
#             # Mavzularni darslarga to'g'ri taqsimlash
#             topic_list = []
#             class_counter = 0
#             topic_index = 0
#             current_topic_hours = 0
#             current_topic = None  # Define current_topic before the loop
#
#             while class_counter < total_classes:
#                 if current_topic_hours == 0:
#                     if topic_index < len(topics):
#                         current_topic = topics[topic_index]
#                         current_topic_hours = current_topic.hours
#                         topic_index += 1
#                     else:
#                         break
#
#                 class_counter += 1
#                 current_topic_hours -= 1
#
#                 if class_counter == schedule_position:
#                     topic_list.append(
#                         {
#                             "class_number": class_counter,
#                             "topic": TopicDetailSerializer(current_topic).data,
#                         }
#                     )
#
#             # Qoldirilgan mavzuni keyingi haftada qoldirmaslik uchun:
#             if current_topic_hours > 0 and class_counter == total_classes:
#                 # Bu holatda keyingi haftaga mavzuni qayta taqsimlash kerak
#                 class_counter = 0
#                 topic_list.append(
#                     {
#                         "class_number": class_counter,
#                         "topic": TopicDetailSerializer(current_topic).data,
#                     }
#                 )
#             print(f"Class counter: {class_counter}")
#             print(f"Topic list: {topic_list}")
#             print(f"Topic index: {topic_index}")
#             print(f"Current topic hours: {current_topic_hours}")
#             return Response(topic_list, status=status.HTTP_200_OK)
#
#         except Exception as e:
#             return Response(
#                 {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
