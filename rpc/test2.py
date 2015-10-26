import openerplib

HOST = "localhost"
PORT = 8069
DB = "ucl"
USER = "admin"
PASS = "admin"

connection = openerplib.get_connection(hostname=HOST,
                                        port=PORT,
                                        database=DB,
                                        login=USER,
                                        password=PASS,
                                        protocol="jsonrpc",
                                        user_id=1)
connection.check_login(force=False)

act_model = connection.get_model('epc.activity')
act_ids = act_model.search([])
activities = act_model.read(act_ids, ['name', 'description'])

for activity in activities:
    print activity
