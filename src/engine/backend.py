import logging
import socket
import psutil

from scapy.interfaces import get_working_ifaces
from scapy.interfaces import NetworkInterface

from src.consts.enums import ConnectionError
from src.consts.logger import LOGGING_NAME
from src.consts.connectivity_test_hosts import CONNECTIVITY_HOSTS, CONNECTIVITY_TEST_PORT, CONNECTION_TIMEOUT


# Game protocol signatures for packet filtering
PROTOCOL_SIGNATURES = {
    "json_start": "{",  # JSON format packets
    "special_start": "x",  # Special format packets
    "min_length": 30,  # Minimum packet length
    "excluded_keys": ["inventory_charms", "steam"],  # Keys to exclude
}


class Backend:

    @staticmethod
    def get_open_connections_from_process() -> set:
        pid: int = 0
        hs_ips = set()
        for proccess in psutil.process_iter(["pid", "name"]):
            if proccess.info["name"] == "Hero_Siege.exe":
                pid = proccess.info["pid"]

        if pid != 0:
            try:
                connections = psutil.net_connections(kind="inet")
                for connection in connections:
                    if connection.pid == pid and hasattr(connection, 'raddr') and connection.raddr and connection.raddr.ip:
                        hs_ips.add(connection.raddr.ip)
            except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
                logging.getLogger(LOGGING_NAME).warning(f"Could not access network connections: {e}")
        return hs_ips

    @staticmethod
    def get_packet_filter() -> str:
        """
        Generate BPF filter based on protocol signatures
        Returns: BPF filter string
        """
        # Filter for TCP packets with minimum length
        base_filter = f"tcp and len > {PROTOCOL_SIGNATURES['min_length']}"

        # Filter for JSON format packets (starting with '{')
        json_filter = f"tcp[((tcp[12:1] & 0xf0) >> 2):1] = 0x{ord(PROTOCOL_SIGNATURES['json_start']):02x}"

        # Filter for special format packets (starting with 'x')
        special_filter = f"tcp[((tcp[12:1] & 0xf0) >> 2):1] = 0x{ord(PROTOCOL_SIGNATURES['special_start']):02x}"

        hs_ips = Backend.get_open_connections_from_process()
        if not hs_ips:
            ip_filter_string = "len < 0"
        else:
            ip_filter_string = f"(host {' or host '.join(hs_ips)}) and len > 30"
        # following filter line commented out because there seems to be a flaw because no package is actually getting through
        # return f"({base_filter}) and ({json_filter} or {special_filter})"
        return ip_filter_string

    @staticmethod
    def get_interfaces() -> list[NetworkInterface]:
        try:
            interfaces = get_working_ifaces()
            return interfaces if interfaces else []
        except Exception as e:
            logging.getLogger(LOGGING_NAME).error(f"Error getting interfaces: {e}")
            return []

    @staticmethod
    def check_internet_connection() -> str | None:
        logger = logging.getLogger(LOGGING_NAME)
        for CONNECTIVITY_TEST_HOST in CONNECTIVITY_HOSTS:
            try:
                with socket.create_connection(
                    (CONNECTIVITY_TEST_HOST, CONNECTIVITY_TEST_PORT), timeout=CONNECTION_TIMEOUT
                ) as s:
                    connection_iface_ip = s.getsockname()[0]
                    return connection_iface_ip
            except (TimeoutError, socket.gaierror) as e:
                logger.info(f"Could not check connection to: {CONNECTIVITY_TEST_HOST}")
                pass
            except Exception as e:
                logger.error(f"Unknown error: {e}")
        logger.error(f"Internet connection check failed")
        return None

    @staticmethod
    def _is_valid_physical_interface(interface) -> bool:
        """
        Check if interface is a valid physical interface
        
        Args:
            interface: NetworkInterface object to validate
        
        Returns:
            bool: True if interface is valid, False otherwise
        """
        try:
            # Check if interface has flags attribute
            if not hasattr(interface, 'flags'):
                return False
            
            flags = interface.flags
            
            # Handle different flag types safely
            flags_str = None
            
            if isinstance(flags, (str, bytes)):
                flags_str = flags if isinstance(flags, str) else flags.decode('utf-8', errors='ignore')
            elif isinstance(flags, list):
                # If flags is a list of strings, join them
                flags_str = ' '.join(str(flag) for flag in flags)
            elif isinstance(flags, int):
                # Flag is an integer (bitmask) - convert to string representation
                # Common flags: 1=UP, 2=BROADCAST, 4=LOOPBACK, 8=POINTOPOINT, 16=RUNNING
                # For our purposes, treat as valid if it has UP and RUNNING bits
                has_up = bool(flags & 0x1)      # Bit 0: UP flag
                has_running = bool(flags & 0x10)  # Bit 4: RUNNING flag
                return has_up and has_running
            else:
                # Convert other types to string safely
                flags_str = str(flags)
            
            # For string-based flags, check for required keywords
            if flags_str:
                flags_upper = flags_str.upper()
                return "OK" in flags_upper and "UP" in flags_upper and "RUNNING" in flags_upper
            
            return False
            
        except (TypeError, AttributeError, ValueError) as e:
            logging.getLogger(LOGGING_NAME).debug(f"Error validating interface: {e}")
            return False

    @staticmethod
    def _get_interface_flags_string(interface) -> str:
        """
        Safely extract flags from interface as string
        """
        try:
            if not hasattr(interface, 'flags'):
                return ""
            
            flags = interface.flags
            
            if isinstance(flags, (str, bytes)):
                return flags if isinstance(flags, str) else flags.decode('utf-8', errors='ignore')
            elif isinstance(flags, list):
                return ' '.join(str(flag) for flag in flags)
            elif isinstance(flags, int):
                # Convert integer flags to meaningful string representation
                flag_parts = []
                if flags & 0x1:
                    flag_parts.append("UP")
                if flags & 0x2:
                    flag_parts.append("BROADCAST")
                if flags & 0x4:
                    flag_parts.append("LOOPBACK")
                if flags & 0x8:
                    flag_parts.append("POINTOPOINT")
                if flags & 0x10:
                    flag_parts.append("RUNNING")
                if flags & 0x20:
                    flag_parts.append("NOARP")
                if flags & 0x40:
                    flag_parts.append("PROMISC")
                if flags & 0x80:
                    flag_parts.append("ALLMULTI")
                if flags & 0x100:
                    flag_parts.append("MASTER")
                if flags & 0x200:
                    flag_parts.append("SLAVE")
                if flags & 0x400:
                    flag_parts.append("MULTICAST")
                if flags & 0x800:
                    flag_parts.append("PORTSEL")
                if flags & 0x1000:
                    flag_parts.append("AUTOMEDIA")
                if flags & 0x2000:
                    flag_parts.append("DYNAMIC")
                
                return ' '.join(flag_parts) if flag_parts else str(flags)
            else:
                return str(flags)
        except Exception:
            return ""

    @staticmethod
    def get_connection_interface() -> str | ConnectionError:
        logger = logging.getLogger(LOGGING_NAME)
        connection_iface_ip = Backend.check_internet_connection()

        if connection_iface_ip is None:
            logger.warning("No internet connection detected")
            return ConnectionError.NoInternet

        interfaces = Backend.get_interfaces()
        
        if not interfaces:
            logger.error("No network interfaces found")
            return ConnectionError.InterfaceNotFound

        # Try to find matching physical interface
        for interface in interfaces:
            try:
                if (Backend._is_valid_physical_interface(interface) 
                    and hasattr(interface, 'ip') 
                    and interface.ip == connection_iface_ip):
                    logger.info(f"Found matching physical interface: {interface.description if hasattr(interface, 'description') else interface.name}")
                    return interface.description if hasattr(interface, 'description') else interface.name
            except Exception as e:
                logger.debug(f"Error checking interface: {e}")
                continue

        # Try to find any available physical interface
        for interface in interfaces:
            try:
                if Backend._is_valid_physical_interface(interface):
                    logger.info(f"Using available physical interface: {interface.description if hasattr(interface, 'description') else interface.name}")
                    return interface.description if hasattr(interface, 'description') else interface.name
            except Exception as e:
                logger.debug(f"Error checking interface: {e}")
                continue

        # Fallback to any working interface
        for interface in interfaces:
            try:
                flags_str = Backend._get_interface_flags_string(interface)
                has_ok = "OK" in flags_str if flags_str else False
                has_up = "UP" in flags_str if flags_str else False
                has_ip = hasattr(interface, 'ip') and interface.ip
                
                if has_ok and has_up and has_ip:
                    logger.warning(f"Falling back to available interface: {interface.description if hasattr(interface, 'description') else interface.name}")
                    return interface.description if hasattr(interface, 'description') else interface.name
            except Exception as e:
                logger.debug(f"Error checking interface fallback: {e}")
                continue

        logger.error("No suitable network interface found")
        return ConnectionError.InterfaceNotFound