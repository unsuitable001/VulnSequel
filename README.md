# VulnSequel

A PoC to demonstate basic SQL injection vulnarabilities. B. Tech DBMS Presentation by Abhineet Kumar & Soumyadip Mondal.

## Build Guide

1. Start your oracle database.
2. Export your credentials to environment.
    For Linux:

    ```bash
    export dbcred='user/pass@host:port'
    ```

3. Then run this to start the app

   ```bash
   pip install -r requirements.txt
   flask run
   ```

4. Create Users Table and populate with dummy data

   ```sql
   CREATE TABLE USERS(username varchar2(26) NOT NULL PRIMARY KEY, pass varchar2(16) NOT NULL);
   ```

5. Create books table and populate with dummy data

   ```sql
   CREATE TABLE BOOKS (BOOK_NO NUMBER(6) PRIMARY KEY, BOOK_NAME VARCHAR2(30) NOT NULL, AUTHOR_NAME VARCHAR2(30), COST NUMBER(7,2), CATEGORY CHAR(10));
   ```

## Using docker

Remember: It's just experimental. May not work out of the box.

### Build

```bash
docker build -t unsuitable001/vulnsql .
docker run -d -p 49161:1521 -p 8080:8080 -p 5000:5000 -v ${PWD}:/devrepo unsuitable001/vulnsql
docker exec -ti <container_name/id> /bin/bash
```

### Run

```bash
docker start <container_name/id>
docker exec -ti <container_name/id> /bin/bash
```

From the shell of the container, run `./start_db.sh` to start the database and `./start.sh` to start the server. **Database gets started automatically.**

### Database

```bash
# Login http://localhost:8080/apex/apex_admin with following credential:
username: ADMIN
password: admin
```

Then create a new workspace, schema and set password accordingly.

## Injection Vectors

### Login

```sql
admin' OR 1 = 1 --
```

### Book Search

```sql
a') UNION SELECT 0, username, pass, 0, 'OTHERS' FROM USERS --
```

## Troubleshooting

1. Make sure that your python arch and Oracle db client arch match up.
2. Make sure to start your dabatase service, i.e `sudo service oracle-xe start`.
3. If there is an error saying `Cannot locate a 64-bit Oracle Client library: "libclntsh.so` or something like that, try doing `export LD_LIBRARY_PATH=$ORACLE_HOME/lib:LD_LIBRARY_PATH` and `source /u01/app/oracle/product/11.2.0/xe/bin/oracle_env.sh`.
4. Do remember, all of the export commands gets enabled for single termial instance. If you close terminals and open again, it gets resetted. For persistance, put these in your `.bashrc` file.
5. For more db related issues, try looking at [cx_Oracle docs](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html).
