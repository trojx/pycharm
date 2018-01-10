import socket

def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8001))
    s.listen(1500)
    while 1:
        conn, addr = s.accept()
        print(addr)
        headers = ''
        while 1:
            buf = conn.recv(2048).decode('utf-8')
            headers += buf
            if len(buf) < 2048:
                break

        headers = headers.replace('127.0.0.1:8001', 'idea.imsxm.com')
                         #.replace('keep-alive', 'close')
                         #.replace('gzip','')
        print(headers)
        s1 = socket.socket()
        s1.connect(('idea.imsxm.com', 80))
        s1.sendall(headers.encode())

        resp = b''
        cnt = 2
        while cnt:
            print '.......', cnt 
            cnt -= 1
            try:
                buf = s1.recv(1024*8)
            except socket.timeout as e:
                print(e)
                break
                
            resp += buf
            if not buf or\
               buf.startswith(b'WebSocket') and buf.endswith(b'\r\n\r\n'):
                break

        #resp = resp.replace(b'Content-Encoding: gzip\r\n', b'')\
        resp =           resp.replace(b'idea.imsxm.com', b'127.0.0.1:8001')
        print resp
        print addr
        conn.sendall(resp)
        conn.close()


main()

