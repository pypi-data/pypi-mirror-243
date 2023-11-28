from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.python_name import package_name
class PublishedRecordMarshmallowBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "published_record_marshmallow"
    section = "marshmallow"
    template = "published-record-marshmallow"
    def _get_output_module(self):
        return package_name(self.current_model.published_record.definition["marshmallow"]["class"])
    def finish(self, **extra_kwargs):
        super().finish(
            published_record=self.current_model.published_record.definition, **extra_kwargs
        )
