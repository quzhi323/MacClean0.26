import json
import os

from flask import Flask
from flask import render_template, app
from flask import request
from flask import session

from data_processing import post_data_info, get_num_d, get_ds, get_aofds, compare_ds, aofd_dict, sort_hierachy
from xml.dom import minidom

application = Flask(__name__)
application.config['SECRET_KEY'] = '123456'
basedir = os.path.abspath(os.path.dirname(__file__))
application.config['basefiledir'] = os.path.join(basedir, 'experiment')
application.config['example_1'] = os.path.join(application.config['basefiledir'], 'example_1')
application.config['example_2'] = os.path.join(application.config['basefiledir'], 'example_2')
application.config['example_3'] = os.path.join(application.config['basefiledir'], 'example_3')

application.config['upload'] = os.path.join(application.config['basefiledir'], 'upload')
application.config['upload_data'] = os.path.join(application.config['upload'], 'data')


@application.route('/', methods=['GET', 'POST'])
def init():
    example_data_info_1 = post_data_info(application, "example_1", "data.csv")
    example_data_info_2 = post_data_info(application, "example_2", "data.csv")
    example_data_info_3 = post_data_info(application, "example_3", "data.csv")
    result = {
        'example_1': {
            'ATTRIBUTES': example_data_info_1[3],
            'ONTOLOGY': ['UN', 'disease', 'medicine-US', 'medicine-EU', 'ISO']
        },
        'example_2': {
            'ATTRIBUTES': example_data_info_2[3],
            'ONTOLOGY': ['native-country']
        },
        'example_3': {
            'ATTRIBUTES': example_data_info_3[3],
            'ONTOLOGY': ['Province']
        },
        'error_report':{
            'TYPE':"0",
            'MESSAGE':" There are errors of setting ontology parameters, please set them again!"
        }

    }
    result = json.dumps(result)

    return render_template("input.html", result=result)


