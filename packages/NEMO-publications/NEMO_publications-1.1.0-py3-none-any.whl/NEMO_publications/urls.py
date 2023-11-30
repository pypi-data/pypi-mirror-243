from NEMO.urls import router, sort_urls
from django.urls import path

from NEMO_publications import api, views

router.register(r"publication_metadata", api.PublicationMetadataViewSet)
router.register(r"publication_data", api.PublicationDataViewSet)
router.register(r"publication", api.PublicationViewSet, basename="publication")
router.registry.sort(key=sort_urls)

urlpatterns = [
    path(
        "search_publication",
        views.search_publication_by_doi,
        name="search_publication",
    ),
    path(
        "edit_publication/<int:publication_data_id>/",
        views.create_or_update_publication_data,
        name="edit_publication",
    ),
    path(
        "create_publication/<int:publication_metadata_id>/",
        views.create_or_update_publication_data,
        name="create_publication",
    ),
    path(
        "save_publication_metadata",
        views.create_publication_metadata,
        name="save_publication_metadata",
    ),
    path(
        "delete_publication/<int:publication_data_id>/",
        views.delete_publication,
        name="delete_publication",
    ),
    path(
        "publication_user_search",
        views.user_search,
        name="publication_user_search",
    ),
    path("publications/", views.get_publications, name="publications"),
]
