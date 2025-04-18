from wakeonlan import send_magic_packet
import nmap
    
def list_uphosts(ip_range: str):
    scanner = nmap.PortScanner()
    scan_results = scanner.scan(hosts=ip_range, arguments="-sn")['nmap']
    uphosts = scan_results['scan'].keys()
    return uphosts

def is_ip_address_online(ip_address: str):
    scanner = nmap.PortScanner()
    scan_results = scanner.scan(hosts=ip_address, arguments="-sn")['nmap']
    return scan_results['scanstats']['uphosts'] > 0

def wake_host(mac_address):
    send_magic_packet(mac_address)