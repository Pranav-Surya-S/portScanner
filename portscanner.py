import socket
import time
import sys

try:
    from termcolor import colored
except ImportError:
    colored = None


def log(symbol, msg, color=None):
    text = f"[{symbol}] {msg}"
    if colored and color:
        print(colored(text, color))
    else:
        print(text)


def parse_ports(port_input):
    ports = set()

    if "-" in port_input:
        start, end = port_input.split("-")
        ports.update(range(int(start), int(end) + 1))
    elif "," in port_input:
        for p in port_input.split(","):
            ports.add(int(p.strip()))
    else:
        ports.add(int(port_input))

    valid_ports = sorted(p for p in ports if 1 <= p <= 65535)
    return valid_ports


SCAN_PROFILES = {
    "0": ("Instant", 0),
    "1": ("Fast", 0.005),
    "2": ("Normal", 0.01),
    "3": ("Slow", 0.05),
    "4": ("Slower", 0.1),
}


def scan(target, ports, delay, timeout, close_delay, log_file):
    open_ports = []

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        log("-", f"Cannot resolve {target}", "red")
        return

    log("*", f"Target: {target} ({ip})", "blue")
    log("*", f"Ports: {len(ports)} | Delay: {delay}s | Timeout: {timeout}s | Close delay: {close_delay}s", "blue")

    try:
        for port in ports:
            status, banner = scan_port(ip, port, timeout, close_delay)

            if status == "open":
                open_ports.append(port)
                log("+", f"Port {port} open", "green")
                if banner:
                    log("*", f"Banner: {banner}", "cyan")
                if log_file:
                    log_file.write(f"{ip}:{port} OPEN {banner}\n")

            time.sleep(delay)

    except KeyboardInterrupt:
        log("!", "Scan interrupted by user", "red")

    finally:
        if log_file:
            log_file.flush()

    log("*", f"Scan complete — {len(open_ports)} open ports", "cyan")
    if open_ports:
        log("+", f"Open ports: {', '.join(map(str, open_ports))}", "green")


def scan_port(ip, port, timeout, close_delay):
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))

        banner = None
        try:
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            data = sock.recv(1024)
            if data:
                banner = data.decode(errors="ignore").replace("\r", "").replace("\n", " | ").strip()
        except (socket.timeout, socket.error):
            pass

        time.sleep(close_delay)
        return "open", banner

    except ConnectionRefusedError:
        return "closed", None

    except socket.timeout:
        return "closed", None

    except socket.error:
        return "closed", None

    finally:
        if sock:
            sock.close()


targets = input("[*] Enter targets (comma separated): ").strip()
port_input = input("[*] Enter ports (e.g. 80 | 1-1000 | 22,80,443): ").strip()

ports = parse_ports(port_input)
if not ports:
    log("!", "No valid ports provided", "red")
    sys.exit(1)

delay_choice = input("[*] Scan type: 0=Instant, 1=Fast, 2=Normal, 3=Slow, 4=Slower: ").strip()

delay = SCAN_PROFILES["2"][1]
for key, (name, value) in SCAN_PROFILES.items():
    if delay_choice == key or delay_choice.lower() == name.lower():
        delay = value
        break

timeout_input = input("[*] Socket timeout (default 0.5s): ").strip()
timeout = float(timeout_input) if timeout_input else 0.5

close_delay_input = input("[*] Socket close delay (default 0s): ").strip()
close_delay = float(close_delay_input) if close_delay_input else 0

log_choice = input("[*] Save results to file? (y/N): ").strip().lower()
log_file = None

try:
    if log_choice == "y":
        filename = input("[*] Output file (default scan_results.txt): ").strip()
        log_file = open(filename or "scan_results.txt", "a")

    if "," in targets:
        for t in targets.split(","):
            scan(t.strip(), ports, delay, timeout, close_delay, log_file)
    else:
        scan(targets, ports, delay, timeout, close_delay, log_file)

except KeyboardInterrupt:
    log("!", "Terminated immediately", "red")

finally:
    if log_file:
        log_file.close()
