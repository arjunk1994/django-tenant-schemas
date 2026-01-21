from django.db.migrations.exceptions import MigrationSchemaMissing

from tenant_schemas.management.commands import SyncCommon
from tenant_schemas.migration_executors import get_executor
from tenant_schemas.utils import (
    get_public_schema_name,
    get_tenant_model,
    schema_exists,
)


class Command(SyncCommon):
    help = (
        "Updates database schema. Manages both apps with migrations and those without."
    )

    def add_arguments(self, parser):
        # SyncCommon ALREADY adds migrate arguments
        super().add_arguments(parser)

        # 🔥 Remove duplicate Django 3.2+ option
        for action in list(parser._actions):
            if "--skip-checks" in action.option_strings:
                parser._remove_action(action)

    def handle(self, *args, **options):
        super().handle(*args, **options)

        self.PUBLIC_SCHEMA_NAME = get_public_schema_name()
        executor = get_executor(codename=self.executor)(self.args, self.options)

        # Public schema
        if self.sync_public and not self.schema_name:
            self.schema_name = self.PUBLIC_SCHEMA_NAME

        if self.sync_public:
            executor.run_migrations(tenants=[self.schema_name])

        # Tenant schemas
        if self.sync_tenant:
            if self.schema_name and self.schema_name != self.PUBLIC_SCHEMA_NAME:
                if not schema_exists(self.schema_name):
                    raise MigrationSchemaMissing(
                        f'Schema "{self.schema_name}" does not exist'
                    )
                tenants = [self.schema_name]
            else:
                tenants = (
                    get_tenant_model()
                    .objects.exclude(schema_name=get_public_schema_name())
                    .values_list("schema_name", flat=True)
                )

            executor.run_migrations(tenants=tenants)
