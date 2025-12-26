# Python Port Scanner

A lightweight, simple python port scanner that scans the ports of the specified ip address.

> [!IMPORTANT] 
> **Legal Disclaimer**: This tool is for **educational and authorized testing purposes only**. Scanning networks, servers, or devices that you do not own or do not have explicit permission to test is illegal. The author accepts no responsibility for unauthorized use.

---

## Features

- **TCP Connect Scan**: Reliable port discovery.
- **Banner Grabbing**: Attempts to fetch service headers (HTTP-style).
- **Speed Profiles**: 5 distinct scan modes ranging from Instant to Slower (stealthier).
- **Flexible Inputs**: Supports single IPs, hostnames, single ports, port lists, and ranges.
- **Logging**: Optional result saving to file.
- **Visuals**: Clean CLI output with optional color support.
- **Safety**: Graceful shutdown support via `Ctrl+C`.

---

## Requirements

- **Python 3.8+**
- **Dependencies**: Standard library only by default.
  - _(Optional)_ `termcolor` for colored terminal output.

---

## Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/Pranav-Surya-S/portScanner
    cd portScanner
    ```

2.  **Install optional dependencies**
    If you want colored output, install the suggested package:
    ```bash
    pip install termcolor
    ```

---

## Usage

Run the script directly using Python:

```bash
python portscanner.py
```

## Example input

```YAML
Targets: 192.168.1.10, scanme.nmap.org
Ports: 22,80,443,1000-2000
Scan type: 0=Instant, 1=Fast, 2=Normal, 3=Slow, 4=Slower: 0
Timeout: 0.5
Save results: y
```

### Input Formats

- **Targets**: Accepts IPv4 addresses or Domain names. Multiple targets can be separated by commas.
- **Ports:** Accepts three formats:
  - Single port: 80
  - List: 22,80,443
  - Range: 1-1024
- **Scan type**: 0=Instant, 1=Fast, 2=Normal, 3=Slow, 4=Slower:

| Mode    | Delay  |
| ------- | ------ |
| Instant | 0s     |
| Fast    | 0.005s |
| Normal  | 0.01s  |
| Slow    | 0.05s  |
| Slower  | 0.1s   |

- **Socket timeout**: (default 0.5s)
- **Socket close delay**: (default 0s)

> [!NOTE]
> Banner grabbing is may not work due to many modern services not responding to this specific payload or blocking the request entirely.

> [!WARNING]
> Firewalls & IDS: Aggressive scanning (Instant/Fast modes) or scanning many ports at once may trigger Intrusion Detection Systems (IDS)
