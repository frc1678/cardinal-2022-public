from django.conf.urls import url
from django.urls import path, include
from .views import (
    InitialApiView,
    TestDataGeneratorApiView,
    CollectionDataRequestApiView,
    TestDataGeneratorApiView,
    SupportedCollectionsApiView,
    MatchScheduleApiView,
    TeamsListApiView,
    VersionApiView,
    LogFileApiView,
)
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny


SchemaView = get_schema_view(
    title="Cardinal",
    description="Cardinal",
    version="1.0.0",
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("hello/", InitialApiView.as_view()),
    path("version/", VersionApiView.as_view()),
    url(
        r'^openapi-schema',
        SchemaView,
        name='openapi-schema',
    ),
    url(
        r'docs/',
        TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={'schema_url': 'openapi-schema'},
        ),
        name='swagger-ui',
    ),
    path("collection/<str:collection_name>/", CollectionDataRequestApiView.as_view()),
    path("supported-collections/", SupportedCollectionsApiView.as_view()),
    path("generate/<str:data_structure_type>/", TestDataGeneratorApiView.as_view()),
    path("match-schedule/<str:comp_code>/", MatchScheduleApiView.as_view()),
    path("teams-list/<str:comp_code>/", TeamsListApiView.as_view()),
    path("log-file/", LogFileApiView.as_view()),
]
