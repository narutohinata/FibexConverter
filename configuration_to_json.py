#!/usr/bin/python3

from io import TextIOWrapper
import sys
import time
import os.path
import glob
import json

from configuration_base_classes import *  

from fibex_parser import FibexParser

depressionLevel = 0
# 0 - no depression, readable 
# 1 - depression without information missing
# 2 - depression wtih information missing

class SimpleConfigurationFactory(BaseConfigurationFactory):

    def create_ecu(self, name, controllers):
        ret = ECU(name, controllers)
        return ret

    def create_controller(self, name, vlans):
        ret = Controller(name, vlans)
        return ret

    def create_interface(self, name, vlanid, sockets):
        ret = Interface(name, vlanid, sockets)
        return ret

    def create_socket(self, name, ip, proto, portnumber, serviceinstances, serviceinstanceclients, eventhandlers,
                      eventgroupreceivers):
        ret = Socket(name, ip, proto, portnumber, serviceinstances, serviceinstanceclients, eventhandlers,
                     eventgroupreceivers)
        return ret

    def create_someip_service_instance(self, service, instanceid, protover, identifer):
        ret = SOMEIPServiceInstance(service, instanceid, protover, identifer)
        return ret

    def create_someip_service_instance_client(self, service, instanceid, protover, server):
        ret = SOMEIPServiceInstanceClient(service, instanceid, protover, server)
        return ret

    def create_someip_service_eventgroup_sender(self, serviceinstance, eventgroupid):
        ret = SOMEIPServiceEventgroupSender(serviceinstance, eventgroupid)
        return ret

    def create_someip_service_eventgroup_receiver(self, serviceinstance, eventgroupid, sender):
        ret = SOMEIPServiceEventgroupReceiver(serviceinstance, eventgroupid, sender)
        return ret

    def create_someip_service(self, name, package, serviceid, majorver, minorver, methods, events, fields, eventgroups):
        ret = SOMEIPService(name, package, serviceid, majorver, minorver, methods, events, fields, eventgroups)
        return ret

    def create_someip_service_method(self, name, methodid, calltype, relia, inparams, outparams,
                                     reqdebounce=-1, reqmaxretention=-1, resmaxretention=-1, tlv=False):
        ret = SOMEIPServiceMethod(name, methodid, calltype, relia, inparams, outparams,
                                  reqdebounce, reqmaxretention, resmaxretention, tlv)
        return ret

    def create_someip_service_event(self, name, methodid, relia, params,
                                    debounce=-1, maxretention=-1, tlv=False):
        ret = SOMEIPServiceEvent(name, methodid, relia, params,
                                 debounce, maxretention, tlv)
        return ret

    def create_someip_service_field(self, name, getterid, setterid, notifierid, getterreli, setterreli, notifierreli,
                                    params,
                                    getter_debouncereq, getter_retentionreq, getter_retentionres,
                                    setter_debouncereq, setter_retentionreq, setter_retentionres,
                                    notifier_debounce, notifier_retention, tlv=False):
        ret = SOMEIPServiceField(self, name, getterid, setterid, notifierid, getterreli, setterreli, notifierreli,
                                 params,
                                 getter_debouncereq, getter_retentionreq, getter_retentionres,
                                 setter_debouncereq, setter_retentionreq, setter_retentionres,
                                 notifier_debounce, notifier_retention, tlv)
        return ret

    def create_someip_service_eventgroup(self, name, eid, eventids, fieldids):
        ret = SOMEIPServiceEventgroup(name, eid, eventids, fieldids)
        return ret

    def create_someip_parameter(self, position, name, desc, mandatory, datatype, signal):
        ret = SOMEIPParameter(position, name, desc, mandatory, datatype, signal)
        return ret

    def create_someip_parameter_basetype(self, name, datatype, bigendian, bitlength_basetype, bitlength_encoded_type):
        ret = SOMEIPParameterBasetype(name, datatype, bigendian, bitlength_basetype, bitlength_encoded_type)
        return ret

    def create_someip_parameter_string(self, name, chartype, bigendian, lowerlimit, upperlimit, termination,
                                       length_of_length, pad_to):
        ret = SOMEIPParameterString(name, chartype, bigendian, lowerlimit, upperlimit, termination, length_of_length,
                                    pad_to)
        return ret

    def create_someip_parameter_array(self, name, dims, child):
        ret = SOMEIPParameterArray(name, dims, child)
        return ret

    def create_someip_parameter_array_dim(self, dim, lowerlimit, upperlimit, length_of_length, pad_to):
        ret = SOMEIPParameterArrayDim(dim, lowerlimit, upperlimit, length_of_length, pad_to)
        return ret

    def create_someip_parameter_struct(self, name, length_of_length, pad_to, members, tlv=False):
        ret = SOMEIPParameterStruct(name, length_of_length, pad_to, members, tlv)
        return ret

    def create_someip_parameter_struct_member(self, position, name, mandatory, child, signal):
        ret = SOMEIPParameterStructMember(position, name, mandatory, child, signal)
        return ret

    def create_someip_parameter_typedef(self, name, name2, child):
        ret = SOMEIPParameterTypedef(name, name2, child)
        return ret

    def create_someip_parameter_enumeration(self, name, items, child):
        ret = SOMEIPParameterEnumeration(name, items, child)
        return ret

    def create_someip_parameter_enumeration_item(self, value, name, desc):
        ret = SOMEIPParameterEnumerationItem(value, name, desc)
        return ret

    def create_someip_parameter_union(self, name, length_of_length, length_of_type, pad_to, members):
        ret = SOMEIPParameterUnion(name, length_of_length, length_of_type, pad_to, members)
        return ret

    def create_someip_parameter_union_member(self, index, name, mandatory, child):
        ret = SOMEIPParameterUnionMember(index, name, mandatory, child)
        return ret

    def create_legacy_signal(self, id, name, compu_scale, compu_consts):
        ret = SOMEIPLegacySignal(id, name, compu_scale, compu_consts)
        return ret


