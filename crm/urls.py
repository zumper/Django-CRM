from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.urls import include, path
from common.views import handler404, handler500

app_name = 'crm'

urlpatterns = [
    path('', include('common.urls', namespace="common")),
    path('', include('django.contrib.auth.urls')),
    path('marketing/', include('marketing.urls', namespace="marketing")),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('leads/', include('leads.urls', namespace="leads")),
    path('contacts/', include('contacts.urls', namespace="contacts")),
    path('opportunities/',
         include('opportunity.urls', namespace="opportunities")),
    path('cases/', include('cases.urls', namespace="cases")),
    path('tasks/', include('tasks.urls', namespace="tasks")),
    path('invoices/', include('invoices.urls', namespace="invoices")),
    path('events/', include('events.urls', namespace="events")),
    path('teams/', include('teams.urls', namespace="teams")),
    path('emails/', include('emails.urls', namespace="emails")),

    # path('planner/', include('planner.urls', namespace="planner")),
    path('logout/', views.LogoutView, {'next_page': '/login/'}, name="logout"),
]

custom_url_patterns = [
    path('api/', include('api.urls', namespace='api')),
    path('interests/', include('interests.urls', namespace='interests')),
    path('listings/', include('listings.urls', namespace="listings")),
    path('buildings/', include('buildings.urls', namespace="buildings")),
    path('deals/', include('deals.urls', namespace="deals")),
]

urlpatterns = urlpatterns + custom_url_patterns

if settings.DEBUG:
  urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = handler404
handler500 = handler500
