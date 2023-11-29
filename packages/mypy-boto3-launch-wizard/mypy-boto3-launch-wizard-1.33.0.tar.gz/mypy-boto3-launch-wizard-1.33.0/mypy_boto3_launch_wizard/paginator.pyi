"""
Type annotations for launch-wizard service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_launch_wizard/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_launch_wizard.client import LaunchWizardClient
    from mypy_boto3_launch_wizard.paginator import (
        ListDeploymentEventsPaginator,
        ListDeploymentsPaginator,
        ListWorkloadDeploymentPatternsPaginator,
        ListWorkloadsPaginator,
    )

    session = Session()
    client: LaunchWizardClient = session.client("launch-wizard")

    list_deployment_events_paginator: ListDeploymentEventsPaginator = client.get_paginator("list_deployment_events")
    list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
    list_workload_deployment_patterns_paginator: ListWorkloadDeploymentPatternsPaginator = client.get_paginator("list_workload_deployment_patterns")
    list_workloads_paginator: ListWorkloadsPaginator = client.get_paginator("list_workloads")
    ```
"""

from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DeploymentFilterTypeDef,
    ListDeploymentEventsOutputTypeDef,
    ListDeploymentsOutputTypeDef,
    ListWorkloadDeploymentPatternsOutputTypeDef,
    ListWorkloadsOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListDeploymentEventsPaginator",
    "ListDeploymentsPaginator",
    "ListWorkloadDeploymentPatternsPaginator",
    "ListWorkloadsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDeploymentEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Paginator.ListDeploymentEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_launch_wizard/paginators/#listdeploymenteventspaginator)
    """

    def paginate(
        self, *, deploymentId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Paginator.ListDeploymentEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_launch_wizard/paginators/#listdeploymenteventspaginator)
        """

class ListDeploymentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Paginator.ListDeployments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_launch_wizard/paginators/#listdeploymentspaginator)
    """

    def paginate(
        self,
        *,
        filters: Sequence[DeploymentFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Paginator.ListDeployments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_launch_wizard/paginators/#listdeploymentspaginator)
        """

class ListWorkloadDeploymentPatternsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Paginator.ListWorkloadDeploymentPatterns)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_launch_wizard/paginators/#listworkloaddeploymentpatternspaginator)
    """

    def paginate(
        self, *, workloadName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkloadDeploymentPatternsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Paginator.ListWorkloadDeploymentPatterns.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_launch_wizard/paginators/#listworkloaddeploymentpatternspaginator)
        """

class ListWorkloadsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Paginator.ListWorkloads)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_launch_wizard/paginators/#listworkloadspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkloadsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Paginator.ListWorkloads.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_launch_wizard/paginators/#listworkloadspaginator)
        """