class ECU(BaseECU):
    def str(self, indent):
        ret = indent * " "
        ret += f"ECU {self.__name__}\n"

        for c in self.__controllers__:
            ret += c.str(indent + 2)

        return ret


class Controller(BaseController):
    def str(self, indent):
        ret = indent * " "
        ret += f"CTRL {self.__name__}\n"
        for i in self.__interfaces__:
            ret += i.str(indent + 2)

        return ret


class Interface(BaseInterface):
    def str(self, indent):
        ret = indent * " "
        ret += f"Interface {self.__vlanname__} (VLAN-ID: 0x{self.__vlanid__:x})\n"
        for s in self.__sockets__:
            ret += s.str(indent + 2)
        return ret


class Socket(BaseSocket):
    def str(self, indent):
        ret = indent * " "
        ret += f"Socket {self.__name__} {self.__ip__}:{self.__portnumber__}/{self.__proto__}\n"
        for i in self.__instances__:
            ret += i.str(indent + 2)
        for i in self.__instanceclients__:
            ret += i.str(indent + 2)
        for c in self.__ehs__:
            ret += c.str(indent + 2)
        for c in self.__cegs__:
            ret += c.str(indent + 2)
        return ret


class SOMEIPServiceInstance(SOMEIPBaseServiceInstance):
    pass


class SOMEIPServiceInstanceClient(SOMEIPBaseServiceInstanceClient):
    def str(self, indent):
        ret = indent * " "
        ret += f"ServiceInstanceClient Service-ID: 0x{self.__service__.serviceid():04x} "
        ret += f"Version: {self.__service__.versionstring()} "
        ret += f"Instance-ID: 0x{self.__instanceid__:04x} "
        ret += f"Protover: {self.__protover__:d}\n"
        return ret


class SOMEIPServiceEventgroupSender(SOMEIPBaseServiceEventgroupSender):
    def str(self, indent):
        ret = indent * " "
        ret += f"EventgroupSender: Service-ID: 0x{self.__si__.service().serviceid():04x} "
        ret += f"Instance-ID: 0x{self.__si__.instanceid():04x} "
        ret += f"Eventgroup-ID: 0x{self.__eventgroupid__:04x}\n"
        return ret


class SOMEIPServiceEventgroupReceiver(SOMEIPBaseServiceEventgroupReceiver):
    def str(self, indent):
        ret = indent * " "
        ret += f"EventgroupReceiver: Service-ID: 0x{self.__si__.service().serviceid():04x} "
        ret += f"Instance-ID: 0x{self.__si__.instanceid():04x} "
        ret += f"Eventgroup-ID: 0x{self.__eventgroupid__:04x}\n"
        return ret


