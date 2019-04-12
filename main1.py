#author：(李志鹏)Frank Lee
#2019 年4 月12日

#!/usr/bin/python
# virsh list
import collections
from lxml import etree
import json
import threading
import sql
import time
from datetime import datetime

libvirt = None
libvirt_type = 'kvm'
libvirt_uri = ''
Instance = collections.namedtuple('Instance', ['name', 'UUID', 'state'])
CPUStats = collections.namedtuple('CPUStats', ['number', 'util'])
Interface = collections.namedtuple('Interface', ['name', 'mac',
                                                 'fref', 'parameters'])
InterfaceStats = collections.namedtuple('InterfaceStats',
                                        ['rx_bytes', 'rx_packets',
                                         'tx_bytes', 'tx_packets'])
Disk = collections.namedtuple('Disk', ['device'])
DiskStats = collections.namedtuple('DiskStats',
                                   ['read_bytes', 'read_requests',
                                    'write_bytes', 'write_requests',
                                    'errors'])
DiskSize = collections.namedtuple('DiskSize', ['total', 'allocation', 'physical'])
Memory = collections.namedtuple('Memory', ['total', 'used', 'util'])


class InspectorException(Exception):
    def __init__(self, message=None):
        super(InspectorException, self).__init__(message)


class InstanceNotFoundException(InspectorException):
    pass


