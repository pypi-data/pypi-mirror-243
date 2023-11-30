from django.contrib import admin
from django.contrib.admin import register

from NEMO_publications.forms import PublicationDataForm
from NEMO_publications.models import PublicationMetadata, PublicationData
from NEMO_publications.views import export_publications


@admin.action(description="Export selected publications in CSV")
def export_publication_for_metadata(model_admin, request, queryset):
    return export_publications(queryset.all())


@admin.action(description="Delete all associated publication data")
def delete_publication_data(model_admin, request, queryset):
    PublicationData.objects.filter(metadata__in=queryset.all()).delete()


@admin.action(description="Delete all publication metadata without data entries")
def delete_metadata_without_data(model_admin, request, queryset):
    PublicationMetadata.objects.filter(publicationdata=None).delete()


@register(PublicationMetadata)
class PublicationMetadataAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "journal",
        "month",
        "year",
        "doi",
    )
    list_filter = (
        "year",
        "month",
        ("creator", admin.RelatedOnlyFieldListFilter),
    )
    date_hierarchy = "creation_time"
    actions = [export_publication_for_metadata, delete_publication_data, delete_metadata_without_data]


@register(PublicationData)
class PublicationDataAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "metadata",
        "get_authors",
        "get_tools",
        "get_projects",
    )
    filter_horizontal = (
        "authors",
        "tools",
        "projects",
    )
    form = PublicationDataForm
    list_filter = [("creator", admin.RelatedOnlyFieldListFilter), ("metadata", admin.RelatedOnlyFieldListFilter)]
    date_hierarchy = "creation_time"

    def get_authors(self, data):
        return data.get_authors()

    def get_tools(self, data):
        return data.get_tools()

    def get_projects(self, data):
        return data.get_projects()
