# coding=utf-8
import logging

from management.controllers import events_controller as ec
from management.kv_store import DBController

logger = logging.getLogger()
db_controller = DBController()


def cluster_create(cluster):
    ec.log_event_cluster(
        cluster_id=cluster.get_id(),
        domain=ec.DOMAIN_CLUSTER,
        event=ec.EVENT_OBJ_CREATED,
        db_object=cluster,
        caused_by=ec.CAUSED_BY_CLI,
        message=f"Cluster created {cluster.get_id()}")


def cluster_status_change(cluster, new_state, old_status):
    ec.log_event_cluster(
        cluster_id=cluster.get_id(),
        domain=ec.DOMAIN_CLUSTER,
        event=ec.EVENT_STATUS_CHANGE,
        db_object=cluster,
        caused_by=ec.CAUSED_BY_CLI,
        message=f"Cluster status changed from {old_status} to {new_state}")
