 
## Cisco Switch Automation with Netmiko

### Project Overview

The goal of this lab was to use automation to perform configuration on three “day 0” Cisco access switches. These switches were preconfigured with only the essentials: hostnames, SVIs, and the required settings for SSH access.  

The following configurations were automatically applied to each switch via a Python script:  

- Assign VLANs to end host facing interfaces and upstream trunk ports  
- Enable PortFast and BPDU Guard on appropriate interfaces  
- Disable VLAN 1 and unused ports  
- Create an SSH access ACL and apply it to all VTYP lines  
- Add a default gateway per VLAN  

This project was designed to bridge my networking knowledge (CCNA-level concepts) with general Python programming skills and show how automation can streamline configuration.  

I want to preface this by acknowledging the caveats of the project:  

This lab was intentionally simple to keep the focus on the automation script. While real world networks wouldn’t automate such a small setup, the project demonstrates how automation concepts can be applied in a realistic context.   

---

### Tools & Technologies  

- Programming: Python  
- Libraries: Netmiko, JSON  
- Networking: Cisco IOS (switches and router), VLANs, PortFast, BPDU Guard, ACLs  
- Virtualization/Lab: GNS3, VMware Workstation Pro  
- Configuration Template: JSON  

---

### Topology

<img width="1063" height="694" alt="topology" src="https://github.com/user-attachments/assets/9644305e-2f94-4884-8830-bb0b83da3105" />

---

### How It Works  

- The lab network was built in GNS3, running on VMware Workstation Pro.  

- The topology included:  
    - 1 Cisco router  
    - 1 Cisco distribution/core switch  
    - 3 Cisco access switches (with minimal "day 0" configs for SSH)  
    - 1 unmanaged switch  
    - 1 automation PC (running Python + Netmiko)  

The script connects from the automation PC to each access switch by establishing an SSH connection using Netmiko. Once connected, it:  

1. Parses device details (hostname, IP, VLANs, access interfaces, default gateway, etc.) from a JSON file.  
2. Applies configuration changes (VLANs, ACLs, security features) using Netmiko.  
3. Runs show commands to verify the configurations and ensure correctness.  
4. Displays console output in real time so the user can follow the configurations  

In short: the JSON file defines what each switch should look like, and the Python script makes it happen automatically.  

---

### Repo Contents

- `README.md` — Project documentation and instructions  
- `netmiko_cisco_sw_automation.py` — Main automation script  
- `access_switch_info.json` — Configuration parameters per device  
- `requirements.txt` — Required Python dependencies  
- `topology.png` — Diagram of lab topology  
- `network_confs/` — Directory containing initial configs:  
  - `dist_core_sw.txt`  
  - `r1_config.txt`  
  - `s2.txt`  
  - `s3.txt`  
  - `s4.txt` 

---  

### Running the Project  

1. **Clone project repo**  
      ```bash  
      git clone https://github.com/ang725/netmiko_cisco_sw_automation.git  
      cd netmiko_cisco_sw_automation  
      ```  
2. **Install dependencies**  
      ```bash  
      pip install -r requirements.txt  
      ```  
3. **Set up ntc-templates environment variable**  
      ```bash   
      export NET_TEXTFSM='/path/to/ntc-templates/templates'  
      ```  
      Replace '/path/to/ntc-templates/templates' with the actual path after pip installs the repo into your environment.  
4. **Update 'access_switch_conf.json' with your switch details**  
5. **Run the script**  
      ```bash  
      python3 netmiko_cisco_sw_automation.py  
      ```  
---

### Network Reachability  

Note: Your automation host (PC/laptop/server) must have IP connectivity to the switches.  

- If your host is in the **same subnet** as the switch management VLAN than no extra steps are needed.  
- If your host is in a **different subnet**:    
    - Either configure a **default gateway** on your host  
    - Or add **static routes** to reach the switch subnets.  

Example:  
```bash  
sudo ip route add 192.168.100.0/24 via 192.168.1.1
```  

---  

### Why I Built It This Way  

I chose to structure the code in a Python class because:  

- It groups configuration methods specific to an access switch, making the script more organized.  
- It allows reuse of methods if new device types or functions are added later.  
- It reflects how I conceptualize devices as each switch being an “object” with certain attributes.  

Because of the simplicity of the lab, I kept everything in a single file. Breaking the code into separate modules would have been unnecessary and complex at this scale.

---

### Takeaways  

This project was written completely from scratch. No tutorials, just my own approach to solving the lab scenario. I wanted to see how I would structure and execute automation on my own.  

If I were to improve or expand this project, I would focus on:  

- **Error Handling**  
    - My priority was getting the script to work for this specific lab. Better error handling would make it more dynamic and reusable across different scenarios or device types.  
- **Template Usage**  
    - While the script pulls many values from JSON, some items (e.g., ACL names, VLAN names) are hardcoded. In addition, the configuration logic is very access switch specific. More template driven logic would make the script more flexible and reusable in real world environments.  
- **Logging**  
    - Right now, output is printed to the console. Replacing this with structured logging would provide better tracking of changes.  
- **Modularization**  
    - For a small network, one file was fine. But in larger or more complex environments, I’d like to explore splitting the functionality into reusable Python modules.  
