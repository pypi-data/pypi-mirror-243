import datetime
import json,time
import shutil
import uuid
import os ,sys
emr_r=os.path.abspath(os.path.dirname(__file__))
rootpath_=os.path.split(emr_r)[0]
sys.path.append(rootpath_)
from vcarhilclient.kunyi_util import *
from vcarhilclient.kunyi_mrt import mrt_client
from vcarhilclient.mrt_client_Logger import _handle_log
from vcarhilclient.kunyi_project import hil_project

class Emr_mrt_client(mrt_client):

    def __init__(self,emr_path,server_name = None, managerment_port=8888, push_port=8889, subscription_port=8890):
        if not os.path.isfile(emr_path):
            raise Exception("Invaild emr path")
        self.project_name = os.path.basename(emr_path).split('.')[0]
        self._emr_path = emr_path
        self.server_name = server_name

        self._emrInfo,self._temp_dir = self._get_proinfo_forEmrPath()
        super().__init__(self.host, server_name, managerment_port, push_port,subscription_port)

        log_path = os.path.join(emr_r,"Log")
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        self.mrt_clien_Log = _handle_log(log_path)


    def _close_env_by_name(self, envName):
        is_env_exists = self.is_env_exists(envName)
        if is_env_exists:
            ec = self.stop_test(envName)
            if ec.value != 0:
                self.mrt_clien_Log.error("End test fail due to %s" % (ec.get_name()))
                return False
            rc = self.delete_test_env(envName)
            if rc.value != 0:
                self.mrt_clien_Log.error("Delete test env %s fail, rc is %s " % (envName, str(rc.value)))
                return False
            else:
                return True
        else:
            self.mrt_clien_Log.warning(f"{envName} not exit!")
            return False

    def close_env_all_of_Em_project(self):
        if len(self.emr_env_names) == 0:
            self.mrt_clien_Log.warning("The current object has no experiments to destroy ")
            return
        for emr_envName,env in self.emr_env_names.items():
            re = self._close_env_by_name(env)
            if re:
                self.mrt_clien_Log.info(f"close env:{env} success!")
            else:
                self.mrt_clien_Log.error(f"close env:{env} failed!")

    def _get_proinfo_forEmrPath(self):
        emrPath = self._emr_path
        '''
        :param emrPath: emr file Path
        :return: [ProjectFilePath;MappingFilePath;EnvironmentName] ;TestBenchLocation
        '''
        cur_dir = os.path.dirname(os.path.abspath(emrPath))
        with open(emrPath) as emr_file:
            try:
                emr_json = json.load(emr_file)
            except:
                self.mrt_clien_Log.error("ipr is not a valid json file")
                raise Exception("ipr is not a valid json file")

            envInfos = []
            self.emr_env_names = {}
            self.emr_env_iprs = {}
            self.emr_env_projects = {}
            self.emr_env_hilsystem = {}
            self.emr_env_node = {}
            pro_name = os.path.basename(emrPath).replace(".emr", "")
            self.host = emr_json["TestBenchLocation"]["IP"]
            for i in emr_json["EnvironmentList"]:
                envInfo = []
                ProjectFilePath = i["ProjectFilePath"]
                MappingFilePath = i["MappingFilePath"]
                emr_env_name = i['EnvironmentName']
                if "NodeName" in i:
                    self.emr_env_node[emr_env_name] = i["NodeName"]
                else:
                    self.emr_env_node[emr_env_name] = None
                self.emr_env_iprs[emr_env_name] = os.path.join(cur_dir, ProjectFilePath)
                this_hilp = hil_project(os.path.join(cur_dir, ProjectFilePath))
                self.emr_env_projects[emr_env_name] = this_hilp
                with open(this_hilp.hil_json_path, mode="r",encoding='utf-8') as hpf:
                    hpjson = json.load(hpf)
                system_id = hpjson["SystemID"][:16]
                mid_file = os.path.join(os.getenv("APPDATA"), "VCarSystem", "VCarEE", "mid")
                if os.path.isfile(mid_file):
                    with open(mid_file, "r") as midf:
                        code = midf.readline().strip()
                else:
                    code = uuid.UUID(int=uuid.getnode()).hex[-8:]
                if self.server_name is None:
                    EnvironmentName = f"{code}_{system_id}_{pro_name}_{emr_env_name}"
                else:
                    EnvironmentName = f"{system_id}_{pro_name}_{emr_env_name}"
                envInfo.append(EnvironmentName)
                envInfo.append(os.path.join(cur_dir, ProjectFilePath))
                envInfo.append(os.path.join(cur_dir, MappingFilePath))
                
                envInfo.append(self.emr_env_node[emr_env_name])
                envInfos.append(envInfo)
                self.emr_env_names[emr_env_name] = EnvironmentName

        return envInfos,os.path.join(cur_dir,".em/EEProject/.publish")

    def get_local_mrt_version(self):
        return self.mrt_version()

    def get_mrtd_server_version(self):
        self.connet()
        return self.mrtd_version()

    def load_env_for_EmProject(self, is_startEnv=True, is_destoryEnv_ifExist=False):

        temp_dir = self._temp_dir
        if not os.path.exists(temp_dir):

            os.mkdir(temp_dir)
        shutil.rmtree(temp_dir)
        ec = self.connet()
        if not (ec.value == 0):
            msg = f"connect rtpc fail {ec.value}"
            self.mrt_clien_Log.error(msg)
            raise Exception(msg)

        for env_name, ip_project_path, mapping_path, node in self._emrInfo:
            if node != self.server_name:
                continue
            project = os.path.dirname(ip_project_path)
            is_env_exists = self.is_env_exists(env_name)
            if is_destoryEnv_ifExist:
                if is_env_exists:
                    self._close_env_by_name(env_name)
                    is_env_exists = False
                    time.sleep(1)
            if not is_env_exists:
                ec = self.create_test_env(env_name)
                if not (ec.value == 0):
                    msg = f"create test env {env_name} fail {ec.value}"
                    self.mrt_clien_Log.error(msg)
                    raise Exception(msg)
                self.mrt_clien_Log.info(f"create test env:{env_name} success!")
                ec, map_id = self.download_file(mapping_path)
                if ec.value != 0:
                    msg = f"download mapping file fail {ec.value}"
                    self.mrt_clien_Log.error(msg)
                    raise Exception(msg)
                ec = self.load_enviroment_interface_mapping(env_name, map_id)
                if ec.value != 0:
                    msg = f"load enviroment interface mapping fail {ec.value}"
                    self.mrt_clien_Log.error(msg)
                    raise Exception(msg)
                zipfile = os.path.join(temp_dir, env_name)
                env_build_path = kunyi_util.file_compress(project, zipfile)
                ec, file_id = self.download_file(env_build_path)
                time.sleep(1)
                if not (ec.value == 0):
                    msg = "Dispatch ip project to rtpc fail"
                    self.mrt_clien_Log.error(msg)
                    raise Exception(msg)
                while True:
                    value = mrt_client.dispatch_progress
                    if value >= 1:
                        if value > 1:
                            msg = "Dispatch ip project to rtpc fail in the middle"
                            self.mrt_clien_Log.error(msg)
                            raise Exception(msg)
                        ecc = self.load_test_resources_to_env(env_name, file_id)
                        if not (ecc.value == 0):
                            msg = "Load project in env %s fail" % (env_name)
                            self.mrt_clien_Log.error(msg)
                            raise Exception(msg)
                        self.mrt_clien_Log.info(("Load project in env:%s success!" % (env_name)))
                        break
            ec, env_info = self.get_env_info(env_name)
            if is_startEnv:
                if env_info.contents.running_status == 0:
                    ec = self.start_test(env_name)
                    if ec.value != 0:
                        msg = "Start test fail due to %s" % (ec.get_name())
                        self.mrt_clien_Log.error(msg)
                        raise Exception(msg)
                    self.mrt_clien_Log.info(f"start env:{env_name} success!")
            ec, env_info = self.get_env_info(env_name)
            if env_info.contents.running_status == 0:
                raise Exception("Env %s is not started" %(env_name))


    def get_env_by_emr_envName(self,emr_envName):
        if len(self.emr_env_names)<1:
            return None

        if emr_envName in self.emr_env_names:
            return self.emr_env_names[emr_envName]
        else:
            return None

    def get_ipr_by_emr_envName(self,emr_envName):
        if len(self.emr_env_names)<1:
            return None

        if emr_envName in self.emr_env_iprs:
            return self.emr_env_iprs[emr_envName]
        else:
            return None

    def get_project_by_emr_envName(self,emr_envName):
        if len(self.emr_env_names)<1:
            return None
        pro = self.emr_env_projects[emr_envName]
        return pro


    def get_signal_dataType_itemCount_structName_structDetail(self,emr_envName, instance_name,portType,port_name):
        '''
        :param env_name:
        :param instance_name:
        :param portType: inputports, outputports, measurements, calibrations
        :param port_name:
        :return:
        '''

        pro = self.get_project_by_emr_envName(emr_envName)
        env_pro_name = self.get_env_by_emr_envName(emr_envName)
        signal_type,item_count,port_type_id,struct_name, is_queue = pro.get_dataType_itemcount(instance_name,portType,port_name)
        struct_detail = pro.get_struct_detail(instance_name,struct_name)

        return env_pro_name,port_type_id,signal_type,item_count,struct_detail,is_queue

    def get_all_signal_dataType_itemCount_structName_structDetail(self,emr_envName, instance_name,portType):
        '''
        :param env_name:
        :param instance_name:
        :param portType: inputports, outputports, measurements, calibrations
        :return:
        '''
        port_detail_list = []
        pro = self.get_project_by_emr_envName(emr_envName)
        env_pro_name = self.get_env_by_emr_envName(emr_envName)
        port_name_list = pro.get_portName_list_by_portType(instance_name,portType)
        for port_name in port_name_list:
            signal_type,item_count,st_id,struct_name,is_queue = pro.get_dataType_itemcount(instance_name,portType,port_name)
            struct_detail = pro.get_struct_detail(instance_name,struct_name)
            port_detail = (env_pro_name,port_name,signal_type,item_count,struct_detail)
            port_detail_list.append(port_detail)

        return port_detail_list

    def get_inputport_all_signal_dataType_itemCount_structName_structDetail(self, emr_envName, instance_name):
        '''
        :param emr_envName:
        :param instance_name:
        :return:
        '''

        return self.get_all_signal_dataType_itemCount_structName_structDetail(emr_envName, instance_name,"InputPorts")

    def get_outputport_all_signal_dataType_itemCount_structName_structDetail(self, emr_envName, instance_name):
        '''
        :param emr_envName:
        :param instance_name:
        :return:
        '''

        return self.get_all_signal_dataType_itemCount_structName_structDetail(emr_envName, instance_name, "OutputPorts")

    def write_input_port_value(self, emr_envName, instance_name, port_name, signal_value, **sub_struct_detail):

        portType = "inputport"
        env_pro_name , port_type_id , signal_type, item_count, struct_detail ,is_queue = \
            self.get_signal_dataType_itemCount_structName_structDetail(emr_envName, instance_name,portType,port_name)
        return self.set_port_value(env_pro_name, instance_name, port_name,
                                   signal_type, signal_value, mrt_port_type_t.MRT_INPUT_PORT,
                                   item_count, struct_detail, **sub_struct_detail)


    def write_cal_Scalar_port_value(self, emr_envName, instance_name, port_name,cal_value_array):
        pro = self.get_project_by_emr_envName(emr_envName)
        env_name = self.get_env_by_emr_envName(emr_envName)
        portType = "Calibration"
        cal_type = "Scalar"
        sn, stid, data_type = pro.get_Calibrations(instance_name, portType, cal_type, port_name)

        return self.set_calibration(env_name, instance_name, port_name, data_type , cal_value_array = cal_value_array)

    def write_cal_Vector_port_value(self, emr_envName, instance_name, port_name,cal_value_array,funlength,funidx = 0):
        pro = self.get_project_by_emr_envName(emr_envName)
        env_name = self.get_env_by_emr_envName(emr_envName)
        portType = "Calibration"
        cal_type = "Vector"
        sn, stid, data_type = pro.get_Calibrations(instance_name, portType, cal_type, port_name)

        return self.set_calibration(env_name, instance_name, port_name,
                                    data_type , funlength=funlength, funidx=funidx,cal_value_array = cal_value_array)

    def write_cal_Curve_port_value(self, emr_envName, instance_name, port_name,cal_value_array,funlength,xlength):
        pro = self.get_project_by_emr_envName(emr_envName)
        env_name = self.get_env_by_emr_envName(emr_envName)
        portType = "Calibration"
        cal_type = "Curve"
        sn, stid, data_type = pro.get_Calibrations(instance_name, portType, cal_type, port_name)

        return self.set_calibration(env_name, instance_name, port_name,
                                    data_type , funlength=funlength, xlength=xlength,cal_value_array = cal_value_array)

    def write_cal_Map_port_value(self, emr_envName, instance_name, port_name,cal_value_array,funlength,xlength,ylength):
        pro = self.get_project_by_emr_envName(emr_envName)
        env_name = self.get_env_by_emr_envName(emr_envName)
        portType = "Calibration"
        cal_type = "Map"
        sn, stid, data_type = pro.get_Calibrations(instance_name, portType, cal_type, port_name)

        return self.set_calibration(env_name, instance_name, port_name,
                                    data_type , funlength=funlength, xlength=xlength,
                                    ylength=ylength,cal_value_array = cal_value_array)

    def read_input_port_value(self, emr_envName, instance_name, port_name,**sub_struct_detail):

        portType = "inputport"
        env_pro_name , port_type_id , signal_type, item_count, struct_detail,is_queue = \
            self.get_signal_dataType_itemCount_structName_structDetail(emr_envName, instance_name, portType, port_name)
        return self.get_port_value(env_pro_name, instance_name, port_name,
                                   mrt_port_type_t.MRT_INPUT_PORT, signal_type, item_count, struct_detail, **sub_struct_detail)

    def read_output_port_value(self, emr_envName, instance_name, port_name,**sub_struct_detail):

        portType = "outputport"
        env_pro_name , port_type_id , signal_type, item_count, struct_detail, is_queue = \
            self.get_signal_dataType_itemCount_structName_structDetail(emr_envName, instance_name, portType, port_name)
        return self.get_port_value(env_pro_name, instance_name, port_name,
                                   mrt_port_type_t.MRT_OUTPUT_PORT, signal_type, item_count, struct_detail, **sub_struct_detail)

    def read_measurement_port_value(self, emr_envName, instance_name, port_name,**sub_struct_detail):

        portType ="measurements"
        env_pro_name , port_type_id , signal_type, item_count, struct_detail, is_queue = \
            self.get_signal_dataType_itemCount_structName_structDetail(emr_envName, instance_name, portType, port_name)
        return self.get_port_value(env_pro_name, instance_name, port_name,
                                   mrt_port_type_t.MRT_MEASUREMENT, signal_type, item_count, struct_detail, **sub_struct_detail)

    def read_cal_Scalar_port_value(self, emr_envName, instance_name, port_name):

        pro = self.get_project_by_emr_envName(emr_envName)
        env_name = self.get_env_by_emr_envName(emr_envName)
        portType = "Calibration"
        cal_type = "Scalar"
        sn, stid, data_type  = pro.get_Calibrations(instance_name,portType,cal_type,port_name)

        return self.get_calibration(env_name,instance_name,port_name,data_type)

    def read_cal_Vector_port_value(self, emr_envName, instance_name, port_name,funlength):

        pro = self.get_project_by_emr_envName(emr_envName)
        env_name = self.get_env_by_emr_envName(emr_envName)
        portType = "Calibration"
        cal_type = "Vector"
        sn, stid, data_type = pro.get_Calibrations(instance_name, portType, cal_type, port_name)

        return self.get_calibration(env_name, instance_name, port_name, data_type,funlength=funlength)

    def read_cal_Curve_port_value(self, emr_envName, instance_name, port_name,funlength,xlength):

        pro = self.get_project_by_emr_envName(emr_envName)
        env_name = self.get_env_by_emr_envName(emr_envName)
        portType = "Calibration"
        cal_type = "Curve"
        sn, stid, data_type = pro.get_Calibrations(instance_name, portType, cal_type, port_name)

        return self.get_calibration(env_name, instance_name, port_name, data_type,funlength=funlength,xlength=xlength)

    def read_cal_Map_port_value(self, emr_envName, instance_name, port_name,funlength,xlength,ylength):

        pro = self.get_project_by_emr_envName(emr_envName)
        env_name = self.get_env_by_emr_envName(emr_envName)
        portType = "Calibration"
        cal_type = "Map"
        sn, stid, data_type = pro.get_Calibrations(instance_name, portType, cal_type, port_name)

        return self.get_calibration(env_name, instance_name, port_name, data_type,
                                    funlength=funlength,xlength=xlength,ylength=ylength)

    def capture_signal_data(self,capture_signals,is_queue = 0 , daq_period = 200,run_time_s = 3):
        '''

        :param capture_signals: eg: capture_signals = {"env_1":[("expression_1","inputport","x[0]"),
                            ("expression_1","outputport","y[0]")
                            ]
                   }
        :param is_queue:
        :param daq_period:
        :param run_time_s:
        :return:
        '''

        port_metas = {}
        env_name = ''
        daq_handle = 0
        for emr_env_name,signal_list in capture_signals.items():
            daq_num = len(signal_list)
            env_name= self.get_env_by_emr_envName(emr_env_name)
            is_env_exists = self.is_env_exists(env_name)
            if not is_env_exists:
                raise Exception(f"Env: {env_name} no start!")
            ec, daq_handle = self.create_daq(env_name, daq_num, is_queue)
            if ec.value != 0:
                raise Exception(f"create daq failed! {ec.value}")
            ec,info = self.get_daq_info(env_name,daq_handle)
            if ec.value != 0:
                raise Exception(f"get daq info failed! {ec.value}")
            index = 0
            for signal_info in signal_list:
                env_name, port_type_id, signal_type, item_count, struct_detail,is_queue = \
                    self.get_signal_dataType_itemCount_structName_structDetail(emr_env_name,*signal_info)

                ec = self.daq_set_port(env_name, daq_handle, index, signal_info[0], signal_info[2], port_type_id)
                if ec.value != 0:
                    raise Exception(f"daq set port failed! {ec.value}")
                index += 1
                port_metas[(signal_info[0], signal_info[2], port_type_id[0])] = {
                    "item_count": item_count, "struct_detail": struct_detail, "datatype": signal_type}
        ec = self.daq_set_trigger_period(env_name, daq_handle, daq_period, 0)
        if ec.value != 0:
            raise Exception(f"daq set trigger period failed! {ec.value}")
        time.sleep(0.1)
        ec = self.start_daq(env_name, daq_handle)
        if ec.value != 0:
            raise Exception(f"start daq failed! {ec.value}")
        start_time = time.time()
        info_dic = {}
        while True:
            time.sleep(daq_period/1000)
            info_ = {}
            message = self.daq_read(env_name, daq_handle, port_metas)
            for signals in message:
                for signal in signals:
                    timeStamp = datetime.datetime.utcfromtimestamp(signal[4] / 1000000).strftime('%m/%d %H:%M:%S.%f')
                    if f"{signal[0]}/{signal[1]}" not in info_dic:
                        info_dic[f"{signal[0]}/{signal[1]}"] = []
                    info_dic[f"{signal[0]}/{signal[1]}"].append(signal[3])
                    if f"{signal[0]}/{signal[1]}" not in info_:
                        info_[f"{signal[0]}/{signal[1]}"] = []
                    info_[f"{signal[0]}/{signal[1]}"].append(signal[3])
                    # info = f"\n{timeStamp}: {signal[0]}/{signal[1]}value: {signal[3]}"
            self.mrt_clien_Log.info(info_)
            if time.time() - start_time > run_time_s:
                self.mrt_clien_Log.info(info_dic)
                return info_dic

    def fetch_data(self, env_name, instance_name, port_name, port_type, frenquency=1, timeout=30):
        port_type_dict = {
            0: "inputport",
            1: "outputport",
            2: "measurement"
        }
        rtpc_env_name = self.emr_env_names[env_name]
        rc, env_info = self.get_env_info(rtpc_env_name)

        rc, daq_handle = self.create_daq(rtpc_env_name, 1, 0)
        env_pro_name, port_type_id, signal_type, item_count, struct_detail, is_queue = \
            self.get_signal_dataType_itemCount_structName_structDetail(env_name, instance_name,
                                                                         port_type_dict[port_type],
                                                                         port_name)
        rc = self.daq_set_port(rtpc_env_name, daq_handle, 0, instance_name, port_name, [port_type])
        port_metas = {}
        port_metas[(instance_name, port_name, port_type)] = {
            "item_count": item_count, "struct_detail": struct_detail, "datatype": signal_type}
        rc = self.daq_set_trigger_period(rtpc_env_name, daq_handle, frenquency, 0)
        self.start_daq(rtpc_env_name, daq_handle)
        start_time = time.time()
        all_values = []
        last_value = []
        while (time.time() - start_time < timeout):
            messages = self.daq_read(rtpc_env_name, daq_handle, port_metas)
            if len(messages) == 0:
                continue
            for msg in messages:
                if len(last_value) == 0:
                    all_values.append((msg[0][3],msg[0][4]))
                    last_value.append(msg[0][3])
                    last_value.append(msg[0][4])
                else:
                    if msg[0][3] != last_value[0]:
                        all_values.append((last_value[0],last_value[1]))
                        all_values.append((msg[0][3], msg[0][4]))
                        last_value[0] = msg[0][3]
                        last_value[1] = msg[0][4]
        if len(last_value) == 1:
            all_values.append((last_value[0],last_value[1]))
        self.stop_daq(rtpc_env_name, daq_handle)
        self.destroy_daq(rtpc_env_name, daq_handle)
        return all_values

    def get_duration(self, orig_env, instance, port_type, port_name, expect_value, expect_op, timeout):
        rtpc_env_name = self.emr_env_names[orig_env]
        rc, env_info = self.get_env_info(rtpc_env_name)
        try:
            eval_str = expect_op + " " + str(expect_value)
            start_time = time.time()
            start_eval = None
            clock_start = None
            duration = None
            while (time.time() - start_time < timeout):
                call_s = time.time()
                if port_type == 0:
                    value = my_mrt.read_input_port_value(orig_env, instance, port_name)
                elif port_type == 1:
                    value = my_mrt.read_output_port_value(orig_env, instance, port_name)
                elif port_type == 2:
                    value = my_mrt.read_measurement_port_value(orig_env, instance, port_name)
                call_e = time.time() - call_s
                if value[0] == 0:
                    continue
                real_eval_str = str(value[1]) + " " + eval_str
                if start_eval is None:
                    if not eval(real_eval_str):
                        continue
                    else:
                        start_eval = True
                        clock_start = time.time() + call_e / 2

                else:
                    if not eval(real_eval_str):
                        duration = time.time() - clock_start
                        break
            if start_eval is None:
                return 0
            if start_eval and (duration is None):
                raise Exception(
                    "Data is still meed the expectation after timeout, please consider increase the timeout")
            ee = time.time() - es
            return round((duration * 1000), 3)
        except Exception as e:
            raise Exception("Test step fail due to %s" % (e))