class SOMEIPService(SOMEIPBaseService):
    def json(self):

        methodDic = dict()
        fieldDic = dict()
        eventDic = dict()
        egDic = dict()
        instanceDic = dict()
        for methodid in sorted(self.__methods__):
            method:SOMEIPServiceMethod = self.__methods__[methodid]
            methodDic[method.name()] = method.json()

        for eventsid in sorted(self.__events__):
            event:SOMEIPServiceEvent = self.__events__[eventsid]
            eventDic[event.name()] = event.json()

        for fieldid in sorted(self.__fields__, key=lambda x: (x is None, x)):
            field:SOMEIPServiceField = self.__fields__[fieldid]
            fieldDic[field.name()] = field.json()

        for egid in sorted(self.__eventgroups__):
            eg:SOMEIPServiceEventgroup = self.__eventgroups__[egid]
            egDic[eg.name()] = eg.json()

        repeatDict = {}

        for instance in self.instances():
            instance:SOMEIPServiceInstance = instance
            identifer:str = instance.identifer()
            if identifer in instanceDic and instance.instanceid() != instanceDic[identifer]["instanceId"]:
                if (identifer in repeatDict):
                    repeatDict[identifer] += 1
                else:
                    repeatDict[identifer] = 1
                identifer += "_" + chr(ord('A') + repeatDict[identifer])
            instanceDic[identifer] = {
                "instanceId": instance.instanceid(),
                "ip": instance.socket().ip(),
                "proto": instance.socket().proto(),
                "port": instance.socket().portnumber()
            }
        for identifer in repeatDict:
            instanceDic[identifer + "_A"] = {
                "instanceId": instanceDic[identifer]["instanceId"],
                "ip": instanceDic[identifer]["ip"],
                "proto": instanceDic[identifer]["proto"],
                "port": instanceDic[identifer]["port"]
            }
            del instanceDic[identifer]

        return {
                "serviceId" : self.__serviceid__,
                "name" : self.name(),
                "packages" : "de." + self.__package__.absolute_path() + "." + self.name(),
                "version" : {
                    "major" : self.__major__,
                    "minor" : self.__minor__
                },
                "methods" : methodDic,
                "fields" : fieldDic,
                "events" : eventDic,
                "eventgroups" : egDic,
                "instances" : instanceDic
        }


class SOMEIPServiceMethod(SOMEIPBaseServiceMethod):
    def json(self):
        attr = {
            "name" : self.__name__,
            "methodId" : self.__methodid__,
            "reliable" : self.__reliable__,
            "inputs" : [],
            "outputs" : [],
        }
        if self.__reqdebouncetime__ >= 0:
            attr["debounce"] = self.__reqdebouncetime__
        if self.__reqretentiontime___ >= 0:
            attr["req_retention_time"] = self.__reqretentiontime___
        if self.__resretentiontime___ >= 0:
            attr["max_response_retention"] = self.__resretentiontime___

        for param in self.__inparams__:
            attr["inputs"].append(param.json())
        for param in self.__outparams__:
            attr["outputs"].append(param.json())

        return attr
    
    def json_field(self,parent:dict,t:str):
        attr = {
            "name" : self.__name__,
            "methodId" : self.__methodid__,
            "reliable" : self.__reliable__,
        }
        
        if len(self.__outparams__) != 1 or (t == "setter" and len(self.__inparams__) != 1):
            print("WARNING: Field Method has more than one Parameters")

        parent["data"] = self.__outparams__[0].json()

        return attr

class SOMEIPServiceEvent(SOMEIPBaseServiceEvent):
    def json(self):
        attr = {
            "name" : self.__name__,
            "methodId" : self.__methodid__,
            "reliable" : self.__reliable__,
            "outputs" : []
        }
        if self.__debouncetime__ >= 0:
            attr["debounce"] = self.__debouncetime__
        if self.__retentiontime___ >= 0:
            attr["retention"] = self.__retentiontime___

        for param in self.__params__:
            attr["outputs"].append(param.json())

        return attr
    
    def json_field(self,parent:dict,t:str):
        attr = {
            "name" : self.__name__,
            "methodId" : self.__methodid__,
            "reliable" : self.__reliable__,
        }
        
        if len(self.__params__) != 1:
            print("WARNING: Field Method has more than one Parameters")

        parent["data"] = self.__params__[0].json()

        return attr

