# coding=utf-8
import datetime
import json
import logging as lg
import math
import time
import uuid

import docker


from management import utils, scripts, constants
from management.cnode_client import CNodeClient
from management.kv_store import DBController
from management.models.caching_node import CachingNode
from management.models.iface import IFace
from management.models.nvme_device import NVMeDevice
from management.models.pool import Pool
from management.rpc_client import RPCClient

logger = lg.getLogger()

db_controller = DBController()


def addNvmeDevices(cluster, rpc_client, devs, snode):
    sequential_number = 0
    devices = []
    ret = rpc_client.bdev_nvme_controller_list()
    ctr_map = {i["ctrlrs"][0]['trid']['traddr']: i["name"] for i in ret}

    for index, pcie in enumerate(devs):

        if pcie in ctr_map:
            nvme_bdev = ctr_map[pcie] + "n1"
        else:
            name = "nvme_%s" % pcie.split(":")[2].split(".")[0]
            ret, err = rpc_client.bdev_nvme_controller_attach(name, pcie)
            time.sleep(2)
            nvme_bdev = f"{name}n1"

        ret = rpc_client.get_bdevs(nvme_bdev)
        if ret:
            nvme_dict = ret[0]
            nvme_driver_data = nvme_dict['driver_specific']['nvme'][0]
            model_number = nvme_driver_data['ctrlr_data']['model_number']
            if model_number not in cluster.model_ids:
                logger.warning("Device model ID is not recognized: %s, "
                               "skipping device: %s", model_number)
                continue
            size = nvme_dict['block_size'] * nvme_dict['num_blocks']
            device_partitions_count = int(size / (cluster.blk_size * cluster.page_size_in_blocks))
            devices.append(
                NVMeDevice({
                    'uuid': str(uuid.uuid4()),
                    'device_name': nvme_dict['name'],
                    'sequential_number': sequential_number,
                    'partitions_count': device_partitions_count,
                    'capacity': size,
                    'size': size,
                    'pcie_address': nvme_driver_data['pci_address'],
                    'model_id': model_number,
                    'serial_number': nvme_driver_data['ctrlr_data']['serial_number'],
                    'nvme_bdev': nvme_bdev,
                    'alloc_bdev': nvme_bdev,
                    'node_id': snode.get_id(),
                    'status': 'online'
                }))
            sequential_number += device_partitions_count
    return devices


def add_node(cluster_id, node_ip, iface_name, data_nics_list, spdk_cpu_mask, spdk_mem, spdk_image=None):
    db_controller = DBController()
    kv_store = db_controller.kv_store

    clusters = db_controller.get_clusters(cluster_id)
    if not clusters:
        logger.error("Cluster not found: %s", cluster_id)
        return False
    cluster = clusters[0]

    logger.info(f"Add Storage node: {node_ip}")
    snode_api = CNodeClient(node_ip)

    node_info, _ = snode_api.info()
    logger.info(f"Node found: {node_info['hostname']}")

    hostname = node_info['hostname']
    snode = db_controller.get_storage_node_by_hostname(hostname)
    if snode:
        logger.error("Node already exists, try remove it first.")
        return False

    logger.info("Deploying SPDK")
    results, err = snode_api.spdk_process_start(spdk_cpu_mask, spdk_mem, spdk_image)
    time.sleep(10)
    if not results:
        logger.error(f"Failed to start spdk: {err}")
        return False

    results, err = snode_api.join_db(db_connection=cluster.db_connection)

    data_nics = []
    names = data_nics_list or [iface_name]
    for nic in names:
        device = node_info['network_interface'][nic]
        data_nics.append(
            IFace({
                'uuid': str(uuid.uuid4()),
                'if_name': device['name'],
                'ip4_address': device['ip'],
                'status': device['status'],
                'net_type': device['net_type']}))

    rpc_user, rpc_pass = utils.generate_rpc_user_and_pass()
    BASE_NQN = cluster.nqn.split(":")[0]
    subsystem_nqn = f"{BASE_NQN}:{hostname}"
    # creating storage node object
    snode = CachingNode()
    snode.uuid = str(uuid.uuid4())
    snode.status = CachingNode.STATUS_IN_CREATION
    # snode.baseboard_sn = node_info['system_id']
    snode.system_uuid = node_info['system_id']
    snode.hostname = hostname
    # snode.host_nqn = subsystem_nqn
    snode.subsystem = subsystem_nqn
    snode.data_nics = data_nics
    snode.mgmt_ip = node_info['network_interface'][iface_name]['ip']
    snode.rpc_port = constants.RPC_HTTP_PROXY_PORT
    snode.rpc_username = rpc_user
    snode.rpc_password = rpc_pass
    snode.cluster_id = cluster_id
    snode.api_endpoint = node_ip
    snode.host_secret = utils.generate_string(20)
    snode.ctrl_secret = utils.generate_string(20)
    snode.write_to_db(kv_store)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip, snode.rpc_port,
        snode.rpc_username, snode.rpc_password)

    # get new node info after starting spdk
    node_info, _ = snode_api.info()
    # adding devices
    nvme_devs = addNvmeDevices(cluster, rpc_client, node_info['spdk_pcie_list'], snode)
    if not nvme_devs:
        logger.error("No NVMe devices was found!")

    snode.nvme_devices = nvme_devs
    snode.write_to_db(db_controller.kv_store)

    ssd_dev = nvme_devs[0]

    # get node hugepages memory
    mem = node_info['hugepages']
    logger.info(f"Hugepages detected: {mem}")
    if mem < 1024*1024:
        return False

    supported_ssd_size = mem * 100 / 2
    split_factor = math.ceil(ssd_dev.size/supported_ssd_size)

    ret = rpc_client.bdev_split(ssd_dev.nvme_bdev, split_factor)
    cache_bdev_name = ret[0]
    snode.cache_bdev = cache_bdev_name
    # get ssd size
    # get split factor
    # set cache_bdev_name


    logger.info("Setting node status to Active")
    snode.status = CachingNode.STATUS_ONLINE
    snode.write_to_db(kv_store)

    logger.info("Done")
    return "Success"


