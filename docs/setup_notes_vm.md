# Setup Notes: Self-Managed MySQL on GCP Compute Engine (VM)

## 1. VM Creation (Compute Engine)
![VM Creation](../screenshots/vm/vm_creation.png)
Steps I performed:
- Opened **Compute Engine → VM Instances → Create Instance**  
- Name: `mysql-vm`
- Region: **us-central1**
- Machine type: **e2-micro (free tier)**
- OS: **Ubuntu 22.04 LTS**
- BEFORE creating, I enabled SSH through browser.
- Created the VM.

## 2. Open Port 3306 (Firewall Rule)
![Firewall Port 3306](../screenshots/vm/firewall_3306.png)

- Go to **VPC Network** and then **Firewall rules** and **Create Firewall Rule**
- Name: `allow-mysql-3306`
- Direction: **Ingress**
- Targets: **All instances in the network**
- Source IP range:``0.0.0.0/0``
- Allowed protocols:tcp:3306
- Save.

## 3. SSH Into VM
![MySQL Status](../screenshots/vm/mysql_status.png)

- Open SSH terminal and input
``sudo apt update``
``sudo apt install -y mysql-server``
- Check status using ``systemctl status mysql``

## 4. Allow Remote MySQL Connections
![MySQL bind-address editing](../screenshots/vm/mysql_bind_address.png)
![MySQL bind-address running](../screenshots/vm/mysql_bind_address_running.png)

- Open the MySQL config: ``sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf``
- Change: ``bind-address = 0.0.0.0``
- Save: **CTRL + O** and then **ENTER** and then **CTRL + X**
- Restart MySQL by using ``sudo systemctl restart mysql``

## 5. Create Database & User (Inside MySQL Shell)
![MySQL Version](../screenshots/vm/mysql_version.png)

- Enter MySQL ``sudo mysql``
- I used these commands ``CREATE DATABASE class_db_anitliu; CREATE USER 'anita'@'%' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON class_db_anitliu.* TO 'anita'@'%'; FLUSH PRIVILEGES;``
- Exit

## 6. Python
- I used these commands ``python3 -m venv .venv; source .venv/bin/activate; pip install sqlalchemy pymysql pandas python-dotenv cryptography``
- I made sure my .env was right. In this case its 
    # VM
    VM_DB_HOST=136.114.86.186
    VM_DB_PORT=3306
    VM_DB_USER=anita
    VM_DB_PASS=password
    VM_DB_NAME=class_db_anitliu

## 7. Run vm_demo.py
![Show Tables (Empty)](../screenshots/vm/show_tables_empty.png)

- Use this command ``python scripts/vm_demo.py``
- This should give you:
    Database auto-verified
    Table visits created
    Returned row count = 5

![vm_demo.py Output](../screenshots/vm/vm_demo_output.png)

## 8. Validate in SSH
- I then used these commands 
    ``sudo mysql``
    `` USE class_db_anitliu;``
    `` SHOW TABLES;``
    ``SELECT * FROM visits;``

![VM Final SSH Query](../screenshots/vm/finalssh.png)

## Total Time: ~1 hour 


