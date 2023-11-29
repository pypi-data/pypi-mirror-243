"""
Type annotations for migrationhuborchestrator service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_migrationhuborchestrator.client import MigrationHubOrchestratorClient
    from mypy_boto3_migrationhuborchestrator.paginator import (
        ListPluginsPaginator,
        ListTemplateStepGroupsPaginator,
        ListTemplateStepsPaginator,
        ListTemplatesPaginator,
        ListWorkflowStepGroupsPaginator,
        ListWorkflowStepsPaginator,
        ListWorkflowsPaginator,
    )

    session = Session()
    client: MigrationHubOrchestratorClient = session.client("migrationhuborchestrator")

    list_plugins_paginator: ListPluginsPaginator = client.get_paginator("list_plugins")
    list_template_step_groups_paginator: ListTemplateStepGroupsPaginator = client.get_paginator("list_template_step_groups")
    list_template_steps_paginator: ListTemplateStepsPaginator = client.get_paginator("list_template_steps")
    list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
    list_workflow_step_groups_paginator: ListWorkflowStepGroupsPaginator = client.get_paginator("list_workflow_step_groups")
    list_workflow_steps_paginator: ListWorkflowStepsPaginator = client.get_paginator("list_workflow_steps")
    list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import MigrationWorkflowStatusEnumType
from .type_defs import (
    ListMigrationWorkflowsResponseTypeDef,
    ListMigrationWorkflowTemplatesResponseTypeDef,
    ListPluginsResponseTypeDef,
    ListTemplateStepGroupsResponseTypeDef,
    ListTemplateStepsResponseTypeDef,
    ListWorkflowStepGroupsResponseTypeDef,
    ListWorkflowStepsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListPluginsPaginator",
    "ListTemplateStepGroupsPaginator",
    "ListTemplateStepsPaginator",
    "ListTemplatesPaginator",
    "ListWorkflowStepGroupsPaginator",
    "ListWorkflowStepsPaginator",
    "ListWorkflowsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListPluginsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListPlugins)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listpluginspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPluginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListPlugins.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listpluginspaginator)
        """

class ListTemplateStepGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListTemplateStepGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatestepgroupspaginator)
    """

    def paginate(
        self, *, templateId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTemplateStepGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListTemplateStepGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatestepgroupspaginator)
        """

class ListTemplateStepsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListTemplateSteps)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatestepspaginator)
    """

    def paginate(
        self, *, templateId: str, stepGroupId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTemplateStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListTemplateSteps.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatestepspaginator)
        """

class ListTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatespaginator)
    """

    def paginate(
        self, *, name: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMigrationWorkflowTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatespaginator)
        """

class ListWorkflowStepGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListWorkflowStepGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowstepgroupspaginator)
    """

    def paginate(
        self, *, workflowId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkflowStepGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListWorkflowStepGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowstepgroupspaginator)
        """

class ListWorkflowStepsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListWorkflowSteps)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowstepspaginator)
    """

    def paginate(
        self, *, workflowId: str, stepGroupId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkflowStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListWorkflowSteps.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowstepspaginator)
        """

class ListWorkflowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListWorkflows)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowspaginator)
    """

    def paginate(
        self,
        *,
        templateId: str = ...,
        adsApplicationConfigurationName: str = ...,
        status: MigrationWorkflowStatusEnumType = ...,
        name: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMigrationWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator.html#MigrationHubOrchestrator.Paginator.ListWorkflows.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowspaginator)
        """
