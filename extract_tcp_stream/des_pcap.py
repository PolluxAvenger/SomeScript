# coding=utf-8

import subprocess


def extract_steam(paap_name):
    try:
        out_bytes = subprocess.check_output(['bash', '/root/PycharmProjects/extrace_stream/extract_stream.sh' , paap_name], shell=True)
    except subprocess.CalledProcessError as e:
        out_bytes = e.output
        code = e.returncode
        print(out_bytes)


if __name__ == "__main__":
    extract_steam('/root/PycharmProjects/extrace_stream/nmap_pic_test.pcap')
