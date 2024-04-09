import time
import importlib
import json
from sqlConnector import MySQLConnection 

try:
    import mysql.connector
except ImportError:
    print("\033[91mmysql.connector is not installed. Run 'pip install mysql-connector-python' \033[0m")



class OuterLayer():
    def __init__(self) -> None:
        self.database = MySQLConnection(host='localhost', user='Hybrid_IDPS', password='css2', database='hybrid_idps')
        self.database.setVerbose(False)
        self.database.hazmat_wipe_Table('outerLayerThreats')
        self.devices = {}
        self.threatTable = {
            "portScanning": 0.2,
            "pinging":      0.9,
        }
        self.central_analyzer()

    def central_analyzer(self):
        interval = 1
        start_time = time.time()
        while True:
            if time.time() - start_time >= interval:
                self.database.connect()
                self.add_devices()
                ###### Analyzer Functions ######
                
                self.analyze_port_scanning()
                
                # self.analyze_tcp_flood() #TODO
                
                # self.analyze_udp_flood() #TODO

                # self.analyze_icmp_flood() #TODO

                # self.analyze_ssh_brute_force() #TODO
                
                # self.analyze_log_in()
                
                ###### Analyzer Functions ######
                
                
                self.display_Events_and_calc_threat_level()
                    
                start_time = time.time()
                self.database.disconnect()

    def analyze_port_scanning(self):
        event_type = 'Possible Port Scanning'
        threatName = "Port Scanning"
        
        scanningCountThreshold = 1 #Over 20 its portScanning (tuneable)
        
        results = self.database.execute_query(f"SELECT * from hybrid_idps.outerLayer WHERE event_type = '{event_type}' ORDER BY timestamp DESC")
        results = self.extract_ips(results)
        for ip, all_events in results.items():
            count = 0
            for event in all_events:
                count += 1

                if count > scanningCountThreshold:
                    logName = f"{threatName}-{event['timestamp']}"
                    # self.add_threat(ip, logName, all_events[:1])
                    self.add_threat(ip, logName, event['geolocation'], event['timestamp'], threatName)
                    count = 0

    def analyze_tcp_flood(self):
        event_types = ['Possible SYN Flood', 'Possible ACK Flood', 'Possible RST Flood', 'Possible FIN Flood']
        threatName = "TCP Flood Attack"
        
        scanningCountThreshold = 1 #Over 20 its portScanning (tuneable)
        
        for event_type in event_types:
            results = self.database.execute_query(f"SELECT * from hybrid_idps.outerLayer WHERE event_type = '{event_type}' ORDER BY timestamp DESC")
            results = self.extract_ips(results)
            for ip, all_events in results.items():
                count = 0
                for event in all_events:
                    count += 1

                    if count > scanningCountThreshold:
                        logName = f"{threatName}-{event['timestamp']}"
                        # self.add_threat(ip, logName, all_events[:1])
                        self.add_threat(ip, logName, event['geolocation'], event['timestamp'], threatName)
                        count = 0

    def analyze_udp_flood(self):
        event_type = 'Possible UDP Flood'
        threatName = "UDP Flood Attack"
        
        scanningCountThreshold = 1 #Over 20 its portScanning (tuneable)
        
        results = self.database.execute_query(f"SELECT * from hybrid_idps.outerLayer WHERE event_type = '{event_type}' ORDER BY timestamp DESC")
        results = self.extract_ips(results)
        for ip, all_events in results.items():
            count = 0
            for event in all_events:
                count += 1

                if count > scanningCountThreshold:
                    logName = f"{threatName}-{event['timestamp']}"
                    # self.add_threat(ip, logName, all_events[:1])
                    self.add_threat(ip, logName, event['geolocation'], event['timestamp'], threatName)
                    count = 0

    def analyze_icmp_flood(self):
        event_type = 'Possible ICMP Flood'
        threatName = "ICMP Flood Attack"
        
        scanningCountThreshold = 1 #Over 20 its portScanning (tuneable)
        
        results = self.database.execute_query(f"SELECT * from hybrid_idps.outerLayer WHERE event_type = '{event_type}' ORDER BY timestamp DESC")
        results = self.extract_ips(results)
        for ip, all_events in results.items():
            count = 0
            for event in all_events:
                count += 1

                if count > scanningCountThreshold:
                    logName = f"{threatName}-{event['timestamp']}"
                    # self.add_threat(ip, logName, all_events[:1])
                    self.add_threat(ip, logName, event['geolocation'], event['timestamp'], threatName)
                    count = 0

    def analyze_ssh_brute_force(self):
        event_type = 'Possible SSH Brute Force'
        threatName = "SSH Brute Force Attack"
        
        scanningCountThreshold = 1 #Over 20 its portScanning (tuneable)
        
        results = self.database.execute_query(f"SELECT * from hybrid_idps.outerLayer WHERE event_type = '{event_type}' ORDER BY timestamp DESC")
        results = self.extract_ips(results)
        for ip, all_events in results.items():
            count = 0
            for event in all_events:
                count += 1

                if count > scanningCountThreshold:
                    logName = f"{threatName}-{event['timestamp']}"
                    # self.add_threat(ip, logName, all_events[:1])
                    self.add_threat(ip, logName, event['geolocation'], event['timestamp'], threatName)
                    count = 0 
    
    def analyze_log_in(self):
        event_type = 'invalidCredentials'
        threatName = "bruteForce"
        
        results = self.database.execute_query(f"SELECT * from hybrid_idps.outerLayer WHERE event_type = '{event_type}' ORDER BY timestamp DESC")
        results = self.extract_ips(results)
        for ip, all_events in results.items():
            count = 0
            for event in all_events:
                count += 1
                if count > 10:
                    logName = f"{threatName}-{event['timestamp']}"
                    # self.add_threat(ip, logName, all_events[:1])
                    self.add_threat(ip, logName, event['geolocation'], event['timestamp'], threatName)
                    count = 0

    def display_Events_and_calc_threat_level(self):
        for ip, deviceData in self.devices.items():
            print("\n")
            print(f"IP: {ip}")
            logs = deviceData["logs"]
            threatLevel = 0
            for threatName, threadType in logs.items():
                print(f"        {threatName}")
                threatLevel += self.threatTable[threadType]
                
            if threatLevel > 1: threatLevel = 1
            self.set_threat_level(ip, threatLevel)
            color_code = "\033[92m"  # Green
            if threatLevel > 0.5:
                color_code = "\033[91m"  # Red
            elif 0 < threatLevel < 0.5:
                color_code = "\033[93m"  # Yellow
            reset_color = "\033[0m"
            print(f"    {color_code}[Threat Level]:   {threatLevel} {reset_color}")
            
    def extract_ips(self, results):
        ip_dict = {}
        for entry in results:
            ip = entry['ip_address']
            if ip not in ip_dict:
                ip_dict[ip] = []
            ip_dict[ip].append(entry)
        return ip_dict

    def add_devices(self):
        results = self.database.execute_query(f"SELECT DISTINCT ip_address from hybrid_idps.outerLayer")
        ip_addresses = [ip['ip_address'] for ip in results]
        for ip in ip_addresses:
            if ip not in self.devices:
                self.devices[ip] = {'threatLevel': 0, 'logs': {}}
                
    def add_threat(self, ip_address, logName, geolocation, timestamp, threatName):
        if ip_address in self.devices:
            device = self.devices[ip_address]
            threatLevel = self.threatTable[threatName]
            
            if logName not in device['logs']:
                print('adds')
                print(device['logs'])
                device['logs'][logName] = threatName
                self.database.add_threat_to_outer_Layer_Threats_DB(ip_address, logName, geolocation, timestamp, threatName, threatLevel)
            
        else:
            print(f"Device with IP address {ip_address} does not exist.")
            
    def set_threat_level(self, ip_address, newThreatLevel):
        if ip_address in self.devices:
            device = self.devices[ip_address]['threatLevel'] = newThreatLevel
        else:
            print(f"Device with IP address {ip_address} does not exist.")

if __name__ == "__main__":
    x = OuterLayer()

        
            