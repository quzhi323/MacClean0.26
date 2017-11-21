import csv
import json
import os


def post_data_info(app,name_experiment, filename):
    '''
    return data file for visual showing
    info[0]=data
    info[1]=num_row
    info[2]=num_col
    info[3]=attributes
    :param app:
    :param filename:
    :return:
    '''
    info = []
    data = []
    example_folder=os.path.join(app.config['basefiledir'], name_experiment)
    data_folder=os.path.join(example_folder,'data')
    datafile = os.path.join(data_folder, filename)
    csv_reader = csv.reader(open(datafile, encoding='utf-8'))
    cal_row =0
    attributes=None
    for row in csv_reader:
        if(cal_row==0):
            attributes=row
        else:
            data.append(row)
        cal_row = cal_row + 1
    num_row = cal_row - 1
    info.append(data)
    info.append(num_row)
    info.append(len(attributes))
    info.append(attributes)

    return info


def get_num_d(app):
    '''
    get number of all dependencies
    result[0] is fd
    result[1] is sys ofd
    result[2] is isa ofd
    :param app:
    :param filename:
    :return:
    '''
    result=[]
    num_fd=0
    num_syn_ofd=0
    output_file = os.path.join(app.config['basefiledir'],'output.txt')

    with open(output_file) as fr:

        for line in fr.readlines():

            ds = line.split(':')
            if ds[0][0] == 'F':
                num_fd=num_fd+1
            if ds[0][0] == 'O':
                num_syn_ofd=num_syn_ofd+1



    result.append(num_fd)
    result.append(num_syn_ofd)


    return result


def get_ds(app):
    '''
    result[0]= fd
    result[1]= ofd
    :param app:
    :return:
    '''

    fd=[]
    ofd=[]

    output_file = os.path.join(app.config['basefiledir'],'output.txt')

    with open(output_file) as fr:

        for line in fr.readlines():

            ds = line.split(':')
            if ds[0][0] == 'F':
                fd.append(ds[1].strip())

            if ds[0][0] == 'O':
                ofd.append(ds[1].strip())

    result=[]
    result.append(fd)
    result.append(ofd)

    return result


def get_aofds(app):
    '''
    aofds[0]= isa_aofd
    aofds[1]= syn_aofd
    :param app:
    :return:
    '''
    aofds=[]
    isa_aofd=[]
    syn_aofd=[]

    detail = app.config['detail']

    list = os.listdir(detail)  # 列出文件夹下所有的目录与文件

    for i in range(0, len(list)):

        path = os.path.join(detail, list[i])

        check=list[i][-1:]

        if check=='n':

            data=load_json(path)

            type=data['TYPE']

            if type==1:
                isa_aofd.append(data)
            if type==0:
                syn_aofd.append(data)

    aofds.append(isa_aofd)
    aofds.append(syn_aofd)

    return aofds


def load_json(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data





