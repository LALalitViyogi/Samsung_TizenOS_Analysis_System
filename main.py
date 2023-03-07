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


def show_data(image_path,part_value,inode,file_name):
    output = subprocess.run(shlex.split(f'sudo icat -o {part_value} {image_path} {inode}'),stdout=subprocess.PIPE)
    #try:
    #    print(output.stdout.decode())
    #except:
    #    print(output.stdout)
    
    if file_name:
        try:
            with open(f'./analysis_files/{file_name}.txt','w') as file:
                file.write(output.stdout.decode())
                file.close()
        except:
            with open(f'./analysis_files/{file_name}.txt','wb') as file:
                file.write(output.stdout)
                file.close()

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

    #print("------ OS INFO ---------")
    show_data(image_path,part_value,os_inode,'os_info')

    #finding build info
    build_inode = search_value(etc_output,'tizen-build.conf')

    #print("-------- BUILD INFO --------")
    show_data(image_path,part_value,build_inode,'build_info')

    #finding network info
    etc_inode = search_value(etc_output,'wifi-direct')
    etc_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {etc_inode}'),stdout=subprocess.PIPE)

    wifi_inode = search_value(etc_output,'dhcpd.conf')
    
    #print("-------- WIFI INFO --------")
    show_data(image_path,part_value,wifi_inode,'network_info')

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
    show_data(image_path,part_value,manu_calender_inode,'manufacture_info')

    manu_calender_inode = search_value(manu_output,'calendarData.txt')
    show_data(image_path,part_value,manu_calender_inode,'calendar_info')

    #working card details
    card_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {card_trans_errror_inode}'),stdout=subprocess.PIPE)

    card_trans_errror_inode = search_value(card_output,'tizen-manifest.xml')
    show_data(image_path,part_value,card_trans_errror_inode,'card_info')

    card_list = ['shared','res']
    for i in range(len(card_list)):
        card_trans_errror_inode = search_value(card_output,f'{card_list[i]}')
        card_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {card_trans_errror_inode}'),stdout=subprocess.PIPE)
    
    card_trans_errror_inode = search_value(card_output,'error.html')
    show_data(image_path,part_value,card_trans_errror_inode,'trans_error_info')

    #connected device and alarm info
    device_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {device_alarm_inode}'),stdout=subprocess.PIPE)

    device_path_list = ['res','wgt','views']
    for i in range(len(device_path_list)):
        device_alarm_inode = search_value(device_output,f'{device_path_list[i]}')
        device_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {device_alarm_inode}'),stdout=subprocess.PIPE)
    
    #all connected devices
    device_alarm_inode = search_value(device_output,'devices')
    show_data(image_path,part_value,device_alarm_inode,'connected_Devices_info')

    device_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {device_alarm_inode}'),stdout=subprocess.PIPE)
    device_path_list =['AIR_PURIFIER','javascript']

    for i in range(len(device_path_list)):
        device_alarm_inode = search_value(device_output,f'{device_path_list[i]}')
        device_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {device_alarm_inode}'),stdout=subprocess.PIPE)
    
    device_alarm_inode = search_value(device_output,'app.js')
    show_data(image_path,part_value,device_alarm_inode,'Alarm_info')


    #shopping details and remaainder info
    shop_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {shop_remainder_inode}'),stdout=subprocess.PIPE)
    shop_list = ['res','wgt']

    for i in range(len(shop_list)):
        shop_remainder_inode = search_value(shop_output,f'{shop_list[i]}')
        shop_output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {shop_remainder_inode}'),stdout=subprocess.PIPE)
    
    shop_remainder_inode = search_value(shop_output,'dummyEmart.json')
    show_data(image_path,part_value,shop_remainder_inode,'shopping_info')

    shop_remainder_inode = search_value(shop_output,'dummyListJson.json')
    show_data(image_path,part_value,shop_remainder_inode,'shop_remainder_info')
     

def vol23_artifacts(image_path,part_value):

    output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path}'),stdout=subprocess.PIPE)

    #finding inode for different paths
    
    mac_inode = search_value(output,'etc')
    mail_inode = search_value(output,'dbspace')


    #work for finding MAC Address of system
    mac_output= subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {mac_inode}'),stdout=subprocess.PIPE)
    mac_inode = search_value(mac_output,'.mac.info')
    show_data(image_path,part_value,mac_inode,'MAC_address_info')

    mail_list = ['5001','.account.db']
    for i in range(len(mail_list)):
        mail_output= subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {mail_inode}'),stdout=subprocess.PIPE)
        mail_inode = search_value(mail_output,f'{mail_list[i]}')
    
    show_data(image_path,part_value,mail_inode,'email_info')

    other_list = ['var','lib']
    for i in range(len(other_list)):
        var_inode = search_value(output,f'{other_list[i]}')
        output= subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {var_inode}'),stdout=subprocess.PIPE)
    
    #var device information
    sys_inode = search_value(output,'misc')
    net_inode = search_value(output,'connman')
    blue_inode = search_value(output,'bluetooth')
    

    #system configuration info 
    output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {sys_inode}'),stdout=subprocess.PIPE)
    sys_inode = search_value(output,'dnsmasq.leases')
    show_data(image_path,part_value,sys_inode,'sys_configure_info')

    #bluetooth information
    output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {blue_inode}'),stdout=subprocess.PIPE)
    
    blue_addr='m'
    for line in output.stdout.decode().split('\n'):
        reg=re.search('\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}',line)
        if reg is not None:
            blue_addr = reg.group()
            break
            #print(blue_addr)

    blue_inode = search_value(output,blue_addr)
    #print(blue_inode)
    output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {blue_inode}'),stdout=subprocess.PIPE)
    blue_inode = search_value(output,'cache')
    show_data(image_path,part_value,blue_inode,'bluetooth_info')

    #networking service details
    output = subprocess.run(shlex.split(f'sudo fls -o {part_value} {image_path} {net_inode}'),stdout=subprocess.PIPE)
    net_addr='m'

    for line in output.stdout.decode().split('\n'):
        reg = re.search('wifi_\w+_managed_none',line)
        if reg is not None:
            net_addr = reg.group()
            #print(reg.group())
            break
    
    net_inode = search_value(output,net_addr)
    show_data(image_path,part_value,net_inode,'wifi_network_info')
        
    

    






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
            vol23_artifacts(image_path,part_value)
        
        elif partition == 'user':
            pass