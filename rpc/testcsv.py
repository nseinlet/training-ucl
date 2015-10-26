import openerplib
import threading
import copy 

HOST = "localhost"
PORT = 8069
DB = "ucl"
USER = "admin"
PASS = "admin"

class Activity():
    max_connections = 3
    semaphore = threading.BoundedSemaphore(max_connections)
    lst_thd = []
    
    def read_using_csv(self, connection):
        slicing = 4
        act_model = connection.get_model('epc.activity')
        act_ids = act_model.search([])
        
        activities = []
        
        begin=0
        while begin<len(act_ids):
            acts = act_model.export_data(act_ids[begin:(begin+slicing)], ['id', 'name', 'description'])
            activities += acts['datas']
            begin += slicing
            
        return activities
        
    def _write_csv(self, model, columns, lines):
        sem = self.semaphore.acquire()
        try:
            model.load(columns, lines, context={'tracking_disable': True})
        finally:
            self.semaphore.release()
            
    def update_csv(self, connection, datas):
        act_model = connection.get_model('epc.activity')
        columns = ['id', 'name', 'description']
        slicing = 4
        begin = 0
        while begin<len(datas):
            thd = threading.Thread(target=self._write_csv, args=(act_model, ['id', 'name', 'description'], datas[begin:(begin+slicing)]))
            thd.start()
            self.lst_thd.append(thd)
            begin += slicing
            
        for thd in self.lst_thd:
            thd.join()
        

connection = openerplib.get_connection(hostname=HOST,
                                        port=PORT,
                                        database=DB,
                                        login=USER,
                                        password=PASS,
                                        protocol="jsonrpc",
                                        user_id=1)
connection.check_login(force=False)
act = Activity()
activities = act.read_using_csv(connection)
act_to_write = []
for activity in activities:
    print activity
    act_to_write.append([activity[0], activity[1]+"()", "%s%s" % (activity[2], "EN RPC")])
    
act.update_csv(connection, act_to_write)
    
    
