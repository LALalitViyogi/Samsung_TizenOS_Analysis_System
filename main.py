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
    show_data(image_path,part_value,os_inode,'os_info')

    #finding build info
    build_inode = search_value(etc_output,'tizen-build.conf')

    print("-------- BUILD INFO --------")
    show_data(image_path,part_value,build_inode,'build_info')





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