class SOMEIPServiceField(SOMEIPBaseServiceField):
    def json(self):

        attr = {
            # "description" : 
            # "dataRef" : 
        }

        if self.__getter__ is not None:
            getter:SOMEIPServiceMethod = self.__getter__
            attr["getter"] = getter.json_field(attr,"getter")

        if self.__setter__ is not None:
            setter:SOMEIPServiceMethod = self.__setter__
            attr["setter"] = setter.json_field(attr,"setter")

        if self.__notifier__ is not None:
            notifier:SOMEIPServiceEvent = self.__notifier__
            attr["notifier"] = notifier.json_field(attr,"notifier")

        return attr


class SOMEIPServiceEventgroup(SOMEIPBaseServiceEventgroup):
    def json(self):
        attr = {
            "name" : self.name(),
            "id" : self.id(),
            "eventids" : self.eventids(),
            "fieldids" : self.fieldids(),
        }
        return attr


class SOMEIPParameter(SOMEIPBaseParameter):
    def json(self):
        attr = {
            "name" : self.__name__,
            "position" : self.__position__,
            # "desc" : self.__desc__,
            # "mandatory" : self.__mandatory__,
            "datatype" : self.__datatype__.json() if self.__datatype__ is not None else "None",
        }
        if self.__signal__ is not None:
            attr["signal"] = self.__signal__.json()
        return attr


class SOMEIPParameterBasetype(SOMEIPBaseParameterBasetype):
    def json(self):
        attr = {
            "name" : self.__name__,
            "type" : "SOMEIPParameterBasetype",
            "datatype" : self.__datatype__,
            "endian" : "BE",
            "bitlength_basetype" : self.__bitlength_basetype__,
            "bitlength_encoded_type" : self.__bitlength_encoded_type__,
        }
        if not self.__bigendian__:
            attr["endian"] = "LE"
        return attr

class SOMEIPParameterString(SOMEIPBaseParameterString):
    def json(self):
        attr = {
            "name" : self.__name__,
            "type" : "SOMEIPParameterString",
            "chartype" : self.__chartype__,
            "endian" : "BE",
            "lowerlimit" : self.__lowerlimit__,
            "upperlimit" : self.__upperlimit__,
            "term" : self.__termination__,
            "lengthOfLength" : self.__lengthOfLength__,
            "padTo" : self.__padTo__,
        }
        if not self.__bigendian__:
            attr["endian"] = "LE"
        return attr
    
class SOMEIPParameterArray(SOMEIPBaseParameterArray):
    def json(self):
        attr = {
            "name" : self.__name__,
            "type" : "SOMEIPParameterArray",
            "dim" : [],
            "child" : self.__child__.json() if self.__child__ is not None else "None",
        }
        for dim in self.__dims__:
            attr["dim"].append(self.__dims__[dim].json())
        return attr



class SOMEIPParameterArrayDim(SOMEIPBaseParameterArrayDim):
    def json(self):
        attr = {
            "Dimension" : self.__dim__,
            "lowerlimit" : self.__lowerlimit__,
            "upperlimit" : self.__upperlimit__,
            "lengthOfLength" : self.__lengthOfLength__,
            # "padding" : self.__padTo__,
        }
        return attr


class SOMEIPParameterStruct(SOMEIPBaseParameterStruct):
    def json(self):
        attr = {
            "name" : self.__name__,
            "type" : "SOMEIPParameterStruct",
            "members" : [],
        }

        if self.__members__ is not None:
            for m in sorted(self.__members__.keys()):
                member:SOMEIPParameterStructMember = self.__members__[m]
                if member is not None:
                    attr["members"].append(member.json())
                else:
                    print("ERROR: struct member == None!")
        return attr
    
class SOMEIPParameterStructMember(SOMEIPBaseParameterStructMember):
    def json(self):
        attr = {
            "position" : self.__position__,
            "name" : self.__name__,
        }
        if self.__child__ is not None:
            attr["child"] = self.__child__.json()
        if self.__signal__ is not None:
            attr["signal"] = self.__signal__.json()
        return attr


class SOMEIPParameterTypedef(SOMEIPBaseParameterTypedef):
    def json(self):
        attr = {
            "name" : self.__name__,
            "type" : "SOMEIPParameterTypedef",
        }
        if self.__child__ is not None:
            attr["child"] = self.__child__.json()
        return attr