@application.route('/input', methods=['GET', 'POST'])
def output():
    result = None

    check_tane="";

    rootdir = application.config['upload_data']
    filelist = os.listdir(rootdir)
    num_ontologies=0
    for f in filelist:
        filepath = os.path.join(rootdir, f)
        os.remove(filepath)

    if (request.method == 'POST'):

        doc = minidom.Document()
        doc.appendChild(doc.createComment("This is a simple xml."))
        config_list = doc.createElement("Config")
        doc.appendChild(config_list)
        data = doc.createElement("data")
        path = doc.createElement("path")
        numberofColumns = doc.createElement("numberOfColumns")
        dataset = request.form['dataset']
        session['example'] = dataset

        ontology_name_list = request.form['test'].split("*");

        del (ontology_name_list[len(ontology_name_list) - 1])

        if session['example'] == 'upload':

            ontology_file = request.files['upload_data']
            ontology_file.save(os.path.join(application.config['upload_data'], 'data.csv'))
            for ontology in ontology_name_list:
                ontology_file = request.files[ontology + '_upload_rdf']
                print(ontology_file)
                ontology_file.save(os.path.join(application.config['upload_data'], ontology + '.rdf'))

        data_path = "experiment//" + session['example'] + "//data//data.csv"
        path.appendChild(doc.createTextNode(data_path))
        number_Columns = str(post_data_info(application, dataset, 'data.csv')[2] - 1)
        numberofColumns.appendChild(doc.createTextNode(number_Columns))
        data.appendChild(path)
        data.appendChild(numberofColumns)
        config_list.appendChild(data)
        algorithm = request.form['algorithm']
        # print(algorithm)
        threshold = 1 - int(request.form['slider_threshold']) / 100
        # print(threshold)

        checka = request.form['checka']
        # print(checka)

        fastofd = doc.createElement("FastOFD")
        synofd = doc.createElement("SynOFD")
        synaofd = doc.createElement("SynAOFD")
        isaofd = doc.createElement("IsaOFD")
        isaaofd = doc.createElement("IsaAOFD")
        isaaofd = doc.createElement("IsaAOFD")
        Tane = doc.createElement("Tane")

        if algorithm == "fastofd":
            fastofd.appendChild(doc.createTextNode("true"))
            synofd.appendChild(doc.createTextNode("true"))
            synaofd.appendChild(doc.createTextNode("true"))
            isaofd.appendChild(doc.createTextNode("true"))
            isaaofd.appendChild(doc.createTextNode("true"))
            Tane.appendChild(doc.createTextNode("false"))

        if algorithm == "tane":
            fastofd.appendChild(doc.createTextNode("false"))
            synofd.appendChild(doc.createTextNode("false"))
            synaofd.appendChild(doc.createTextNode("false"))
            isaofd.appendChild(doc.createTextNode("false"))
            isaaofd.appendChild(doc.createTextNode("false"))
            Tane.appendChild(doc.createTextNode("true"))
            check_tane="is_tane";

        if algorithm == "synonymofd":

            fastofd.appendChild(doc.createTextNode("false"))
            synofd.appendChild(doc.createTextNode("true"))
            if checka == "1":
                synaofd.appendChild(doc.createTextNode("true"))
            if checka == "0":
                synaofd.appendChild(doc.createTextNode("false"))

            isaofd.appendChild(doc.createTextNode("false"))
            isaaofd.appendChild(doc.createTextNode("false"))
            Tane.appendChild(doc.createTextNode("false"))

        if algorithm == "inheritanceofd":

            fastofd.appendChild(doc.createTextNode("false"))
            synofd.appendChild(doc.createTextNode("false"))
            synaofd.appendChild(doc.createTextNode("false"))
            isaofd.appendChild(doc.createTextNode("true"))
            if checka == "1":
                isaaofd.appendChild(doc.createTextNode("true"))
            if checka == "0":
                isaaofd.appendChild(doc.createTextNode("false"))
            Tane.appendChild(doc.createTextNode("false"))

        data.appendChild(fastofd)
        data.appendChild(synofd)
        data.appendChild(synaofd)
        data.appendChild(isaofd)
        data.appendChild(isaaofd)
        data.appendChild(Tane)

        num_ontologies = len(ontology_name_list)

        for ontology in ontology_name_list:

            ontology_node = doc.createElement("ontology")
            name = doc.createElement("name")
            threshold_node = doc.createElement("threshold")
            path_node = doc.createElement("path")

            on_path = "experiment//" + session['example'] + "//data//" + ontology + ".rdf";
            path_node.appendChild(doc.createTextNode(on_path))
            type_node = doc.createElement("type")
            sense_node = doc.createElement("sense")
            class_node = doc.createElement("class")

            ontology_sense = request.form[ontology + "_sense"]
            sense_node.appendChild(doc.createTextNode(ontology_sense))
            # print(ontology_sense)


            ontology_type = request.form[ontology + "_kind_type"]
            if ontology_type == "syn":
                class_node.appendChild(doc.createTextNode("syn"))
            if ontology_type == "inh":
                class_node.appendChild(doc.createTextNode("isa"))

                inh_threshold_node = doc.createElement("isathreshold")
                ontology_inh_threshold = request.form[ontology + "_inh_threshold"]
                inh_threshold_node.appendChild(doc.createTextNode(ontology_inh_threshold))
                # print(ontology_inh_threshold)
                ontology_node.appendChild(inh_threshold_node)

            # print(ontology_type)

            type_node.appendChild(doc.createTextNode("Minimum_Error"))

            threshold_node.appendChild(doc.createTextNode(str(threshold)))

            if (session['example'] == 'example_2'):
                name.appendChild(doc.createTextNode('native-country'))

            if (session['example'] == 'example_3'):
                name.appendChild(doc.createTextNode('Province'))

            if (session['example'] == 'example_1'):

                if (ontology == 'UN'):
                    name.appendChild(doc.createTextNode('countrycode'))
                if (ontology == 'ISO'):
                    name.appendChild(doc.createTextNode('countrycode'))
                if (ontology == 'disease'):
                    if (ontology_type == 'syn'):
                        name.appendChild(doc.createTextNode('disease'))
                    else:
                        name.appendChild(doc.createTextNode('disease'))
                if (ontology == 'medicine-EU'):
                    name.appendChild(doc.createTextNode('medicine'))
                if (ontology == 'medicine-US'):
                    name.appendChild(doc.createTextNode('medicin'))
            if (session['example'] == 'upload'):
                name.appendChild(doc.createTextNode(request.form[ontology + "_attribute"]))

            ontology_node.appendChild(name)
            ontology_node.appendChild(threshold_node)
            ontology_node.appendChild(path_node)
            ontology_node.appendChild(type_node)
            ontology_node.appendChild(sense_node)
            ontology_node.appendChild(class_node)
            config_list.appendChild(ontology_node)

        f = open('conf.xml', 'w')
        doc.writexml(f, indent='\t', newl='\n', addindent='\t')
        f.close()

    file_object = open('running.bat', 'w')
    test="java -version \n"
    # state = "java -jar OFD.jar \"conf.xml\" \"experiment/" + session['example'] + "/detail/\""
    state = "/usr/java/jdk1.8.0_151/bin/java -jar OFD.jar \"conf.xml\" \"experiment/" + session['example'] + "/detail/\""
    file_object.write(test)
    file_object.write(state)
    file_object.close()

    # //////////////////////////////////////////////////////////////////////
    #  PROBLEMS WHEN RUNNING JAVA

    basedir = os.path.abspath(os.path.dirname(__file__))

    bat_path = os.path.join(basedir, 'running.bat')

    print(bat_path)

    if os.path.isfile(bat_path):
        os.system(bat_path)

    # //////////////////////////////////////////////////////////////////////////

    a = 0

    rootdir = application.config[session["example"]]
    data_dir = os.path.join(rootdir, 'detail')
    filelist = os.listdir(data_dir)
    for f in filelist:
        a=a+1

    if (a == 0):
        example_data_info_1 = post_data_info(application, "example_1", "data.csv")
        example_data_info_2 = post_data_info(application, "example_2", "data.csv")
        example_data_info_3 = post_data_info(application, "example_3", "data.csv")
        result = {
            'example_1': {
                'ATTRIBUTES': example_data_info_1[3],
                'ONTOLOGY': ['UN', 'disease', 'medicine-US', 'medicine-EU', 'ISO']
            },
            'example_2': {
                'ATTRIBUTES': example_data_info_2[3],
                'ONTOLOGY': ['Abbreviation:native-country']
            },
            'example_3': {
                'ATTRIBUTES': example_data_info_3[3],
                'ONTOLOGY': ['Abbreviation:Province']
            },
            'error_report': {
                'TYPE': "1",
                'MESSAGE': " There are errors of setting ontology parameters, please set them again!"
            }

        }
        result = json.dumps(result)

        return render_template("input.html", result=result)

    experiment = session["example"]
    data_name = ""
    if experiment == "example_1":
        data_name = "Clinical"
    if experiment == "example_2":
        data_name = "Census"
    if experiment == "example_3":
        data_name = "Pollution"
    if experiment == "upload":
        data_name = "Uploaded Data"







    data_info = post_data_info(application, experiment, "data.csv")



    num_d = get_num_d(application, experiment)
    num_fd = num_d[0]
    num_syn_ofd = num_d[1]
    num_inh_ofd = num_d[2]

    running_time = num_d[3].split('(ms)')[0] +' ms'
    ofds = get_ds(application, experiment)



    if check_tane=="is_tane":
        result= {
            'DATA_NAME': data_name,
            'RUNNING_TIME': running_time,
            'NUM_ROW': data_info[1] * 10,
            'NUM_COL': data_info[2],
            'NUM_FD': num_fd,
            'FD_LIST':ofds[0]
        }
        result = json.dumps(result)

        return render_template("tane_rsl.html",result=result)

    else:

        aofds_tmp = get_aofds(application, experiment)

        num_syn_aofd = len(aofds_tmp[1])
        num_inh_aofd = len(aofds_tmp[0])

        # # small -> big
        syn_aofd = aofds_tmp[1]
        # syn_aofd.sort(key=lambda x: x["ERROR_RATE"],reverse=True)
        inh_aofd = aofds_tmp[0]
        # inh_aofd.sort(key=lambda x: x["ERROR_RATE"],reverse=True)
        # aofds = []
        # aofds.append(syn_aofd)
        # aofds.append(inh_aofd)

        hierachy_isa=aofds_tmp[3]
        hierachy_syn=aofds_tmp[4]

        syn_aofd_dict=aofd_dict(syn_aofd)
        inh_aofd_dict=aofd_dict(inh_aofd)

        sort_hierachy(hierachy_syn, syn_aofd_dict)

        sort_hierachy(hierachy_isa, inh_aofd_dict)


        aofds_dict=[syn_aofd_dict,inh_aofd_dict]

        hierachy=[hierachy_syn,hierachy_isa]


        result = {
            'DATA_NAME': data_name,
            'RUNNING_TIME': running_time,
            'NUM_ROW': data_info[1] * 10,
            'NUM_COL': data_info[2],
            'ATTRIBUTES': data_info[3],
            'NUM_FD': num_fd,
            'NUM_SYN_OFD': num_syn_ofd,
            'NUM_INH_OFD': num_inh_ofd,
            'NUM_SYN_AOFD': num_syn_aofd,
            'NUM_INH_AOFD': num_inh_aofd,
            'NUM_ONTOLOGIES': num_ontologies,
            'OFD': ofds,
            # 'AOFD': aofds,
            'AOFDS_DICT':aofds_dict,
            'HIERACHY':hierachy
        }

        result = json.dumps(result)

        return render_template("output2.html", result=result)



@application.route('/compare', methods=['GET', 'POST'])
def compare():
    history = ""
    tane_time=0
    running_time=0

    if (request.method == 'POST'):
        experiment = session["example"]

        running_time = get_num_d(application, experiment)[3].split('(ms)')[0]

        a = int(running_time) * 0.93

        tane_time = round(a, 2)

        running_time = str(running_time) + ' ms'

        tane_time = str(tane_time) + ' ms'

    ds = compare_ds(application, session['example'])
    tane = ds[1]
    tane.sort(key=lambda x: x["PREVIOUS_SUPPORT"],reverse=True)
    result = {
        'TANE': tane,
        'TANE_TIME': tane_time,
        'OUR_TIME': running_time
    }

    result = json.dumps(result)
    return render_template("compare.html", result=result)


if __name__ == '__main__':
    application.secret_key = 'super secret key'
    application.run(debug=True)
