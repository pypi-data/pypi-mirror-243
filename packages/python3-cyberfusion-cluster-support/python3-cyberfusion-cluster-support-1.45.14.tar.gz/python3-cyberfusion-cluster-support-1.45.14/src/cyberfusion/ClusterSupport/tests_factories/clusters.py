"""Factories for API object."""

from typing import Any, Dict, List, Optional

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.clusters import (
    Cluster,
    ClusterGroup,
    MeilisearchEnvironment,
    UNIXUserHomeDirectory,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class ClusterFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = Cluster

    customer_id = 1
    php_ioncube_enabled: bool = False
    meilisearch_master_key: Optional[str] = None
    meilisearch_environment: Optional[MeilisearchEnvironment] = None
    meilisearch_backup_interval: Optional[int] = None
    new_relic_apm_license_key: Optional[str] = None
    new_relic_mariadb_password: Optional[str] = None
    new_relic_infrastructure_license_key: Optional[str] = None
    php_sessions_spread_enabled: bool = False
    http_retry_properties: Optional[dict] = None
    kernelcare_license_key: Optional[str] = None
    wordpress_toolkit_enabled: bool = False
    malware_toolkit_enabled: bool = False
    sync_toolkit_enabled: bool = False
    bubblewrap_toolkit_enabled: bool = False
    malware_toolkit_scans_enabled: bool = False
    database_toolkit_enabled: bool = False
    description = factory.Faker("word")
    unix_users_home_directory: Optional[str] = None
    php_versions: List[str] = []
    redis_password: Optional[str] = None
    postgresql_backup_interval: Optional[int] = None
    mariadb_backup_interval: Optional[int] = None
    mariadb_cluster_name: Optional[str] = None
    redis_memory_limit: Optional[int] = None
    mariadb_version: Optional[str] = None
    postgresql_version: Optional[int] = None
    nodejs_version: Optional[int] = None
    nodejs_versions: List[str] = []
    custom_php_modules_names: List[str] = []
    php_settings: Dict[str, Any] = {}
    automatic_borg_repositories_prune_enabled: bool = False
    groups: List[str] = []


class ClusterWebFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.WEB]
    unix_users_home_directory = factory.fuzzy.FuzzyChoice(
        UNIXUserHomeDirectory
    )
    php_versions = ["8.1", "8.0", "7.4", "7.3", "7.2", "7.1", "7.0", "5.6"]
    nodejs_versions = ["14.0"]
    nodejs_version = 18
    http_retry_properties: dict = {
        "tries_amount": None,
        "tries_failover_amount": None,
        "conditions": [],
    }


class ClusterRedirectFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.REDIRECT]
    http_retry_properties: dict = {
        "tries_amount": None,
        "tries_failover_amount": None,
        "conditions": [],
    }


class ClusterDatabaseFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.DB]
    mariadb_version = "10.10"
    postgresql_version = 15
    mariadb_cluster_name = factory.Faker(
        "password",
        special_chars=False,
        upper_case=False,
        digits=False,
    )
    redis_password = factory.Faker("password", special_chars=False, length=24)
    redis_memory_limit = factory.Faker("random_int", min=32, max=1024)
    mariadb_backup_interval = factory.Faker("random_int", min=4, max=24)
    postgresql_backup_interval = factory.Faker("random_int", min=4, max=24)


class ClusterMailFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.MAIL]
    unix_users_home_directory = UNIXUserHomeDirectory.MNT_MAIL


class ClusterBorgClientFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.BORG_CLIENT, ClusterGroup.WEB]
    unix_users_home_directory = factory.fuzzy.FuzzyChoice(
        UNIXUserHomeDirectory
    )
    http_retry_properties: dict = {
        "tries_amount": None,
        "tries_failover_amount": None,
        "conditions": [],
    }


class ClusterBorgServerFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.BORG_SERVER]
    unix_users_home_directory = UNIXUserHomeDirectory.MNT_BACKUPS