def connect(caching_node_id, lvol_id):
    lvol = db_controller.get_lvol_by_id(lvol_id)
    if not lvol:
        logger.error(f"LVol not found: {lvol_id}")
        return False

    if lvol.status != lvol.STATUS_ONLINE:
        logger.error(f"LVol must be online, lvol status: {lvol.status}")
        return False

    pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False

    cnode = None
    if caching_node_id == 'this':
        hostn = utils.get_hostname()
        logger.info(f"Trying to get node by hostname: {hostn}")
        cnode = db_controller.get_caching_node_by_hostname(hostn)
    else:
        cnode = db_controller.get_caching_node_by_id(caching_node_id)
        if not cnode:
            logger.info(f"Caching node uuid not found: {caching_node_id}")
            cnode = db_controller.get_caching_node_by_hostname(caching_node_id)
            if not cnode:
                logger.error("Caching node not found")
                return False


    rpc_client = RPCClient(
        cnode.mgmt_ip, cnode.rpc_port, cnode.rpc_username, cnode.rpc_password)

    # create nvmef connection
    if lvol.ha_type == 'single':
        snode = db_controller.get_storage_node_by_id(lvol.node_id)
        for nic in snode.data_nics:
            ret = rpc_client.bdev_nvme_attach_controller_tcp(lvol.get_id(), lvol.nqn, nic.ip4_address, "4420")
            logger.debug(ret)

    elif lvol.ha_type == "ha":
        for nodes_id in lvol.nodes:
            snode = db_controller.get_storage_node_by_id(nodes_id)
            for nic in snode.data_nics:
                ret = rpc_client.bdev_nvme_attach_controller_tcp(lvol.get_id(), lvol.nqn, nic.ip4_address, "4420")
                logger.debug(ret)

    # create ocf device
    cach_bdev = f"ocf_{lvol.get_id()}"
    dev = cnode.cache_bdev
    ret = rpc_client.bdev_ocf_create(cach_bdev, 'wt', dev, f"{lvol.get_id()}n1")
    logger.debug(ret)
    if not ret:
        logger.error("Failed to create OCF bdev")
        return False

    # create subsystem (local)
    subsystem_nqn = cnode.subsystem + ":lvol:" + lvol.get_id()
    logger.info("Creating subsystem %s", subsystem_nqn)
    ret = rpc_client.subsystem_create(subsystem_nqn, 'sbcli-cn', lvol.get_id())
    ret = rpc_client.transport_list("TCP")
    if not ret:
        ret = rpc_client.transport_create("TCP")
    ret = rpc_client.listeners_create(subsystem_nqn, "TCP", '127.0.0.1', "4420")

    # add cached device to subsystem
    logger.info(f"add {cach_bdev} to subsystem {subsystem_nqn}")
    ret = rpc_client.nvmf_subsystem_add_ns(subsystem_nqn, cach_bdev)
    if not ret:
        logger.error(f"Failed to add: {cach_bdev} to the subsystem: {subsystem_nqn}")
        return False

    # make nvme connect to nqn
    cnode_client = CNodeClient(cnode.api_endpoint)
    ret = cnode_client.connect_nvme('127.0.0.1', "4420", lvol.nqn)

    # add lvol to cnode
    cnode.lvols = list(set(cnode.lvols.append(lvol.get_id())))
    cnode.write_to_db(db_controller.kv_store)

    # TODO: return device path
    nvme_devs = cnode_client.info()['nvme_devices']
    logger.debug(nvme_devs)
    for dev in nvme_devs:
        if dev['model_id'] == lvol.get_id():
            return dev['device_path']
    return True


