import os
import time
import sys
r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(rootpath)
from vcarhilclient.kunyi_project import *
from vcarhilclient.kunyi_mrt import *
from vcarhilclient.Enums import *
from vcarhilclient.signal_daq import *
import random
import string
import shutil
import pretty_errors

class meta_format(Enum):
    name_only = 1,
    meta_tuple = 2,
    meta_dict = 3,
    meta_orig = 4


class hil_test():
    def __init__(self, ipr_path, mrt_client, env_name=None,mapping_path=None,temp_dir = r'c:\zip_dir'):
        self.project = hil_project(ipr_path)
        self.mrt_client = mrt_client
        ec = self.mrt_client.connet()
        self.mapping_path = mapping_path
        self.temp_dir = temp_dir
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)
        self.Reconnection_state = 0
        self.__current_env_name = env_name
        self.signal_daq = signal_daq(self.mrt_client, self.__current_env_name)
        self.isrestore = False

    def load_enviroment_mapping(self):
        if self.mapping_path is None:
            return
        ec, map_id = self.mrt_client.download_file(self.mapping_path)
        if ec.value != 0:
            raise Exception(f"download mapping file fail {ec.value}")
        ec = self.mrt_client.load_enviroment_interface_mapping(self.__current_env_name,map_id)
        if ec.value != 0:
            raise Exception(f"load enviroment interface mapping fail {ec.value}")

    def start_test(self):
        #if self.is_test_running():
        #    return
        ec = self.mrt_client.start_test(self.__current_env_name)
        if ec.value != 0:
            raise Exception("Start test fail due to %s" %(ec.get_name()))
        return ec.get_name()


    def end_test(self):
        if not self.is_test_running():
            return
        ec = self.mrt_client.stop_test(self.__current_env_name)
        if ec.value != 0:
            raise Exception("End test fail due to %s" %(ec.get_name()))

    def close(self):
        self.signal_daq.keep_fetch = False
        self.end_test()
        rc = self.mrt_client.delete_test_env(self.__current_env_name)
        if rc.value != 0:
            with open("./readErro.erro", "a") as f:
                f.write(f"{time.strftime('%m%d_%H:%M:%S')}:Delete test env {self.__current_env_name} fail, rc is{str(rc.value)}\n")
            print("Delete test env %s fail, rc is %s " %(self.__current_env_name, str(rc.value)))
        return rc.value

    def close_env_name(self,envName):
        if not self.is_test_running():
            return
        ec = self.mrt_client.stop_test(envName)
        if ec.value != 0:
            raise Exception("End test fail due to %s" %(ec.get_name()))
        rc = self.mrt_client.delete_test_env(self.__current_env_name)
        if rc.value != 0:
            with open("./readErro.erro", "a") as f:
                f.write(
                    f"{time.strftime('%m%d_%H:%M:%S')}:Delete test env {self.__current_env_name} fail, rc is{str(rc.value)}\n")
            print("Delete test env %s fail, rc is %s " % (self.__current_env_name, str(rc.value)))

    def list_instances(self):
        return self.project.instances.keys()

    def get_calInfo(self,instance,signal_type,cal_type,signal_name):
        calName , stid , datatype = self.project.get_Calibrations(instance,signal_type,cal_type,signal_name)
        return calName , stid ,datatype

    def write_cal(self, env_name, instance_name, cal_name,cal_datatype, xlength=0, ylength=0, funlength=1,
                        xidx=0, yidx=0, funidx=0, cal_value_array=[]):

        return  self.mrt_client.set_calibration(env_name, instance_name, cal_name,
                        cal_datatype, xlength, ylength, funlength,xidx, yidx, funidx, cal_value_array)

    def read_cal(self, env_name, instance_name, cal_name,cal_datatype, xlength=0, ylength=0, funlength=1,xidx=0, yidx=0, funidx=0):

        return  self.mrt_client.get_calibration(env_name, instance_name, cal_name,cal_datatype, xlength, ylength, funlength,
                        xidx, yidx, funidx)

    def get_signalInfo(self,instance,signal_type,signal_name):
        dataType , itemcount , sid , struct , is_queue = self.project.get_dataType_itemcount(instance,signal_type,signal_name)

        return dataType ,itemcount,sid

    def writePort(self, env_name, instance_name, port_name, signal_type, signal_value,
                       port_type, item_count, struct_detail=None, **sub_struct_detail):
        rc = self.mrt_client.set_port_value(env_name, instance_name, port_name, signal_type, signal_value,
                       port_type, item_count, struct_detail, **sub_struct_detail)
        expect_size = self.expect_valueSize(signal_type)
        if rc == expect_size:
            print("Set the value successfully.")
            return 1
        else:
            print(f"Failed to set the value,reCode:{rc}")
            return 0

    def readPort(self, env_name, instance_name, port_name, signal_type,
                  port_type, item_count, struct_detail=None, **sub_struct_detail):
        rc,value = self.mrt_client.get_port_value(env_name, instance_name, port_name, port_type,
                                            signal_type,  item_count, struct_detail, **sub_struct_detail)
        expect_size = self.expect_valueSize(signal_type)
        if rc == expect_size:
            print(f"Get the signal[{port_name}] value successfully. signalValue:{value}")
            return value, 1
        else:
            print("Failed to get the value")
            return None, 0


    def list_input_ports(self, instance_name, format=meta_format.meta_orig):
        if not instance_name in self.project.instances:
            return None
        all_input_ports = self.project.get_instance_items(instance_name, "InputPorts")
        if format == meta_format.name_only:
            name_list = []
            for port in all_input_ports.values():
                name_list.append(port["Name"])
            return name_list
        elif format == meta_format.meta_dict:
            return all_input_ports
        elif format == meta_format.meta_tuple:
            tuple_list = []
            for port in all_input_ports.values():
                tuple_list.append((instance_name, port["Name"], "InputPorts"))
            return tuple_list
        else:
            return list(all_input_ports.values())

    def list_output_ports(self, instance_name, format=meta_format.meta_orig):
        if not instance_name in self.project.instances:
            return None
        all_output_ports = self.project.get_instance_items(instance_name, "OutputPorts")
        if format == meta_format.name_only:
            name_list = []
            for port in all_output_ports.values():
                name_list.append(port["Name"])
            return name_list
        elif format == meta_format.meta_dict:
            return all_output_ports
        elif format == meta_format.meta_tuple:
            tuple_list = []
            for port in all_output_ports.values():
                tuple_list.append((instance_name, port["Name"], "OutputPorts"))
            return tuple_list
        else:
            return list(all_output_ports.values())

    def list_measurements(self, instance_name, format=meta_format.meta_orig):
        if not instance_name in self.project.instances:
            return None
        all_measurements = self.project.get_instance_items(instance_name, "Measurements")
        if format == meta_format.name_only:
            name_list = []
            for port in all_measurements.values():
                name_list.append(port["Name"])
            return name_list
        elif format == meta_format.meta_dict:
            re_dict = {}
            for port in all_measurements.values():
                re_dict["Name"] = port
        elif format == meta_format.meta_tuple:
            tuple_list = []
            for port in all_measurements.values():
                tuple_list.append((instance_name, port["Name"], "Measurements"))
            return tuple_list
        else:
            return list(all_measurements.values())

    def list_calibrations(self, instance_name, format=meta_format.name_only):
        if not instance_name in self.project.instances:
            return None
        calibrations = {}
        all_scalar = self.project.get_instance_items(instance_name, "Calibrations.Scalar")
        calibrations["scalars"] = all_scalar
        all_vector = self.project.get_instance_items(instance_name, "Calibrations.Vector")
        calibrations["vectors"] = all_vector
        all_map = self.project.get_instance_items(instance_name, "Calibrations.Map")
        calibrations["maps"] = all_map
        all_curve = self.project.get_instance_items(instance_name, "Calibrations.Curve")
        calibrations["curves"] = all_curve
        return calibrations

    def monitor_signals(self, signal_list):
        list_with_datatype = []
        # The signal item is tuple of instance name, port name and port type
        for signal in signal_list:
            item_detail = self.project.get_instance_item(signal[0], signal[1], signal[2])
            item_datatype = item_detail["Type"]
            list_with_datatype.append((signal[0], signal[1], signal[2], item_datatype))
        self.signal_daq.add_monitoring_singals(list_with_datatype)


    def fetch_values(self, instance_ports,
                             fetch_datatype=fetch_value_datatype.RAW):
        all_results = []

        for port in instance_ports:
            item_detail = self.project.get_instance_item(port[0], port[1], port[2])
            if item_detail is None:
                continue
            item_datatype = item_detail["Type"]
            mrt_port_type = kunyi_util.string_to_mrt_signal_type(port[2])
            portInfo = (port[0], port[1], mrt_port_type[0])
            if portInfo in self.signal_daq.full_signal_buffers:
                item_value = self.signal_daq.pop(portInfo)
                if item_value is not None:
                    r_item = (port[0], port[1], port[2], item_value[0], item_value[1])
                    all_results.append(r_item)

            else:
                item_value = self.mrt_client.get_outputPort_value(self.__current_env_name,
                                                            port[0], port[1], mrt_port_type, item_datatype,
                                                            1, None)
                r_item = (port[0], port[1], port[2], item_value[1], 0)
                all_results.append(r_item)
        return all_results

    def fetch_calibration_values(self, cal_infos, fetch_type=fetch_value_type.ON_DEMAND,
                                 fetch_datatype=fetch_value_datatype.RAW, **filters):
        all_results = []
        for item in cal_infos:
            item_detail = self.project.get_instance_item(item[0], item[1], "Calibrations.%s" %(item[2]))
            if item_detail is None:
                continue
            if "Value" in item_detail:
                item_datatype = item_detail["Value"]["DataType"]
            elif "Values" in item_detail:
                item_datatype = item_detail["Values"]["DataType"]
            else:
                # Struct type does not support yet
                return None
            if item[2] == "Scalar":
                item_value = self.mrt_client.get_calibration_value(self.__current_env_name, item[0], item[1],
                                                               0, 0, 1, item_datatype)
            else:
                # Vector, Map, Curve do not supported yet
                return None
            r_item = (item[0], item[0], item_value[0])
            all_results.append(r_item)
        return all_results

    def update_input_port_values(self, instance_port_tuple, newvalue):
        input_port_meta = self.project.get_instance_item("VectorCAN_1", "Inport", "InputPorts")


        port_detail = self.project.get_instance_item(instance_port_tuple[0], instance_port_tuple[1], instance_port_tuple[2])
        port_struct = self.project.get_instance_item(instance_port_tuple[0], port_detail["RefStruct"], "Structs")
        all_structs = self.project.get_instance_items(instance_port_tuple[0], "Structs")
        self.mrt_client.set_input_port_value()

    def update_calibration_values(self, instance_port_pairs, newvalue):
        pass

    def set_input_port_values(self,instance_name, port_name, signal_type,signal_value,item_count, struct_detail=None, **sub_struct_detail):
        rc = self.mrt_client.set_input_port_value(self.__current_env_name, instance_name, port_name, signal_type, signal_value, item_count,
                                       struct_detail, **sub_struct_detail)

        expect_size = self.expect_valueSize(signal_type)
        if rc == expect_size:
            print("Set the value successfully.")
            return 1
        else:
            print(f"Failed to set the value,recode:{rc}")
            return 0

    def get_inputPort_value(self, instance_name, port_name, signal_type, item_count, struct_detail=None,
                             **sub_struct_detail):
        rc, value = self.mrt_client.get_input_port_value(self.__current_env_name, instance_name, port_name,
                                                          signal_type, item_count, struct_detail, **sub_struct_detail)

        expect_size = self.expect_valueSize(signal_type)
        if rc == expect_size:
            print("Get the value successfully.")
            return value, 1
        else:
            print("Failed to get the value")
            return None, 0

    def get_outputPort_value(self,instance_name, port_name, signal_type,item_count,struct_detail=None, **sub_struct_detail):
        rc,value= self.mrt_client.get_output_port_value(self.__current_env_name, instance_name, port_name, signal_type,item_count,struct_detail, **sub_struct_detail)

        expect_size = self.expect_valueSize(signal_type)
        if rc == expect_size:
            print("Get the value successfully.")
            return value , 1
        else:
            print("Failed to get the value")
            return None , 0

    def get_measurementPort_value(self, instance_name, port_name, signal_type, item_count, struct_detail=None,
                             **sub_struct_detail):
        rc, value = self.mrt_client.get_measurement_value(self.__current_env_name, instance_name, port_name,
                                                          signal_type, item_count, struct_detail, **sub_struct_detail)

        expect_size = self.expect_valueSize(signal_type)
        if rc == expect_size:
            print("Get the value successfully.")
            return value, 1
        else:
            print("Failed to get the value")
            return None, 0

    def expect_valueSize(self,signal_type):
        type_dict = {"Int8": 1,
                     "Int16": 2,
                     "Int32": 4,
                     "Int64": 8,
                     "UInt8": 1,
                     "UInt16": 2,
                     "UInt32": 4,
                     "UInt64": 8,
                     "Float": 4,
                     "Double": 8,
                     "Bool": 1,
                     "ASCII": 2000,
                     "UTF8": 2000}
        expect_size = type_dict[signal_type]
        return expect_size

    def prepare_test_env(self, timeout=30,is_start_env = True):

        if self.__current_env_name is  None:
            self.__current_env_name = ''.join(random.choices(string.ascii_lowercase, k=10))
        else:
            ec, info = self.mrt_client.get_env_info(self.__current_env_name)
            if ec.value == 0:
                if info.contents.running_status == 1 and self.isrestore:
                    # raise Exception("There is a running test in rtpc, please stop the test before "
                    #                 "your re-dispatch ip project")
                    if self.restore_env():
                        while True:
                            command = input(f"An experiment of the same name({self.__current_env_name}) is running in RTPC!\n"
                                            "Please select Restore(input:1),Destroy and recreate(input:2) "
                                            "or Destroy and Exit(enter:Ctrl + C + Enter)\n:")
                            if command == "1":
                                self.Reconnection_state = 1
                                self.mrt_client.log_write(1,f"{self.__current_env_name}",f"Reconnection env:{self.__current_env_name}")
                                print(f"\nReconnection env:{self.__current_env_name}...")
                                break
                            elif command == "2":
                                self.close()
                                self.signal_daq.daq_handle = None
                                self.prepare_test_env()
                                break
                            else:
                                continue
                    else:
                        while True:
                            command = input(f"An experiment of the same name({self.__current_env_name}) is running in RTPC!\n"
                                            "This environment could't connect,Please select Destroy and"
                                            " recreate(input:2) or Destroy and Exit(enter:Ctrl + C + Enter)\n:")
                            if command == "2":
                                self.close()
                                self.signal_daq.daq_handle = None
                                self.prepare_test_env()
                                break
                            else:
                                continue
                elif info.contents.running_status == 1:
                    self.close()
                    self.signal_daq.daq_handle = None
                    self.prepare_test_env()
            else:
                ec = self.mrt_client.create_test_env(self.__current_env_name)
                if not (ec.value == 0):
                    self.mrt_client.log_write(3, f"{self.__current_env_name}","create test env %s fail" % (self.__current_env_name))
                    raise Exception(f"create test env {self.__current_env_name} fail {ec.value}")
                self.load_enviroment_mapping()
                zipfile = os.path.join(self.temp_dir, self.__current_env_name)
                temp_dir = kunyi_util.file_compress(self.project.project_root_dir, zipfile)
                ec, file_id = self.mrt_client.download_file(temp_dir)
                time.sleep(1)

                if not (ec.value == 0):
                    raise Exception("Dispatch ip project to rtpc fail")
                start_time = time.time()
                while (time.time() - start_time) < timeout:
                    value = mrt_client.dispatch_progress
                    if value >= 1:
                        if value > 1:
                            raise Exception("Dispatch ip project to rtpc fail in the middle")

                        ecc = self.mrt_client.load_test_resources_to_env(self.__current_env_name, file_id)
                        if not (ecc.value == 0):
                            self.mrt_client.log_write(3, f"{self.__current_env_name}","Load project in env %s fail" % (self.__current_env_name))
                            raise Exception("Load project in env %s fail" % (self.__current_env_name))
                        if is_start_env:
                            self.start_test()
                        return self.__current_env_name
                    time.sleep(1)
                raise Exception("Dispatch ip project to rtpc take more than %s second" % (str(timeout)))

    def is_test_running(self):
        ec, info = self.mrt_client.get_env_info(self.__current_env_name)
        if ec.value != 0:
            return False
        if info.contents.running_status == 1:
            return True
        return False

    def enable_logging(self,  log_path, fetch_period=3):
        reader = self.mrt_client.open_log_reader()
        if reader == None:
            raise Exception("Enable logging fail")
        self.logging_enabled = True

        new_t = Thread(target=self.__fetch_log, args=(log_path, fetch_period,))
        new_t.start()


    def __fetch_log(self, log_path, fetch_period):
        log_name = self.project.project_name + "_" + self.project.system_id + "_" + self.__current_env_name
        log_idx = 1
        while self.logging_enabled:
            try:
                logs = self.mrt_client.fetch_log(4098)
                log_file = os.path.join(log_path, log_name + ".log")
                with open(log_file, 'a+') as log_f:
                    log_f.write(logs)
                    log_f.write("\r\n")
                # Logging rotate per every 100M
                if os.path.getsize(log_file) > 104857600:
                    achive_file = os.path.join(log_path, log_name + str(log_idx) + ".log")
                    os.rename(log_file, achive_file)
                    log_idx = log_idx + 1
                time.sleep(fetch_period)
            except Exception as ex:
                print(sys.exc_info()[2])
                continue

    def disable_logging(self):
        self.logging_enabled = False

    def update_ip_project(self):
        if self.__current_env_name != None:
            if self.is_test_running():
                raise Exception("There is a running test in rtpc, please stop the test before "
                                "your re-dispatch ip project")


        # delete current env
        # update project by create a new hil project
        else:
            pass
    def restore_env(self,):
        try:
            with open("./daqinfo.txt", "r") as f:
                daq_handle = int(f.read())
                ec, info = self.mrt_client.get_daq_info(self.__current_env_name, daq_handle)
                if ec.value == 0:
                    self.signal_daq.daq_handle = daq_handle
                return True
        except:
            return False

    def get_mrtClientVersion(self):
        v = self.mrt_client.mrt_version()
        return v

    def get_rtpcVersion(self):
        v = self.mrt_client.mrtd_version()
        return v








