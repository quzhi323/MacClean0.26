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
    csv_reader = csv.reader(open(datafile))
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



def get_num_d(app,experiment):
    '''
    get number of all dependencies
    result[0] is fd
    result[1] is sys ofd
    result[2] is isa ofd
    result[3] is running time
    :param app:
    :param filename:
    :return:
    '''
    result=[]
    num_fd=0
    num_syn_ofd=0
    num_inh_ofd = 0
    running_time=0
    root= os.path.join(app.config['basefiledir'], experiment)
    detail=os.path.join(root,'detail')
    output_file = os.path.join(detail,'output.txt')

    with open(output_file) as fr:

        for line in fr.readlines():

            ds = line.split(':')
            if ds[0] == 'FD':
                num_fd=num_fd+1
            if ds[0] == 'SYN_OFD':
                num_syn_ofd=num_syn_ofd+1
            if ds[0] == 'ISA_OFD':
                num_inh_ofd=num_inh_ofd+1
            if ds[0] == 'Running Time':
                running_time=ds[1]


    result.append(num_fd)
    result.append(num_syn_ofd)
    result.append(num_inh_ofd)
    result.append(running_time)


    return result



def get_ds(app,experiment):
    '''
    result[0]= fd
    result[1]= syn_ofd
    result[2]= inh_ofd
    :param app:
    :return:
    '''

    fd=[]
    syn_ofd=[]
    inh_ofd=[]

    root = os.path.join(app.config['basefiledir'], experiment)
    detail = os.path.join(root, 'detail')
    output_file = os.path.join(detail, 'output.txt')

    with open(output_file) as fr:

        for line in fr.readlines():

            ds = line.split(':')
            if ds[0] == 'FD':
                fd.append(ds[1].strip())

            if ds[0] == 'SYN_OFD':
                ofd=ds[1].strip()
                comb=ofd.split("*")
                d=comb[0]
                sense=comb[1]
                rsl=d+"  (sense:"+sense+")"
                syn_ofd.append(rsl)

            if ds[0] == 'ISA_OFD':
                ofd = ds[1].strip()
                comb = ofd.split("*")
                d = comb[0]
                sense = comb[1]
                rsl = d + "  (sense:" + sense + ")"
                inh_ofd.append(rsl)

    result=[]
    result.append(fd)
    result.append(syn_ofd)
    result.append(inh_ofd)

    return result



def get_aofds(app,experiment):

    '''
    aofds[0]= isa_aofd
    aofds[1]= syn_aofd
    aofds[2]= tane
    aofds[3]= isa_hierachy
    aofds[4]=syn_inherachy
    :param app:
    :return:
    '''
    aofds=[]
    isa_aofd=[]
    syn_aofd=[]
    tane=[]
    hierachy_isa={}
    hierachy_syn={}

    root = os.path.join(app.config['basefiledir'], experiment)
    detail = os.path.join(root, 'detail')

    list = os.listdir(detail)  # 列出文件夹下所有的目录与文件

    for i in range(0, len(list)):

        path = os.path.join(detail, list[i])

        check=list[i][-1:]

        if check=='n' and list[i]!= 'hierarchy_isa.json' and list[i]!= 'hierarchy_syn.json':

            data=load_json(path)

            type=data['TYPE']

            if type==1:
                isa_aofd.append(data)
            if type==0:
                syn_aofd.append(data)
            if type==2:
                tane.append(data)

        if list[i]== 'hierarchy_isa.json':
            data=load_json(path)
            hierachy_isa=data

        if list[i]== 'hierarchy_syn.json':
            data=load_json(path)
            hierachy_syn=data

    aofds.append(isa_aofd)
    aofds.append(syn_aofd)
    aofds.append(tane)
    aofds.append(hierachy_isa)
    aofds.append(hierachy_syn)


    return aofds



def compare_ds(app,experiment):

    '''
    aofds[0]= fastofd
    aofds[1]= tanefd
    :param app:
    :return:
    '''
    aofds=[]
    fastofd=[]
    tanefd=[]
    tane=[]

    root = os.path.join(app.config['basefiledir'], experiment)
    detail = os.path.join(root, 'detail')

    list = os.listdir(detail)  # 列出文件夹下所有的目录与文件

    for i in range(0, len(list)):

        path = os.path.join(detail, list[i])
        check=list[i][-1:]
        if check=='n' and list[i]!= 'hierarchy_isa.json' and list[i]!= 'hierarchy_syn.json':

            data=load_json(path)

            type=data['TYPE']

            if type==1:
                fastofd.append(data)
            if type==0:
                fastofd.append(data)
            if type==2:
                tane.append(data)

    aofds.append(fastofd)
    aofds.append(tane)
    return aofds



def load_json(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data



def aofd_dict(aofd_list):
    aofd_dict={}
    for aofd in aofd_list:
        id = aofd['ID']
        aofd_dict[id]=aofd

    return aofd_dict



def sort_hierachy(hierachy,dict):

    parents=hierachy['HIERARCHY']

    parents.sort(key=lambda x: dict[x["ID"]]["ERROR_RATE"], reverse=True)


    for parent in parents:

        kids = parent['CHILDREN']

        kids.append(parent['ID'])

        kids.sort(key=lambda x: dict[x]["ERROR_RATE"], reverse=True)