class LibvirtInspector():
    per_type_uris = dict(uml='uml:///system', xen='xen:///', lxc='lxc:///')

    def __init__(self):
        self.uri = self._get_uri()
        self.connection = None

    def _get_uri(self):
        return libvirt_uri or self.per_type_uris.get(libvirt_type,
                                                     'qemu:///system')

    def _get_connection(self):
        if not self.connection or not self._test_connection():
            global libvirt
            if libvirt is None:
                libvirt = __import__('libvirt')
            # LOG.debug('Connecting to libvirt: %s', self.uri)
            self.connection = libvirt.open(self.uri)
        return self.connection

    def _test_connection(self):
        try:
            self.connection.getCapabilities()
            return True
        except libvirt.libvirtError as e:
            if (e.get_error_code() == libvirt.VIR_ERR_SYSTEM_ERROR and
                    e.get_error_domain() in (libvirt.VIR_FROM_REMOTE,
                                             libvirt.VIR_FROM_RPC)):
                # LOG.debug('Connection to libvirt broke')
                return False
            raise

    def _lookup_by_name(self, instance_name):
        try:
            return self._get_connection().lookupByName(instance_name)
        except Exception as ex:
            if not libvirt or not isinstance(ex, libvirt.libvirtError):
                raise InspectorException(unicode(ex))
            error_code = ex.get_error_code()
            msg = ("Error from libvirt while looking up %(instance_name)s: "
                   "[Error Code %(error_code)s] "
                   "%(ex)s" % {'instance_name': instance_name,
                               'error_code': error_code,
                               'ex': ex})
            raise InstanceNotFoundException(msg)

    def inspect_instances(self):
        if self._get_connection().numOfDomains() > 0:
            for domain_id in self._get_connection().listDomainsID():
                try:
                    # We skip domains with ID 0 (hypervisors).
                    if domain_id != 0:
                        domain = self._get_connection().lookupByID(domain_id)
                        state = domain.state(0)[0]
                        if state != 1:
                            state = 0
                        yield Instance(name=domain.name(),
                                       UUID=domain.UUIDString(), state=state)
                except libvirt.libvirtError:
                    # Instance was deleted while listing... ignore it
                    pass

    # shut off instances
    def inspect_defined_domains(self):
        if self._get_connection().numOfDomains() > 0:
            for instance_name in self._get_connection().listDefinedDomains():
                domain = self._lookup_by_name(instance_name)
                state = domain.state(0)[0]
                if state != 1:
                    state = 0
                yield Instance(name=instance_name,
                               UUID=domain.UUIDString(), state=state)

    def inspect_disk_info_for_down(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        # mem_total = domain.info()[1]
        tree = etree.fromstring(domain.XMLDesc(0))
        for device in filter(
                bool,
                [target.get("dev")
                 for target in tree.findall('devices/disk/target')]):
            disk = Disk(device=device)
            try:
                disk_size = domain.blockInfo(device, 0)
            except libvirt.libvirtError:
                disk_size = [0, 0, 0]
                pass
            size = DiskSize(total=disk_size[0] / (1024 * 1024), allocation=disk_size[1] / (1024 * 1024),
                            physical=disk_size[2] / (1024 * 1024))
            yield (disk, size)

    def inspect_vnics_info_for_down(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        tree = etree.fromstring(domain.XMLDesc(0))
        for iface in tree.findall('devices/interface'):
            target = iface.find('target')
            if target is not None:
                name = target.get('dev')
            else:
                continue
            mac = iface.find('mac')
            if mac is not None:
                mac_address = mac.get('address')
            else:
                continue
            fref = iface.find('filterref')
            if fref is not None:
                fref = fref.get('filter')
            params = dict((p.get('name').lower(), p.get('value'))
                          for p in iface.findall('filterref/parameter'))
            yield Interface(name=name, mac=mac_address,
                            fref=fref, parameters=params)

    def inspect_mem_info_for_down(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        mem_total = domain.info()[1]
        return mem_total

    def inspect_cpus(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        try:
            (_, _, _, num_cpu, cpu_time_start) = domain.info()
            import time
            real_time_start = time.time()
            time.sleep(1)
            (_, _, _, _, cpu_time_end) = domain.info()
            real_time_end = time.time()
            real_diff_time = real_time_end - real_time_start
            util = 100 * (cpu_time_end - cpu_time_start) / (float)(num_cpu * real_diff_time * 1000000000)
            if util > 100:
                util = 100.0
            if util < 0:
                util = 0.0
            return CPUStats(number=num_cpu, util=str(util))
        except libvirt.libvirtError:
            pass

    def inspect_memory(self, instance_name):
        try:
            domain = self._lookup_by_name(instance_name)
            domain.setMemoryStatsPeriod(5)
            meminfo = domain.memoryStats()
            free_mem = float(meminfo['unused'])
            total_mem = float(meminfo['available'])
            util = ((total_mem - free_mem) / total_mem) * 100
            return Memory(total=total_mem, used=total_mem - free_mem, util=util)
        except:
            pass
        try:
            domain = self._lookup_by_name(instance_name)
            actual = float(domain.memoryStats()['actual'])
            rss = float(domain.memoryStats()['rss'])
            rss = rss - 150000
            if rss >= actual:
               rss = rss - 250000
            if rss <= 0:
               rss = rss + 150000
               # util = str(int((rss / actual)*100))
               util = (rss / actual) * 100
               # import decimal
               # util = decimal.Decimal(str(round(util, 0)))
            return Memory(total=actual, used=rss, util=util)
        except libvirt.libvirtError:
            pass

    def inspect_vnics(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        tree = etree.fromstring(domain.XMLDesc(0))
        for iface in tree.findall('devices/interface'):
            target = iface.find('target')
            if target is not None:
                name = target.get('dev')
            else:
                continue
            mac = iface.find('mac')
            if mac is not None:
                mac_address = mac.get('address')
            else:
                continue
            fref = iface.find('filterref')
            if fref is not None:
                fref = fref.get('filter')
            params = dict((p.get('name').lower(), p.get('value'))
                          for p in iface.findall('filterref/parameter'))
            interface = Interface(name=name, mac=mac_address,
                                  fref=fref, parameters=params)
            try:
                rx_bytes, rx_packets, _, _, \
                tx_bytes, tx_packets, _, _ = domain.interfaceStats(name)
                stats = InterfaceStats(rx_bytes=rx_bytes,
                                       rx_packets=rx_packets,
                                       tx_bytes=tx_bytes,
                                       tx_packets=tx_packets)
                yield (interface, stats)
            except libvirt.libvirtError:
                pass

    def inspect_disks(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        tree = etree.fromstring(domain.XMLDesc(0))
        for device in filter(
                bool,
                [target.get("dev")
                 for target in tree.findall('devices/disk/target')]):
            disk = Disk(device=device)
            block_stats = domain.blockStats(device)
            stats = DiskStats(read_requests=block_stats[0],
                              read_bytes=block_stats[1],
                              write_requests=block_stats[2],
                              write_bytes=block_stats[3],
                              errors=block_stats[4])
            try:
                disk_size = domain.blockInfo(device, 0)
            except libvirt.libvirtError:
                disk_size = [0, 0, 0]
                pass
            size = DiskSize(total=disk_size[0] / (1024 * 1024), allocation=disk_size[1] / (1024 * 1024),
                            physical=disk_size[2] / (1024 * 1024))
            yield (disk, stats, size)


def output():
    libvirtInspector = LibvirtInspector()
    instances = libvirtInspector.inspect_instances()
    not_running_instances = libvirtInspector.inspect_defined_domains()
    list = []
    for instance in not_running_instances:
        dict = {}
        dict['vmid'] = instance.UUID
        dict['domain_name'] = instance.name
        dict['state'] = instance.state
        cpus = libvirtInspector.inspect_cpus(instance.name)
        dict['cpu'] = cpus.number
        dict['cpu_usage'] = cpus.util
        dict['memory_total'] = libvirtInspector.inspect_mem_info_for_down(instance.name)
        dict['memory_used'] = ""
        dict['memory_usage'] = ""
        dict['current_time']=datetime.time()

        # get the nic infomation
        nicList = []
        nicdict = {'nic_name': '', 'mac': '', 'ip': '', 'net_send_read': '', 'net_receive_write': '',
                   'net_send_request': '', 'net_receive_reques': ''}
        nicList.append(nicdict)
        dict['nics'] = nicList
        # get the disk infomation
        disks = libvirtInspector.inspect_disk_info_for_down(instance.name)
        diskList = []
        for disk in disks:
            diskdict = {}
            diskdict['device'] = disk[0].device
            diskdict['total_size'] = disk[1].total
            diskdict['used_size'] = disk[1].physical
            diskdict['disk_read'] = ""
            diskdict['disk_write'] = ""
            diskdict['disk_read_request'] = ""
            diskdict['disk_write_request'] = ""
            diskList.append(diskdict)
        dict['disks'] = diskList
        list.append(dict)
    for instance in instances:
        memory = libvirtInspector.inspect_memory(instance.name)
        dict = {}
        dict['current_time']=time.asctime( time.localtime(time.time()) )
        dict['vmid'] = instance.UUID
        dict['domain_name'] = instance.name
        dict['state'] = instance.state
        cpus = libvirtInspector.inspect_cpus(instance.name)
        dict['cpu'] = cpus.number
        dict['cpu_usage'] = cpus.util
        dict['memory_total'] = memory.total
        dict['memory_used'] = memory.used
        dict['memory_usage'] = memory.util
        # get the nic infomation
        nics = libvirtInspector.inspect_vnics(instance.name)
        nicList = []
        for nic in nics:
            nicdict = {}
            nicdict['nic_name'] = nic[0].name
            nicdict['mac'] = nic[0].mac
            nicdict['ip'] = nic[0].parameters.get('ip', '')
            nicdict['net_send_read'] = nic[1].tx_bytes
            nicdict['net_receive_write'] = nic[1].rx_bytes
            nicdict['net_send_request'] = nic[1].tx_packets
            nicdict['net_receive_reques'] = nic[1].rx_packets
            nicList.append(nicdict)
        dict['nics'] = nicList
        # get the disk infomation
        disks = libvirtInspector.inspect_disks(instance.name)
        diskList = []
        for disk in disks:
            diskdict = {}
            diskdict['device'] = disk[0].device
            diskdict['total_size'] = disk[2].total
            diskdict['used_size'] = disk[2].physical
            diskdict['disk_read'] = disk[1].read_bytes
            diskdict['disk_write'] = disk[1].write_bytes
            diskdict['disk_read_request'] = disk[1].read_requests
            diskdict['disk_write_request'] = disk[1].write_requests
            diskList.append(diskdict)
        dict['disks'] = diskList
        list.append(dict)
    f = open("vm_monitor.json", "wr")
    try:
        # json.dump(list, f, indent=2)
        # f.flush()
        # print list[0]
        print "##########"
        # print f
        sql.collection.insert(list[0])
    finally:
        f.close()
        # print list
    # print list
    global t
    t=threading.Timer(10,output)
    t.start()


def main():
    output()


if __name__ == "__main__":
    # for i in  range(10):
    #       main()
    #       time.sleep(10)
    #       print sql.collection.find()
      main()