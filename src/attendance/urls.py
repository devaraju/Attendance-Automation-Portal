from django.urls import path

from .views import (
        dynamic_stream,
        attendanceCapture,
        attendanceUpload,
        attendanceView,
        attendanceStatistics
    ) 

urlpatterns = [
    path('capture_attendance/',attendanceCapture, name="capture-attendance"),
    path('capture_video/<stream_path>/', dynamic_stream,name="videostream"),

    path('attendance_upload/', attendanceUpload, name="attendance-upload"),
    path('attendance_view/', attendanceView, name="attendance-view"),
    path('attendance_statistics/', attendanceStatistics, name="attendance-statistics"),

]