import paramiko

class Conexao:
    def __init__(self, host, username, password):
        self._host =  host
        self._username = username
        self._password = password

    def list(self):
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self._host, username=self._username, password=self._password)
        _stdin, _stdout,_stderr = client.exec_command("df")
        print(_stdout.read().decode())
        client.close()
        
