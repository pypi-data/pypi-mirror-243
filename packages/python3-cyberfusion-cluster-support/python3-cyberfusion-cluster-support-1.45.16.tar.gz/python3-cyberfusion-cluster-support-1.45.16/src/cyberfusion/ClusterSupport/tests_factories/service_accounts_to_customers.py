"""Factories for API object."""

import factory

from cyberfusion.ClusterSupport.service_accounts import ServiceAccountGroup
from cyberfusion.ClusterSupport.service_accounts_to_customers import (
    ServiceAccountToCustomer,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class ServiceAccountToCustomerFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountToCustomer

        exclude = ("service_account",)

    customer_id = 1
    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountFactory",
        group=ServiceAccountGroup.INTERNET_ROUTER,
        default_ipv6_ip_address=factory.Faker("ipv6"),
        default_ipv4_ip_address=factory.Faker("ipv4"),
        default_ipv6_netbox_id=factory.Faker("random_int", min=500, max=2000),
        default_ipv4_netbox_id=factory.Faker("random_int", min=500, max=2000),
        netbox_additional_prefix_ipv6_id=factory.Faker(
            "random_int", min=500, max=2000
        ),
        netbox_additional_prefix_ipv4_id=factory.Faker(
            "random_int", min=500, max=2000
        ),
        netbox_fhrp_group_ipv6_id=factory.Faker(
            "random_int", min=500, max=2000
        ),
        netbox_fhrp_group_ipv4_id=factory.Faker(
            "random_int", min=500, max=2000
        ),
    )
    service_account_id = factory.SelfAttribute("service_account.id")
