# snapshot — shadowsocksr obfs plugin obfs_tls.py — excerpt (manyuser branch)
# source: https://raw.githubusercontent.com/shadowsocksrr/shadowsocksr/manyuser/shadowsocks/obfsplugin/obfs_tls.py
# fetched:2026-09-14
# note: point-in-time capture committed so claims.json can check the quote offline; the gate does not re-fetch it, freshness is not checked.
# repo: https://github.com/shadowsocksrr/shadowsocksr
# excerpt, not executable: file header (copyright), the tls_ticket_auth __init__ and sni() helper,
# client_encode() (record framing + hand-assembled ClientHello) and server_decode()'s record check;
# elided regions are marked with "# …"

#!/usr/bin/env python
#
# Copyright 2015-2015 breakwa11
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# … (verbatim source; elided region marked)
class tls_ticket_auth(plain.plain):
    def __init__(self, method):
        self.method = method
        self.handshake_status = 0
        self.send_buffer = b''
        self.recv_buffer = b''
        self.client_id = b''
        self.max_time_dif = 60 * 60 * 24 # time dif (second) setting
        self.tls_version = b'\x03\x03'
        self.overhead = 5
    def sni(self, url):
        url = common.to_bytes(url)
        data = b"\x00" + struct.pack('>H', len(url)) + url
        data = b"\x00\x00" + struct.pack('>H', len(data) + 2) + struct.pack('>H', len(data)) + data
        return data

    def pack_auth_data(self, client_id):
        utc_time = int(time.time()) & 0xFFFFFFFF
        data = struct.pack('>I', utc_time) + os.urandom(18)
        data += hmac.new(self.server_info.key + client_id, data, hashlib.sha1).digest()[:10]
        return data
    def client_encode(self, buf):
        if self.handshake_status == -1:
            return buf
        if self.handshake_status == 8:
            ret = b''
            while len(buf) > 2048:
                size = min(struct.unpack('>H', os.urandom(2))[0] % 4096 + 100, len(buf))
                ret += b"\x17" + self.tls_version + struct.pack('>H', size) + buf[:size]
                buf = buf[size:]
            if len(buf) > 0:
                ret += b"\x17" + self.tls_version + struct.pack('>H', len(buf)) + buf
            return ret
        if len(buf) > 0:
            self.send_buffer += b"\x17" + self.tls_version + struct.pack('>H', len(buf)) + buf
        if self.handshake_status == 0:
            self.handshake_status = 1
            data = self.tls_version + self.pack_auth_data(self.server_info.data.client_id) + b"\x20" + self.server_info.data.client_id + binascii.unhexlify(b"001cc02bc02fcca9cca8cc14cc13c00ac014c009c013009c0035002f000a" + b"0100")
            ext = binascii.unhexlify(b"ff01000100")
            host = self.server_info.obfs_param or self.server_info.host
            if host and host[-1] in string.digits:
                host = ''
            hosts = host.split(',')
            host = random.choice(hosts)
            ext += self.sni(host)
            ext += b"\x00\x17\x00\x00"
            if host not in self.server_info.data.ticket_buf:
                self.server_info.data.ticket_buf[host] = os.urandom((struct.unpack('>H', os.urandom(2))[0] % 17 + 8) * 16)
            ext += b"\x00\x23" + struct.pack('>H', len(self.server_info.data.ticket_buf[host])) + self.server_info.data.ticket_buf[host]
            ext += binascii.unhexlify(b"000d001600140601060305010503040104030301030302010203")
            ext += binascii.unhexlify(b"000500050100000000")
            ext += binascii.unhexlify(b"00120000")
            ext += binascii.unhexlify(b"75500000")
            ext += binascii.unhexlify(b"000b00020100")
            ext += binascii.unhexlify(b"000a0006000400170018")
            data += struct.pack('>H', len(ext)) + ext
            data = b"\x01\x00" + struct.pack('>H', len(data)) + data
            data = b"\x16\x03\x01" + struct.pack('>H', len(data)) + data
            return data
# … (verbatim source; elided region marked)
    def server_decode(self, buf):
        if self.handshake_status == -1:
            return (buf, True, False)

        if (self.handshake_status & 4) == 4:
            ret = b''
            self.recv_buffer += buf
            while len(self.recv_buffer) > 5:
                if ord(self.recv_buffer[0]) != 0x17 or ord(self.recv_buffer[1]) != 0x3 or ord(self.recv_buffer[2]) != 0x3:
                    logging.info("data = %s" % (binascii.hexlify(self.recv_buffer)))
                    raise Exception('server_decode appdata error')
                size = struct.unpack('>H', self.recv_buffer[3:5])[0]
                if len(self.recv_buffer) < size + 5:
