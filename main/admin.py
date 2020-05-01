from django.contrib import admin
from django.http import HttpResponseRedirect
from django import forms

from main import models


def make_onpublished(modeladmin, request, queryset):
    queryset.update(is_pub=True)


make_onpublished.short_description = "Mark selected stories as published"


def make_offpublished(modeladmin, request, queryset):
    queryset.update(is_pub=False)


make_offpublished.short_description = "Mark selected stories as published off"


class PubAdmin(admin.ModelAdmin):
    """
    Publication model admin

    Add new 'admin/publish_changeform.html' template to change form and add On Publish button
    """
    list_display = ('title', 'author', 'created_date', 'is_pub')
    list_filter = ('title', 'author', 'created_date', 'is_pub')
    search_fields = ('title', 'text')
    actions = (make_onpublished, make_offpublished)

    change_form_template = "admin/publish_changeform.html"

    def response_change(self, request, obj):
        """
        Publish button
        Off publish button
        """
        # if publish button was pressed(_publish arg in POST data)
        if "_publish" in request.POST:
            obj.is_pub = True
            obj.save()
            self.message_user(request, "This publication now published")
            return HttpResponseRedirect(".")
        # if publish-off button was pressed(_publish arg in POST data)
        elif "_offpublish" in request.POST:
            obj.is_pub = False
            obj.save()
            self.message_user(request, "This publication published off")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


admin.site.register(models.Pub, PubAdmin)

admin.site.register(models.Comment)
