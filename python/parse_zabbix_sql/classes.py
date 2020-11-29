import psycopg2
import datetime
import config


connlst = [
    config.zabbix_db_hostname,
    config.zabbix_db_username,
    config.zabbix_db_password,
    config.zabbix_db_name
]


# Factory
class Report:
    def __init__(self):
        raise Exception('Cannot create an instance for class Report')

    def get_report(report):
        if report == 'incoming_traffic':
            return Get_zabbix_metriks(connlst).write_incoming_traffic(config.filename)
        elif report == 'hdd_size':
            return Get_zabbix_metriks(connlst).write_hdd_size(config.filename)
        elif report == 'speed_reading':
            return Get_zabbix_metriks(connlst).write_speed_reading(config.filename)
        elif report == 'speed_writing':
            return Get_zabbix_metriks(connlst).write_speed_writing(config.filename)
        elif report == 'using_hdd_size':
            return Get_zabbix_metriks(connlst).write_using_hdd_size(config.filename)
        elif report == 'memory_used':
            return Get_zabbix_metriks(connlst).write_memory_used(config.filename)
        elif report == 'cpu_used':
            return Get_zabbix_metriks(connlst).write_cpu_used(config.filename)
        else:
            Exception('There is not report with name {report}')


# Connector (Parent class)
class Connect_database:
    def __init__(self, connlst):
        self.__connlst = connlst

    def get_connection(self):
        try:
            with psycopg2.connect(connlst) as conn:
                return conn.cursor()
        except psycopg2.Error:
            print("Cannot connect to database")


