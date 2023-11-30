# coding=utf-8

from datetime import datetime

from management.models.base_model import BaseModel


class MgmtNode(BaseModel):

    STATUS_ONLINE = 'online'
    STATUS_OFFLINE = 'offline'
    STATUS_ERROR = 'error'
    STATUS_REPLACED = 'replaced'
    STATUS_SUSPENDED = 'suspended'
    STATUS_IN_CREATION = 'in_creation'
    STATUS_IN_SHUTDOWN = 'in_shutdown'
    STATUS_RESTARTING = 'restarting'
    STATUS_REMOVED = 'removed'
    STATUS_UNREACHABLE = 'unreachable'

    attributes = {
        "baseboard_sn": {"type": str, 'default': ""},
        "system_uuid": {"type": str, 'default': ""},
        "hostname": {"type": str, 'default': ""},
        "status": {"type": str, 'default': ""},
        "docker_ip_port": {"type": str, 'default': ""},
        "cluster_id": {"type": str, 'default': ""},
        "mgmt_ip": {"type": str, 'default': ""},
        "updated_at": {"type": str, 'default': str(datetime.now())},

    }

    def __init__(self, data=None):
        super(MgmtNode, self).__init__()
        self.set_attrs(self.attributes, data)
        self.object_type = "object"

    def get_id(self):
        return self.system_uuid
