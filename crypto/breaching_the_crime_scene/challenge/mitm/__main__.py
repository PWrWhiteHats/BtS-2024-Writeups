import pyshark

app1_port = 5000
app2_port = 5001

banner = f""\
f"-------------------------\n"\
f"|  MITM Packet Sniffer  |\n"\
f"-------------------------\n"\
f"v1.2\n"\
f"ONLY FOR AUTHORIZED USE\n"\
f"\nSniffing traffic between forum.silly.net and images.silly.net...\n"\
f"Reporting packets for ports {app1_port},{app2_port}...\n"\
f"Starting sniffer..."

def main():
    print(banner, flush=True)
    capture = pyshark.LiveCapture("lo", bpf_filter=f'(port {app1_port} or port {app2_port})')
    counter = 0;

    def on_packet(packet):
        if 'TLS' in packet:
            nonlocal counter
            counter += 1
            print(f'[{counter}] TLS packet:',)
            print(f'{packet["ip"].src}:{packet["tcp"].srcport} -> '\
                  f'{packet["ip"].dst}:{packet["tcp"].dstport}\n'\
                  f'{packet["TLS"]._all_fields}\n',)
    
    capture.apply_on_packets(on_packet)

main()