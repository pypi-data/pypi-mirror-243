"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.service_accounts import (
    ServiceAccount,
    ServiceAccountGroup,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class ServiceAccountFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccount

    name = factory.Faker("domain_name")
    group = ServiceAccountGroup.MAIL_PROXY
    default_ipv6_ip_address = None
    default_ipv4_ip_address = None
    default_ipv6_netbox_id = None
    default_ipv4_netbox_id = None
