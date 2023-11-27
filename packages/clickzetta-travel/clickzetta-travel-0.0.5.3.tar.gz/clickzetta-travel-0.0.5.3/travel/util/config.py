import os
import json
from clickzetta import connect

class Config():
    def __init__(self, conf_file='config.json'):
        if not os.path.exists(conf_file):
            self.create_conf_file(conf_file)
            raise Exception(f'{conf_file} created, resolve all "todo" in it and run again.')

        print(f'read {conf_file}')
        with open(conf_file) as f:
            config = json.load(f)
        # clickzetta
        if 'clickzetta' in config:
            cz_conf = config['clickzetta']
        else:
            cz_conf = config
        self.username = cz_conf['username']
        self.password = cz_conf['password']
        self.instance = cz_conf['instance']
        self.service = cz_conf['service']
        self.workspace = cz_conf['workspace']
        self.schema = cz_conf['schema']
        self.vcluster = cz_conf['vcluster']
        # hints
        if 'hints' in config:
            self.hints = config['hints']
        else:
            self.hints = dict()

    def create_conf_file(self, conf_file):
        ret = input(f'{conf_file} not found, create one? (y/n) ')
        if ret.strip().lower() != 'y':
            raise Exception(f'{conf_file} not found')
        v = 'todo'
        config = {
            'clickzetta': {
                'username': v,
                'password': v,
                'service': v,
                'instance': v,
                'workspace': v,
                'schema': v,
                'vcluster': v,
            },
            'hints': {
                # 'cz.sql.group.by.having.use.alias.first': 'true',
            }
        }
        with open(conf_file, 'w') as f:
            json.dump(config, f, indent=4)

    def get_cz_conn(self):
        conn = connect(username=self.username,
                       password=self.password,
                       service=self.service,
                       instance=self.instance,
                       workspace=self.workspace,
                       schema=self.schema,
                       vcluster=self.vcluster)
        return conn

    def get_hints(self):
        return {'hints': self.hints}
