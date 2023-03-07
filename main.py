import subprocess
import shlex
import os
import re


def print_table(image_path):
    outputs= subprocess.run(shlex.split(f'sudo mmls {image_path}'),stdout= subprocess.PIPE)
    for line in outputs.stdout.decode().split('\n')[5:]:
        values=list()
        for i in line.split(' '):
            if i!=' ' and i!='':
                values.append(i)
        print(values[-1:])

def get_part_inode(image_path,partition):
    outputs= subprocess.run(shlex.split(f'sudo mmls {image_path}'),stdout= subprocess.PIPE)
    for line in outputs.stdout.decode().split('\n'):
        if partition in line:
            values = list()
            for i in line.split(' '):
                if i!=' ' and i!='':
                    values.append(i)
            return values[2]


def show_data(image_path,part_value,inode,file_name=None):
    output = subprocess.run(shlex.split(f'sudo icat -o {part_value} {image_path} {inode}'))
    try:
        print(output.stdout.decode())
    except:
        print(output.stdout)

def search_value(output,file_name):
    
    for line in output.stdout.decode().split('\n'):
        if file_name in line:
            return line.split(' ')[1].split(':\t')[0]

def vol21_artifacts(image_path,part_value):

    output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path}'),stdout=subprocess.PIPE)
    
    #etc file part
    etc_inode=search_value(output,'etc')

    #usr_app file part
    usr_inode = search_value(output,'usr')
    
    #print(etc_inode)
    #print(usr_inode)

    etc_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {etc_inode}'),stdout=subprocess.PIPE)

    #finding os_info inode
    os_inode = search_value(etc_output,'os-release')

    print("------ OS INFO ---------")
    #show_data(image_path,part_value,os_inode,'os_info')

    #finding build info
    build_inode = search_value(etc_output,'tizen-build.conf')

    print("-------- BUILD INFO --------")
    #show_data(image_path,part_value,build_inode,'build_info')

    #finding network info
    etc_inode = search_value(etc_output,'wifi-direct')
    etc_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {etc_inode}'),stdout=subprocess.PIPE)

    wifi_inode = search_value(etc_output,'dhcpd.conf')
    
    print("-------- WIFI INFO --------")
    #show_data(image_path,part_value,wifi_inode,'network_info')

    #working user apps
    output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {usr_inode}'),stdout=subprocess.PIPE)
    usr_inode = search_value(output,'apps')
    output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {usr_inode}'),stdout=subprocess.PIPE)

    #recipe image
    #img_inode = search_value(output,'1K3CsGDv16')

    #payment details
    #pay_inode = search_value(output,'8s4wz2jex0')

    #Manufacturer location and calender data
    manu_calender_inode = search_value(output,'9zWvGSYU8Z')

    #geo location
    #geo_inode = search_value(output,'com.glympse.tizen.frapp')

    #voice messages
    #voice_inode = search_value(output,'com.glympse.tizen.frapp.service')

    #card and transaction error details
    card_trans_errror_inode = search_value(output,'com.mastercard.tizen')

    #connected device and alarm info
    device_alarm_inode = search_value(output,'kzOK54sYx0')

    #shopping and remainder details
    shop_remainder_inode = search_value(output,'LAykghKXQw')

    ##############   detailed work for each aspects ##################

    #manufacturing
    manu_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {manu_calender_inode}'),stdout=subprocess.PIPE)
    manu_list = ['res','wgt','libs']

    for i in range(len(manu_list)):
        manu_calender_inode = search_value(manu_output,f'{manu_list[i]}')
        manu_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {manu_calender_inode}'),stdout=subprocess.PIPE)
    
    manu_calender_inode = search_value(manu_output,'AccInfoData.txt')
    #show_data(image_path,part_value,manu_calender_inode,'manufacture_info')

    manu_calender_inode = search_value(manu_output,'calendarData.txt')
    #show_data(image_path,part_value,manu_calender_inode,'calendar_info')

    #working card details
    card_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {card_trans_errror_inode}'),stdout=subprocess.PIPE)

    card_trans_errror_inode = search_value(card_output,'tizen-manifest.xml')
    #show_data(image_path,part_value,card_trans_errror_inode,'card_info')

    card_list = ['shared','res']
    for i in range(len(card_list)):
        card_trans_errror_inode = search_value(card_output,f'{card_list[i]}')
        card_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {card_trans_errror_inode}'),stdout=subprocess.PIPE)
    
    card_trans_errror_inode = search_value(card_output,'error.html')
    #show_data(image_path,part_value,card_trans_errror_inode,'trans_error_info')



    




if __name__ == "__main__":
    image_path = "SamsungRefrigerator-002.img"
    
    print("Choose Mode of Operation")
    print("Automated:1\t Partition Based:2\t Path_File Search:3")
    
    mode=int(input("Enter Mode Number:"))
    
    if mode==1:
        pass

    elif mode==2:
        print_table(image_path)
        
        partition = input("Enter Parttiton Name:")
        part_value=get_part_inode(image_path,partition)
        
        if partition=='rootfs.img':
            vol21_artifacts(image_path,part_value)
        
        elif partition == 'system-data':
            pass
        
        elif partition == 'user':
            pass