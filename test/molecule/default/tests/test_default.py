import os
import requests

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_nginx(host):
    assert host.service("nginx").is_running
    assert host.service("nginx").is_enabled
    assert host.socket("tcp://0.0.0.0:80").is_listening
# domain =  host.ansible("debug", "var=external_domain")['external_domain']
    response = requests.get("http://localhost")
    assert response.status_code == 200
    assert response.headers['Server'] != "nginx"
    check_syntax = host.run("nginx -t")
    assert check_syntax.rc == 0
