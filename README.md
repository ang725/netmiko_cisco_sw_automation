 
## Cisco Switch Automation with Netmiko

### Project Overview

The goal of this lab was to use automation to perform initial configuration on three “day 0” Cisco access switches. These switches were preconfigured with only the essentials: hostnames, SVIs, and the required settings for SSH access.  

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

<img width="925" height="649" alt="topology" src="https://github.com/user-attachments/assets/6b657658-42b9-431b-b013-849c64a0e69d" />

----

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

### Running the Project  

1. **Clone project repo**  
      ```bash  
      git clone https://github.com/ang725/netmiko_cisco_sw_automation.git  
      cd your-repo-name  
      ```  
2. **Clone ntc-templates repo & set environment variable**  
      ```bash  
      git clone https://github.com/networktocode/ntc-templates.git  
      export NET_TEXTFSM='/path/to/ntc-templates/templates'  
      ```  
3. **Install dependencies**  
      ```bash  
      pip install netmiko  
      ```  
4. **Update 'access_switch_conf.json' with your switch details**  
5. **Run the script**  
      ```bash  
      python3 netmiko_script.py  
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
