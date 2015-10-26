import xmlrpclib

HOST = "localhost"
PORT = 8069
DB = "ucl"
USER = "admin"
PASS = "admin"

root = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

uid = xmlrpclib.ServerProxy(root + 'common').login(DB, USER, PASS)
print "Logged in as %s (uid: %d)" % (USER, uid)

# Create a new note
sock = xmlrpclib.ServerProxy(root + 'object')
args = {
    'name' : "Cree par RPC",
    'description' : 'Use XML RPC',
    'create_uid': uid,
}
note_id = sock.execute(DB, uid, PASS, 'epc.activity', 'create', args)
