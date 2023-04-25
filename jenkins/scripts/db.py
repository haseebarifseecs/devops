'''
The Script is expecting to read two Command Line arguments from stdin and uses the "sys" library to parse the Command-Line Arguments.
It uses the postgresql podname and the namespace in which the pod is running to exec into the conatiner and create 
-> use postgres user to create tripal role
-> use postgres user to create tripal database
-> use postgres user to restore database backup
Handle exceptions in case the above fails
'''


import subprocess
import sys

try:
    podname = sys.argv[1]
    namespace = sys.argv[2]
except:
    print("[+]Usage python3 <script.py> <podname> <namespace>")
    
try:
    cmd = f'''kubectl exec -it {podname} -n {namespace} -- psql -U "postgres" -c "create role tripal with superuser login password 'tripal'"'''
    print(cmd)
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)
except:
    print("[Error] Failed Creating Role")
    

try:
    cmd = f'''kubectl exec -it {podname} -n {namespace} -- psql -U "postgres" -c "create database tripal"'''
    print(cmd)
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)
except:
    print("[Error] Failed Creating Database")
    
#kubectl cp -n ${env.NAMESPACE} /home/devops/db-backup/db.sql.gz ${dbPodName}:/data/postgres/backup
try:
    cmd = f'''kubectl cp -n {namespace} /home/devops/db-backup/db.sql.gz {podname}:/data/postgres/backup'''
    print(cmd)
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)
except:
    print("[Error] Failed Copying Backup")

#kubectl exec -n ${env.NAMESPACE} -it ${dbPodName} -- /bin/bash -c 'gunzip /data/postgres/backup/db.sql.gz'
try:
    cmd = f'''kubectl exec -n  {namespace} -it {podname} -- /bin/bash -c "gunzip /data/postgres/backup/db.sql.gz"'''
    print(cmd)
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)
except:
    print("[Error] Failed Unarchiving Database")

#kubectl exec -n ${env.NAMESPACE} -it ${dbPodName} -- psql tripal -U 'postgres' -f '/data/postgres/backup/db.sql'
try:
    cmd = f'''kubectl exec -n {namespace} -it {podname} -- psql tripal -U "postgres" -f "/data/postgres/backup/db.sql"'''
    print(cmd)
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)
except:
    print("[Error] Failed Restoring Database")