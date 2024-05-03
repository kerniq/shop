import csv
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.db.models.options import Options


class ExportAsCSVMixins:
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}-export.csv"

        csv_whiter = csv.writer(response)
        csv_whiter.writerow(field_names)

        for obj in queryset:
            csv_whiter.writerow([getattr(obj, field) for field in field_names])

        return response

    export_csv.short_description = "Export as CSV"
