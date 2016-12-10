# py-postgresql基本操作
###创建连接

##### 详细config配置参见[官方文档](http://python.projects.pgfoundry.org/docs/1.1/driver.html)中*Connection Keywords*部分

```sql
    config = {
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres'
    }
    db = pg_driver.connect(**config)
```

### 表创建

```sql
    ps = db.prepare("""
         CREATE TABLE IF NOT EXISTS employee (
             employee_name text,
             employee_salary numeric,
             employee_dob date,
             employee_hire_date date
         );
     """)
```

### 插入

```sql
    from datetime import date, datetime
    mkemp = db.prepare("INSERT INTO employee VALUES ($1, $2, $3, $4)")
  --单行插入
    rs = mkemp(
        "John Johnson",
        "92000",
        date(1950, 12, 10),
        date(1998, 4, 23)
    )
  > ('INSERT', 1) --'INSERT'为操作类型，1为影响行数

  --多行插入
    mkemp.load_rows([
        ("Jack Johnson", "85000", date(1962, 11, 23), date(1990, 3, 5)),
        ("Debra McGuffer", "52000", date(1973, 3, 4), date(2002, 1, 14)),
        ("Barbara Smith", "86000", date(1965, 2, 24), date(2005, 7, 19)),
    ])
```

### 查询
```sql
    ps = db.prepare("select * from employee")
    rs = ps()
    print(rs)

  > [('Jack Johnson', Decimal('85000'), datetime.date(1962, 11, 23), datetime.date(1990, 3, 5)), ('Debra McGuffer', Decimal('52000'), datetime.date(1973, 3, 4), datetime.date(2002, 1, 14)), ('Barbara Smith', Decimal('86000'), datetime.date(1965, 2, 24), datetime.date(2005, 7, 19)), ('John Johnson', Decimal('92000'), datetime.date(1950, 12, 10), datetime.date(1998, 4, 23))]
```
##### 查询结果遍历/取值方式，结果为list结构

1. 整行遍历

   ```sql
       for row in rs:
           print(row)

   > ('Jack Johnson', Decimal('85000'), datetime.date(1962, 11, 23), datetime.date(1990, 3, 5))
   > ('Debra McGuffer', Decimal('52000'), datetime.date(1973, 3, 4), datetime.date(2002, 1, 14))
   > ('Barbara Smith', Decimal('86000'), datetime.date(1965, 2, 24), datetime.date(2005, 7, 19))
   > ('John Johnson', Decimal('92000'), datetime.date(1950, 12, 10), datetime.date(1998, 4, 23))
    
   ```

2. 输出每行指定位置的值

   ```sql
   --下表从0开始
       for row in rs:
           print(row[0])

   > Jack Johnson
   > Debra McGuffer
   > Barbara Smith
   > John Johnson
   ```

3. 输出每行指定字段的值  

   ```sql
       for row in rs:
           print(row['employee_name'])

   > Jack Johnson
   > Debra McGuffer
   > Barbara Smith
   > John Johnson
   ```

4. 迭代行中的key-value

   ```sql
       row = db.prepare("select * from employee").first()
       for k, v in row.items():
           print(k + "=" + str(v))

   > employee_name=Jack Johnson
   > employee_salary=85000
   > employee_dob=1962-11-23
   > employee_hire_date=1990-03-05
   ```

### 更新

```sql
    ps = db.prepare("update employee set employee_name='gloria'  where employee_dob=$1")
    rs = ps(date(1962, 11, 23))
    print(rs())

> ('UPDATE', 1)
```