task_conf = """
    server {{ # {task_name}
        server_name {task_name}.ctf.sicamp.ru;
        proxy_pass http://localhost:{port}
    }}"""
conf = """
server {{
    listen 443 ssl;
    ssl_certificate /root/ctf.sicamp.ru/cert.pem;
    ssl_certificate_key /root/ctf.sicamp.ru/privkey.pem;
    server {{
        server_name ctf.sicamp.ru;
        proxy_pass http://localhost:8000
    }}
    {tasks}
}}
server {{
        listen 80 http;
        server_name ctf.sicamp.ru;
        return 301 https://$server_name$request_uri;  # enforce https
#        rewrite ^(.*) https://www.example.com$uri permanent;
}}"""


import os
import yaml
tasks = []
used_ports = {}
tasks_compiled = ""
fatals = 0
for task_name in os.listdir():
    if os.path.isdir(task_name):
        print("task: ", task_name, end = " ")
        docker_path = os.path.join(task_name, "docker-compose.yml")
        if os.path.isfile(docker_path):
            print("Is a service. ")
            with open(docker_path) as f:
                docker = yaml.load(f)
                if "services" not in docker:
                    print("Fatal: no services")
                    fatals+=1
                    continue
                if task_name not in docker["services"]:
                    print("fatal: task_name doesn't match or does not exist")
                    fatals += 1
                    continue
                if "ports" not in docker["services"][task_name]:
                    print("fatal: no ports directive ")
                    fatals += 1
                    continue
                ports = docker["services"][task_name]["ports"]
                if len(ports) != 1:
                    print("fatal: more/less than 1 port")
                    fatals += 1
                    continue
                port = ports[0].split(":")[0]
                if port in used_ports:
                    print("fatal: port is used")
                    fatals += 1
                    continue
                tasks_compiled += task_conf.format(task_name = task_name, port=port)
                print(f"{task_name}.ctf.sicamp.ru -> http://localhost:{port}")
        else:
            print()

conf = conf.format(tasks=tasks_compiled)
print(conf)
with open("LKLCTF.conf", "w") as f:
    f.write(conf)

print(f"{fatals} errors")
