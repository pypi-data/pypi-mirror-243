from django.db.models import Q
from djangoldp.views import LDPViewSet
from djangoldp_community.models import Community

class MyTerritoriesView(LDPViewSet):
    model = Community
    parent_model = Community
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(Q(tzcld_profile__regions__referents=user) | Q(members__in=user.communities.filter(is_admin=True))).distinct()

class MemberOfCommunitiesView(LDPViewSet):
    model = Community
    parent_model = Community
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(Q(members__in=user.communities.filter(is_admin=True)) | Q(members__in=user.communities.filter(is_admin=False))).distinct()