# Get Zabbix metriks
class Get_zabbix_metriks(Connect_database):
    def __init__(self, connlst):
        super().__init__(connlst)

    def __get_incoming_traffic(self):
        cursor = super().get_connection()
        date_last_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month - 1) + '-01'
        date_this_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-01'
        try:
            cursor.execute("""
                select h.name, i.itemid, round(avg(value_avg/1000/1000), 2) as avg, round(max(value_max)/1000/1000, 2) as max
                from trends t
                inner join items i on t.itemid = i.itemid
                inner join hosts h on h.hostid = i.hostid
                where i.itemid in (38501, 36500, 38001, 38735) and to_timestamp(clock) between %s and %s
                group by h.name, i.itemid
                order by h.name
               """, (date_last_month, date_this_month,))
        except psycopg2.Error:
            print("Cannot run the sql query")

        return list(cursor)

    def write_incoming_traffic(self, filename):
        lst = (self.__get_incoming_traffic())
        if lst is not None:
            lst = list(lst)
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write("____________ (2) Incomming Traffic _________________\n")
                    for line in lst:
                        f.write(str(line[2]))
                        f.write(config.spliter)
                        f.write('\n')
                        f.write(str(line[3]))
                        f.write(config.spliter)
                        f.write('\n')
                    f.write("____________________________________________________\n")
            except PermissionError:
                print('Do not have permission to create the file')

    def __get_hdd_size(self):
        cursor = super().get_connection()
        date_this_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-01'
        try:
            cursor.execute("""
                select h.name, round((tu.value_min/1024/1024/1024)) as value
                from trends_uint tu
                inner join items i on tu.itemid = i.itemid
                inner join hosts h on h.hostid = i.hostid
                where i.itemid in (36676, 36677, 38747, 38748, 38049, 38050, 38629, 38630) and to_timestamp(clock) = %s
                order by h.name
               """, (date_this_month,))
        except psycopg2.Error:
            print("Cannot run the sql query")

        return list(cursor)

    def write_hdd_size(self, filename):
        lst = (self.__get_hdd_size())
        if lst is not None:
            lst = list(lst)
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write("__________________ (3) HDD Size ____________________\n")
                    for line in lst:
                        if line[1] > 1000:
                            f.write(str(round(line[1]/1000 , 1)))
                        else:
                            f.write(str(line[1]))
                        f.write(config.spliter)
                        f.write('\n')
                    f.write("____________________________________________________\n")
            except PermissionError:
                print('Do not have permission to create the file')

    def __get_speed_reading(self):
        cursor = super().get_connection()
        date_last_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month - 1) + '-01'
        date_this_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-01'
        try:
            cursor.execute("""
                    select h.name, round((max(value_max/1000/1000)), 2) as max
                    from trends t
                    inner join items i on t.itemid = i.itemid
                    inner join hosts h on h.hostid = i.hostid
                    where i.itemid in (36484, 36937, 37507, 41997, 36485, 36938, 37508, 41998) and to_timestamp(clock) between %s and %s
                    group by h.name, i.itemid
                    order by h.name
               """, (date_last_month, date_this_month,))
        except psycopg2.Error:
            print("Cannot run the sql query")

        return list(cursor)

    def write_speed_reading(self, filename):
        lst = (self.__get_speed_reading())
        if lst is not None:
            lst = list(lst)
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write("____________ (3.5) Speed Reading ___________________\n")
                    for line in lst:
                        f.write(str(line[1]))
                        f.write(config.spliter)
                        f.write('\n')
                    f.write("____________________________________________________\n")
            except PermissionError:
                print('Do not have permission to create the file')

    def __get_speed_writing(self):
        cursor = super().get_connection()
        date_last_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month - 1) + '-01'
        date_this_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-01'
        try:
            cursor.execute("""
                    select h.name, round((max(value_max/1000/1000)), 2) as max
                    from trends t
                    inner join items i on t.itemid = i.itemid
                    inner join hosts h on h.hostid = i.hostid
                    where i.itemid in (36494, 36947, 37517, 42007, 36495, 36948, 37518, 42008) and to_timestamp(clock) between %s and %s
                    group by h.name, i.itemid
                    order by h.name
               """, (date_last_month, date_this_month,))
        except psycopg2.Error:
            print("Cannot run the sql query")

        return list(cursor)

    def write_speed_writing(self, filename):
        lst = (self.__get_speed_reading())
        if lst is not None:
            lst = list(lst)
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write("____________ (3.6) Speed Writing ___________________\n")
                    for line in lst:
                        f.write(str(line[1]))
                        f.write(config.spliter)
                        f.write('\n')
                    f.write("____________________________________________________\n")
            except PermissionError:
                print('Do not have permission to create the file')

    def __get_using_hdd_size(self):
        cursor = super().get_connection()
        date_this_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-01'
        try:
            cursor.execute("""
                        select h.name, tu.itemid, round((min(tu.value_min)/1024/1024/1024),2) as value
                        from trends_uint tu
                        inner join items i on tu.itemid = i.itemid
                        inner join hosts h on h.hostid = i.hostid
                        where i.itemid in (36678, 36679, 38749, 38750, 38051, 38052, 38631, 38632) and to_timestamp(clock) = %s
                        group by h.name, tu.itemid
                        order by h.name
                   """, (date_this_month,))
        except psycopg2.Error:
            print("Cannot run the sql query")

        return list(cursor)

    def write_using_hdd_size(self, filename):
        lst = (self.__get_using_hdd_size())
        if lst is not None:
            lst = list(lst)
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write("____________ (3.7) Using HDD Size __________________\n")
                    for line in lst:
                        f.write(str(line[2]))
                        f.write(config.spliter)
                        f.write('\n')
                    f.write("____________________________________________________\n")
            except PermissionError:
                print('Do not have permission to create the file')

    def __get_memory_used(self):
        cursor = super().get_connection()
        date_last_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month - 1) + '-01'
        date_this_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-01'
        try:
            cursor.execute("""
                    select h.name, round((max(value_max/1024/1024/1024)), 2) as max
                    from trends t
                    inner join items i on t.itemid = i.itemid
                    inner join hosts h on h.hostid = i.hostid
                    where i.itemid in (36466, 36856, 37245, 37861) and to_timestamp(clock) between %s and %s
                    group by h.name, i.itemid
                    order by h.name 
                  """, (date_last_month, date_this_month,))
        except psycopg2.Error:
            print("Cannot run the sql query")

        return list(cursor)

    def write_memory_used(self, filename):
        lst = (self.__get_memory_used())
        if lst is not None:
            lst = list(lst)
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write("____________ (4) Memory Used __________________\n")
                    for line in lst:
                        f.write(str(line[1]))
                        f.write(config.spliter)
                        f.write('\n')
                    f.write("____________________________________________________\n")
            except PermissionError:
                print('Do not have permission to create the file')

    def __get_cpu_used(self):
        cursor = super().get_connection()
        date_last_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month - 1) + '-01'
        date_this_month = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-01'
        try:
            cursor.execute("""
                    select h.name, round((100 - min(value_min)), 2) as min
                    from trends t
                    inner join items i on t.itemid = i.itemid
                    inner join hosts h on h.hostid = i.hostid
                    where i.itemid in (36382, 36772, 37161, 37777) and to_timestamp(clock) between %s and %s
                    group by h.name, i.itemid
                    order by h.name
                  """, (date_last_month, date_this_month,))
        except psycopg2.Error:
            print("Cannot run the sql query")

        return list(cursor)

    def write_cpu_used(self, filename):
        lst = (self.__get_cpu_used())
        if lst is not None:
            lst = list(lst)
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write("____________ (5) CPU Used __________________\n")
                    for line in lst:
                        f.write(str(line[1]))
                        f.write(config.spliter)
                        f.write('\n')
                    f.write("____________________________________________________\n")
            except PermissionError:
                print('Do not have permission to create the file')