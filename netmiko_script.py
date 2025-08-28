from netmiko import ConnectHandler
import json

class SwitchAutomaiton:

    def __init__(self, switch):
        """
        Initialize connection to switch.
        """
        self.switch = switch
        self.net_connect = self.connect()
        self.trunk_ports = []
        self.access_ports = self.switch['access_ports']


    def connect(self):
        """
        Establish SSH connection.
        """
        device = {
            "device_type": self.switch["device_type"],
            "host": self.switch["device_ip"]['address'],
            "username": self.switch["username"],
            "password": self.switch["password"],
    }
        return ConnectHandler(**device)


    def update_trunk_vlans(self):
        """
        Add access VLAN to upstream trunk port(s). 
        """
        print(f"Updating upstream trunk port(s)...")
    
        intf_stat = self.net_connect.send_command("show interface status", use_textfsm=True)
        for intf in intf_stat:
            if intf['vlan'] == 'trunk':
                self.trunk_ports.append(intf['port'])
        if not self.trunk_ports:        
            raise Exception(f"ERROR: There are no trunk ports configured on {self.switch['name']}.")
        for trunk in self.trunk_ports:
            cmds = [
                f"interface {trunk}",
                f"switchport trunk allowed vlan add {self.switch['access_vlan']}",
            ]
            self.net_connect.send_config_set(cmds)


    def configure_access_ports(self):
        """
        Configure access VLANS and apply portfast & bpduguard.
        """
        print(f"Configuring access ports...")
        
        cmds = [
            f"interface range {' , '.join(self.access_ports)}",
            "switchport mode access",
            f"switchport access vlan {self.switch['access_vlan']}",
            "spanning-tree portfast",
            "spanning-tree bpduguard enable",
        ]
        self.net_connect.send_config_set(cmds)
    

    def disable_unused_ports(self):
        """
        - Shutdown VLAN 1 switching
        - Move unused ports in UNUSED_PORTS VLAN and shutdown.
        """
        print("Shutting down VLAN 1...")
        self.net_connect.send_config_set([
            "vlan 1",
            "shutdown",
        ])

        intf_stat = self.net_connect.send_command("show interfaces status", use_textfsm=True)
        unused_ports = [
            intf['port'] for intf in intf_stat
            if intf['port'] not in self.trunk_ports
            and intf['port'] not in self.access_ports
        ]

        if not unused_ports: 
            print("ERROR: No ports to be shutdown.")
            return

        print("Shutting down unused ports...")
        cmds = [
            "vlan 888",
            "name UNUSED_PORTS", 
            f"interface range {' , '.join(unused_ports)}",
            "switchport mode access",
            "switchport access vlan 888",
            "shutdown",
        ]
        self.net_connect.send_config_set(cmds)


    def apply_ssh_acl(self):
        """
        Apply ACL to vty lines, restricting SSH access to MANAGEMENT VLAN (SVI).        
        """
        print("Creating and applying SSH access ACL...")
       
        acl_name = f"{self.switch['name']}_SSH_ACCESS"

        cmds = [
            f"ip access-list standard {acl_name}",
            f"permit {self.switch['net_auto_pc']['address']} {self.switch['net_auto_pc']['address']}",
            "line vty 0 4",
            f"access-class {acl_name} in"
        ]
        self.net_connect.send_config_set(cmds)

    
    def add_default_gw(self):
        """
        Apply a default gateway per VLAN.
        """
        print("Adding default gateway...")
        self.net_connect.send_command(f"ip default-gateway {self.switch['default_gateway']['address']}")


    def push_configs(self):
        """
        Run all commands.
        """
        print("**********************************************************************************************************************")
        print(f"{self.switch['name']}\n")
        
        try:
            self.update_trunk_vlans()
            self.configure_access_ports()
            self.disable_unused_ports()
            self.apply_ssh_acl()
            self.add_default_gw()
            print("\nFINISHED")
        except Exception as e:
            print(f"ERROR: Unexpected problem pushing configs to {self.switch['name']}: {e}")


with open("access_switch_info.json") as file:
    switches = json.load(file)

for sw in switches:
    switch = SwitchAutomaiton(sw)
    switch.push_configs()
