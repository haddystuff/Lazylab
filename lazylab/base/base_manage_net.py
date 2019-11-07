from xml.etree import ElementTree

class BaseManageNet(object):
    def __init__(self, vm, virt_conn):
        self.vm = vm
        self.virt_conn = virt_conn
        
    def create_net(self):
        for interface in  self.vm['interfaces']:
            net_name = self.vm['interfaces'][interface]
            net_root = ElementTree.fromstring(constants.net_xml)
            net_root[0].text = net_name
            domain = next(net_root.iter('domain'))
            domain.set('name', net_name)
            try:
                network = self.virt_conn.networkCreateXML(ElementTree.tostring(net_root, encoding='unicode'))
            except Exception as err:
                continue
            print(net_name)
        return(0)
