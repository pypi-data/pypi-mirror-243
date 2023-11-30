# coding=utf-8
import logging

from management.controllers import events_controller as ec


logger = logging.getLogger()


def mgmt_add(node):
    ec.log_event_cluster(
        cluster_id=node.cluster_id,
        domain=ec.DOMAIN_CLUSTER,
        event=ec.EVENT_OBJ_CREATED,
        db_object=node,
        caused_by=ec.CAUSED_BY_CLI,
        message=f"Management node added {node.hostname}",
        node_id=node.get_id())


def mgmt_remove(node):
    ec.log_event_cluster(
        cluster_id=node.cluster_id,
        domain=ec.DOMAIN_CLUSTER,
        event=ec.EVENT_OBJ_DELETED,
        db_object=node,
        caused_by=ec.CAUSED_BY_CLI,
        message=f"Management node removed {node.hostname}",
        node_id=node.get_id())
