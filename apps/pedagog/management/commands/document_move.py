from django.core.management.base import BaseCommand

from apps.pedagog.models.documents import Document, FileModel


class Command(BaseCommand):

    def handle(self, *args, **options):
        documents = Document.objects.all()
        for document in documents:
            file = document.file
            if not file.name:
                self.stdout.write("File mavjud emas")
                continue
            self.stdout.write("Fayil ko'chirildi {}".format(document.id))
            file_instance, created = FileModel.objects.get_or_create(file=file)
            document.document_file.add(file_instance)
