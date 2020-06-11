from cjdnsadmin.cjdnsadmin import connect
from http.server import HTTPServer, BaseHTTPRequestHandler
import hashlib
import base64
import io
import json

# test:
# curl -H 'Authorization: cjdns 0ytl2njc1hy86tlxtc2zc3449up47uqb0u04kcy233d7zrn2cwh1_cnrbpj2xgspqhzu1l22c306lfsdldz9n5pfj65brp7qd3bg7vvydszxfyt3pby3sfj88ct94rj7vnt6rvldk0y09hddmpj7uk38yq10' -X POST -d 'hello world' http://localhost:8000/
# Content: hello world
# Content hash is: uU0nuZNNPgilLlLX2n2r+sSE7+N6U4DukIj3rOLvzek=
# Authorization: {"error": "none", "ipv6": "fca4:aa4c:3686:6a29:e301:89a5:942c:38d3", "pubkey": "hwnu9u7n8v9u7rjrflhsv45q16p103c1rfx9208hnzr2tq988z90.k", "txid": "T8861LEA1U"}%    

# user@underscore ~ % curl -H 'Authorization: cjdns 0ytl2njc1hy86tlxtc2zc3449up47uqb0u04kcy233d7zrn2cwh1_cnrbpj2xgspqhzu1l22c306lfsdldz9n5pfj65brp7qd3bg7vvydszxfyt3pby3sfj88ct94rj7vnt6rvldk0y09hddmpj7uk38yq10' -X POST -d 'hello worlx' http://localhost:8000/
# Content: hello worlx
# Content hash is: xb1np7VHkEBKv7kWNVbUyu3n5S3R2WMt7b3XhSupvJQ=
# Authorization: {"error": "invalid signature", "txid": "AMXUMLT8MO"}%

class S(BaseHTTPRequestHandler):
    cjdns = connect("127.0.0.1", 11234, "NONE")
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def do_POST(self):
        content = self.rfile.read(int(self.headers['Content-Length']))
        digest = base64.b64encode(hashlib.sha256(content).digest()).decode('utf-8')
        print(content.decode('utf-8'))
        auth = self.headers['Authorization']
        cs = 'unsigned'
        if auth != None and auth.index('cjdns ') == 0:
            sig = auth.replace('cjdns ', '')
            cs = json.dumps(self.cjdns.Sign_checkSig(digest, sig))
            print(cs)
        self._set_headers()
        self.wfile.write(("Content: " + content.decode('utf-8') +
            "\nContent hash is: " + digest + '\nAuthorization: ' + cs).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

run()