class SOMEIPParameterEnumeration(SOMEIPBaseParameterEnumeration):
    def json(self):
        attr = {
            "name" : self.__name__,
            "type" : "SOMEIPParameterEnumeration",
            "child" : self.__child__.json(),
            "items" : {}
        }
        items = list(self.__items__)
        items.sort(key=lambda e:int(e.__value__))
        for i in items:
            i:SOMEIPParameterEnumerationItem = i
            i.map(attr["items"])
        return attr


class SOMEIPParameterEnumerationItem(SOMEIPBaseParameterEnumerationItem):
    def json(self):
        return {
            self.__value__ : self.__name__
        }
    def map(self,map:dict):
        map[self.__value__] = self.__name__ 


class SOMEIPParameterUnion(SOMEIPBaseParameterUnion):
    def json(self):
        attr = {
            "name" : self.__name__,
            "type" : "SOMEIPParameterUnion",
            "members" : []
        }
        if self.__members__ is not None:
            for m in sorted(self.__members__.keys()):
                member = self.__members__[m]
                if member is not None:
                    attr["members"].append(member.json())
                else:
                    print("ERROR: union member == None!")
        return attr

class SOMEIPParameterUnionMember(SOMEIPBaseParameterUnionMember):
    def json(self):
        attr = {
            "name" : self.name(),
            "index" : self.index()
        }
        if self.__child__ is not None:
            attr["child"] = self.__child__.json()

        return attr


class SOMEIPLegacySignal(SOMEIPBaseLegacySignal):
    def json(self):
        attr = {
            "name" : self.__name__,
        }
        if depressionLevel < 2:
            if self.__compu_scale__ is not None and len(self.__compu_scale__) == 3:
                attr["scale"] = f"f(x) = {self.__compu_scale__[0]} + {self.__compu_scale__[1]}/{self.__compu_scale__[2]} * x"
            if self.__compu_consts__ is not None and len(self.__compu_consts__) > 0:
                attr["consts"] = f""
                first = True
                for name, start, end in self.__compu_consts__:
                    if first:
                        first = False
                    else:
                        attr["consts"] += ", "
                    attr["consts"] += f"{name} ({start}-{end})"

            return attr





class FibexParserJson(FibexParser):
    def json(self):
        interfaceDic = dict()
        for serviceKey in self.__services__:
            service:SOMEIPService = self.__services__[serviceKey]
            interfaceDic[service.name()] = service.json()
        retDic = {
            "interfaces" : interfaceDic,
        }
        return retDic




###############################################################################
###############################################################################
###############################################################################

def help_and_exit():
    print("illegal arguments!")
    print(f"  {sys.argv[0]} type filename")
    print(f"  example: {sys.argv[0]} FIBEX test.xml")
    sys.exit(-1)


def build_json(fibex_files:list,file:TextIOWrapper,dep=0):
    depressionLevel = dep
    conf_factory = SimpleConfigurationFactory()
    fb = FibexParserJson()
    for f in fibex_files:
        fb.parse_file(conf_factory, f)
    try:
        if depressionLevel == 0:
            jsonStr = json.dumps(fb.json(),skipkeys=False,indent=2)
        else:
            jsonStr = json.dumps(fb.json(),skipkeys=False,separators=(',',':'))
        file.write(jsonStr)
    except:
        print("Error: build json error")
        print(fb.json(),file=file)
    print("Done.")

def main():
    print("Converting configuration to json")

    if len(sys.argv) != 3:
        help_and_exit()

    (t, filename) = sys.argv[1:]

    if os.path.isdir(filename):
        fibex_files = glob.glob(filename + "/**/FBX*.xml", recursive=True)
        target_dir = os.path.join(filename, "json")
        textfile = os.path.join(target_dir, "all_files" + ".json")
    elif os.path.isfile(filename):
        fibex_files = [filename]
        (path, f) = os.path.split(filename)
        filenoext = '.'.join(f.split('.')[:-1])
        target_dir = os.path.join(path, filenoext, "json")
        textfile = os.path.join(target_dir, filenoext + ".json")
    else:
        help_and_exit()

    f = open(textfile, "w")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        time.sleep(0.5)

    if t.upper() == "FIBEX":
        build_json(fibex_files,f,depressionLevel)
    else:
        help_and_exit()
    
    f.close()

if __name__ == "__main__":
    main()