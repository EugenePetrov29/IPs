import pandas as pd
import os
from tqdm import tqdm
import csv
from itertools import groupby
from datetime import date as d
import time
import os

today = time.strftime("_%d_%m_%Y")

# Указываем GEO
geos = ('US', 'GB', 'IT', 'DE', 'FR')
# Указываем по сколько IP должно быть в пачке на выходе                               
quantity_per_part = 100000
# Указываем кол-во выгруженых репортов    
reports = 6
# Указываем путь к файлу с имеющимися IP адресами                                                 
# Указываем местонахождение отдельной папки с репортами       

for geo in geos:
    curent_ip_path = F"/home/nik/work/Eugene/new_reports/{geo}.csv"
    new_ip_parts_path = '/home/nik/work/Eugene/new_reports/' + geo + str(today) + '/'
    data = range(1,reports + 1)
                                

    new_ip_from_reposts = []
    curent_ip = pd.read_csv(
        os.path.join(curent_ip_path),
        )
    curent_ip = curent_ip['user_connection_ip'].to_list()

    print('Загрузка и объединение репортов:')
    for i in tqdm(data):
        list_ip = pd.read_csv(
            os.path.join(new_ip_parts_path + str(i) + ".csv"),
            )
        new_ip_from_reposts.append(list_ip['user_connection_ip'].to_list())

    print('Идет обработка данных...')

    def listmerge3(lstlst):
        all=[]
        for lst in lstlst:
            all.extend(lst)
        return all

    result = listmerge3(new_ip_from_reposts)
    curent_ip = listmerge3(curent_ip)

    new_ip_without_validation = set(result)
    print('Загружено новых уникальных IP адресов: ' + str(len(result)), end='   ::::::   ')


    new_ip_list = list(set(new_ip_without_validation) - set(curent_ip))
    print('Новых IP адресов после проверки: ' + str(len(new_ip_list)))

    new_curent_ip = []
    new_curent_ip.append(curent_ip)
    new_curent_ip.append(new_ip_list)
    new_curent_ip = listmerge3(new_curent_ip)


    print('Всего было IP адресов: ' + str(len(curent_ip)), end='   ::::::   ')
    print('Всего стало IP адресов: ' + str(len(new_curent_ip)))


    parts = [new_ip_list[i:i+quantity_per_part] for i in range(0,len(new_ip_list),quantity_per_part)]
    print('Всего пачек: ' + str(len(parts)))



    output_dir_name = geo + today
    parts_output_dir_name = output_dir_name + '/' + str(len(parts)) + '_parts_per_' + str(quantity_per_part) + '_ips'



    os.mkdir(output_dir_name)
    os.mkdir(parts_output_dir_name)


    print('Запись файла со всеми IP адресами:')
    with open(output_dir_name + '/' + 'All_' + geo + today +'.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for item in tqdm(new_curent_ip):
            csv_writer.writerow([item])

    print('Запись файла с новыми IP адресами:')
    with open(output_dir_name + '/' + geo + today +'.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for item in tqdm(new_ip_list):
            csv_writer.writerow([item])

    print('Разделение новых IP адресов на части...')
    a = 1
    for part in parts:
        with open(parts_output_dir_name + '/part' + str(a) + '.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for item in part:
                csv_writer.writerow([item])
        a += 1

    print('Готово!')