from django.urls import path

from .views import (
        attendanceCapture,
        attendanceUpload,
        attendanceView,
        attendanceStatistics,

        dynamic_stream,
        attendanceCapture_dev,
    )

urlpatterns = [
    path('capture_attendance/',attendanceCapture, name="capture-attendance"),
    path('attendance_upload/', attendanceUpload, name="attendance-upload"),
    path('attendance_view/', attendanceView, name="attendance-view"),
    path('attendance_statistics/', attendanceStatistics, name="attendance-statistics"),

    path('attendanceCapture_dev/',attendanceCapture, name="capture-attendance-dev"),
    path('capture_video/<stream_path>/', dynamic_stream,name="videostream"),

]