def disconnect(caching_node_id, lvol_id):
    lvol = db_controller.get_lvol_by_id(lvol_id)
    if not lvol:
        logger.error(f"LVol not found: {lvol_id}")
        return False

    cnode = None
    if caching_node_id == 'this':
        hostn = utils.get_hostname()
        logger.info(f"Trying to get node by hostname: {hostn}")
        cnode = db_controller.get_caching_node_by_hostname(hostn)
    else:
        cnode = db_controller.get_caching_node_by_id(caching_node_id)
        if not cnode:
            logger.info(f"Caching node uuid not found: {caching_node_id}")
            cnode = db_controller.get_caching_node_by_hostname(caching_node_id)
            if not cnode:
                logger.error("Caching node not found")
                return False


    # disconnect local nvme
    cnode_client = CNodeClient(cnode.api_endpoint)
    ret = cnode_client.disconnect_nqn(lvol.nqn)

    # remove subsystem
    rpc_client = RPCClient(
        cnode.mgmt_ip, cnode.rpc_port, cnode.rpc_username, cnode.rpc_password)

    subsystem_nqn = cnode.subsystem + ":lvol:" + lvol.get_id()
    ret = rpc_client.subsystem_delete(subsystem_nqn)

    # remove ocf bdev
    cach_bdev = f"ocf_{lvol.get_id()}"
    ret = rpc_client.bdev_ocf_delete(cach_bdev)

    # disconnect lvol controller/s
    ret = rpc_client.bdev_nvme_detach_controller(lvol.get_id())

    # remove lvol id from node lvol list
    cnode.lvols.remove(lvol.get_id())
    cnode.write_to_db(db_controller.kv_store)




    # if lvol.ha_type == 'single':
    #     ret = rpc_client.bdev_nvme_detach_controller(lvol.get_id())
    #
    # elif lvol.ha_type == "ha":
    #     for nodes_id in lvol.nodes:
    #         snode = db_controller.get_storage_node_by_id(nodes_id)
    #         ret = rpc_client.bdev_nvme_attach_controller_tcp(lvol.get_id(), lvol.nqn, nic.ip4_address, "4420")
    return True




def deploy():
    logger.info("Installing dependencies")
    ret = scripts.install_deps()

    DEV_IP = utils.get_ips().split()[0]
    logger.info(f"Node IP: {DEV_IP}")

    node_docker = docker.DockerClient(base_url=f"tcp://{DEV_IP}:2375", version="auto", timeout=60 * 5)
    # create the api container
    nodes = node_docker.containers.list(all=True)
    for node in nodes:
        if node.attrs["Name"] == "/CachingNodeAPI":
            logger.info("CachingNodeAPI container found, skip deploy...")
            return False

    logger.info("Creating CachingNodeAPI container")
    container = node_docker.containers.run(
        "hamdykhader/simplyblock:latest",
        "python WebApp/caching_node_app.py",
        detach=True,
        privileged=True,
        name="CachingNodeAPI",
        network_mode="host",
        volumes=[
            '/etc/foundationdb:/etc/foundationdb',
            '/var/tmp:/var/tmp',
            '/var/run:/var/run',
            '/dev:/dev',
            '/lib/modules/:/lib/modules/',
            '/sys:/sys'],
        restart_policy={"Name": "on-failure", "MaximumRetryCount": 99}
    )
    logger.info("Pulling spdk image")
    node_docker.images.pull("hamdykhader/spdk:core")
    return f"{DEV_IP}:5000"


def list_nodes(is_json=False):
    db_controller = DBController()
    nodes = db_controller.get_caching_nodes()
    data = []
    output = ""

    for node in nodes:
        logger.debug(node)
        logger.debug("*" * 20)
        data.append({
            "UUID": node.uuid,
            "Hostname": node.hostname,
            "Management IP": node.mgmt_ip,
            # "Subsystem": node.subsystem,
            "NVMe Devs": f"{len(node.nvme_devices)}",
            "LVOLs": f"{len(node.lvols)}",
            # "Data NICs": "\n".join([d.if_name for d in node.data_nics]),
            "Status": node.status,
            # "Updated At": datetime.datetime.strptime(node.updated_at, "%Y-%m-%d %H:%M:%S.%f").strftime(
            #     "%H:%M:%S, %d/%m/%Y"),
        })

    if not data:
        return output

    if is_json:
        output = json.dumps(data, indent=2)
    else:
        output = utils.print_table(data)
    return output


def remove_node(node_id, force=False):
    db_controller = DBController()
    snode = db_controller.get_caching_node_by_id(node_id)
    if not snode:
        logger.error(f"Can not find caching node: {node_id}")
        return False

    if snode.lvols:
        if force:
            for lvol_id in snode.lvols:
                logger.info(f"Disconnecting LVol {lvol_id}")
                disconnect(node_id, lvol_id)
        else:
            logger.error("Connected LVols found on the node, use --force to disconnect all")
            return False

    logger.info("Removing node")


    snode_api = CNodeClient(snode.api_endpoint)
    results, err = snode_api.spdk_process_kill()

    snode.remove(db_controller.kv_store)

    # storage_events.snode_remove(snode)
    logger.info("done")
