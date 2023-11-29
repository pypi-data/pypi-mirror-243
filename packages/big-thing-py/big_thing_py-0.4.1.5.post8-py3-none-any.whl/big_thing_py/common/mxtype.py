from enum import Enum, auto
from typing import Union


class MXNetworkType(Enum):
    MQTT = 0
    API = 1
    BLUETOOTH = 2
    BLE = 3
    RF = 4
    XBEE = 5


class MXType(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    UNDEFINED = auto()
    INTEGER = 'int'
    DOUBLE = 'double'
    STRING = 'string'
    BOOL = 'bool'
    BINARY = 'binary'
    VOID = 'void'

    def __str__(self):
        return str(self.name)

    @classmethod
    def get(cls, name: Union[str, type]) -> 'MXType':
        try:
            if isinstance(name, str):
                name = name.lower()
                if name is not None:
                    for mxtype in MXType:
                        if mxtype.value == name:
                            return mxtype
                        elif mxtype.value == 'int' and name == 'integer':
                            return cls.INTEGER
                        elif mxtype.value == 'double' and name == 'float':
                            return cls.DOUBLE
                        elif mxtype.value == 'string' and name == 'str':
                            return cls.STRING
                        elif mxtype.value == 'bool' and name == 'boolean':
                            return cls.BOOL
                    return cls.UNDEFINED
                else:
                    return cls.UNDEFINED
            elif isinstance(name, type):
                if name == int:
                    return MXType.INTEGER
                elif name == float:
                    return MXType.DOUBLE
                elif name == bool:
                    return MXType.BOOL
                elif name == str:
                    return MXType.STRING
                elif name == str:
                    return MXType.BINARY
                elif name is None:
                    return MXType.VOID
        except Exception:
            return cls.UNDEFINED

    def to_pytype(self):
        if self == MXType.INTEGER:
            return int
        elif self == MXType.DOUBLE:
            return float
        elif self == MXType.BOOL:
            return bool
        elif self == MXType.STRING:
            return str
        elif self == MXType.BINARY:
            return str
        elif self == MXType.VOID:
            return None


class MXActionType(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    REGISTER = auto()
    EXECUTE = auto()
    ALIVE = auto()
    VALUE_PUBLISH = auto()
    AVAILABILITY = auto()
    REFRESH = auto()
    SUPER_SCHEDULE = auto()
    SUPER_EXECUTE = auto()
    SUB_SCHEDULE = auto()
    SUB_EXECUTE = auto()


class MXProtocolType:
    class Base(Enum):
        # ===============
        # ___  ___ _____
        # |  \/  ||_   _|
        # | .  . |  | |
        # | |\/| |  | |
        # | |  | |  | |
        # \_|  |_/  \_/
        # ===============

        # MT/RESULT/REGISTER/[ThingName]
        MT_RESULT_REGISTER = 'MT/RESULT/REGISTER/%s'

        # MT/RESULT/UNREGISTER/[ThingName]
        MT_RESULT_UNREGISTER = 'MT/RESULT/UNREGISTER/%s'

        # MT/EXECUTE/[FunctionName]/[ThingName]/([TargetMiddlewareName]/[Request_ID])
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        MT_EXECUTE = 'MT/EXECUTE/%s/%s/%s/%s'

        # MT/RESULT/BINARY_VALUE/[ThingName]
        MT_RESULT_BINARY_VALUE = 'MT/RESULT/BINARY_VALUE/%s'

        # ===============
        #  _____ ___  ___
        # |_   _||  \/  |
        #   | |  | .  . |
        #   | |  | |\/| |
        #   | |  | |  | |
        #   \_/  \_|  |_/
        # ===============

        # TM/RESULT/EXECUTE/[FunctionName]/[ThingName]/([TargetMiddlewareName]/[Request_ID])
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        TM_RESULT_EXECUTE = 'TM/RESULT/EXECUTE/%s/%s/%s/%s'

        # TM/REGISTER/[ThingName]
        TM_REGISTER = 'TM/REGISTER/%s'

        # TM/UNREGISTER/[ThingName]
        TM_UNREGISTER = 'TM/UNREGISTER/%s'

        # TM/ALIVE/[ThingName]
        TM_ALIVE = 'TM/ALIVE/%s'

        # [ValueName]/[ThingName]
        TM_VALUE_PUBLISH = '%s/%s'

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class Manager(Enum):
        pass

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class Super(Enum):
        # ===============
        # ___  ___ _____
        # |  \/  |/  ___|
        # | .  . |\ `--.
        # | |\/| | `--. \
        # | |  | |/\__/ /
        # \_|  |_/\____/
        # ===============

        # MS/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        MS_SCHEDULE = 'MS/SCHEDULE/%s/%s/%s/%s'

        # MS/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        MS_EXECUTE = 'MS/EXECUTE/%s/%s/%s/%s'

        # MS/RESULT/SCHEDULE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        MS_RESULT_SCHEDULE = 'MS/RESULT/SCHEDULE/%s/SUPER/%s/%s'

        # MS/RESULT/EXECUTE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        MS_RESULT_EXECUTE = 'MS/RESULT/EXECUTE/%s/SUPER/%s/%s'

        # MS/RESULT/SERVICE_LIST/[SuperThingName]
        MS_RESULT_SERVICE_LIST = 'MS/RESULT/SERVICE_LIST/%s'

        # ================
        #  _____ ___  ___
        # /  ___||  \/  |
        # \ `--. | .  . |
        #  `--. \| |\/| |
        # /\__/ /| |  | |
        # \____/ \_|  |_/
        # ================

        # SM/SCHEDULE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        SM_SCHEDULE = 'SM/SCHEDULE/%s/SUPER/%s/%s'

        # SM/EXECUTE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        SM_EXECUTE = 'SM/EXECUTE/%s/SUPER/%s/%s'

        # SM/RESULT/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        SM_RESULT_SCHEDULE = 'SM/RESULT/SCHEDULE/%s/%s/%s/%s'

        # SM/RESULT/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        SM_RESULT_EXECUTE = 'SM/RESULT/EXECUTE/%s/%s/%s/%s'

        # SM/AVAILABILITY/[SuperThingName]
        SM_AVAILABILITY = 'SM/AVAILABILITY/%s'

        # SM/REFRESH/[SuperThingName]
        SM_REFRESH = 'SM/REFRESH/%s'

        # ==================
        #   _____    _____
        #  |  __ \  / ____|
        #  | |__) || |
        #  |  ___/ | |
        #  | |     | |____
        #  |_|      \_____|
        # ==================

        # PC/SCHEDULE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        PC_SCHEDULE = 'PC/SCHEDULE/%s/SUPER/%s/%s'

        # PC/EXECUTE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        PC_EXECUTE = 'PC/EXECUTE/%s/SUPER/%s/%s'

        # PC/RESULT/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        PC_RESULT_SCHEDULE = 'PC/RESULT/SCHEDULE/%s/%s/%s/%s'

        # PC/RESULT/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        PC_RESULT_EXECUTE = 'PC/RESULT/EXECUTE/%s/%s/%s/%s'

        # PC/SERVICE_LIST/#
        PC_SERVICE_LIST = 'PC/SERVICE_LIST/%s'

        # PC/TRAVERSE/#
        PC_TRAVERSE = 'PC/TRAVERSE/%s'

        # ==================
        #    _____  _____
        #   / ____||  __ \
        #  | |     | |__) |
        #  | |     |  ___/
        #  | |____ | |
        #   \_____||_|
        # ==================

        # CP/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        CP_SCHEDULE = 'CP/SCHEDULE/%s/%s/%s/%s'

        # CP/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[Requester MWName]
        CP_EXECUTE = 'CP/EXECUTE/%s/%s/%s/%s'

        # CP/RESULT/SCHEDULE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        CP_RESULT_SCHEDULE = 'CP/RESULT/SCHEDULE/%s/SUPER/%s/%s'

        # CP/RESULT/EXECUTE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        CP_RESULT_EXECUTE = 'CP/RESULT/EXECUTE/%s/SUPER/%s/%s'

        # CP/SERVICE_LIST/#
        CP_SERVICE_LIST = 'CP/SERVICE_LIST/%s'

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class WebClient(Enum):
        # ==================
        #   ______  __  __
        #  |  ____||  \/  |
        #  | |__   | \  / |
        #  |  __|  | |\/| |
        #  | |____ | |  | |
        #  |______||_|  |_|
        # ==================

        #### Hub Connect
        # EM/REQUEST_CONNECTION/[ClientID]
        EM_REQUEST_CONNECTION = 'EM/REQUEST_CONNECTION/%s'

        # EM/CONNECT_AS_OWNER/[ClientID]
        EM_CONNECT_AS_OWNER = 'EM/CONNECT_AS_OWNER/%s'

        #### Member Manage
        # EM/SET_MEMBER_LEVEL/[ClientID]
        EM_SET_MEMBER_LEVEL = 'EM/SET_MEMBER_LEVEL/%s'

        # EM/SET_MEMBER_STATE/[ClientID]
        EM_SET_MEMBER_STATE = 'EM/SET_MEMBER_STATE/%s'

        # EM/DELETE_MEMBER/[ClientID]
        EM_DELETE_MEMBER = 'EM/DELETE_MEMBER/%s'

        #### Device Manage
        # EM/REGISTER_THING/[ClientID]
        EM_REGISTER_THING = 'EM/REGISTER_THING/%s'

        # EM/UNREGISTER_THING/[ClientID]
        EM_UNREGISTER_THING = 'EM/UNREGISTER_THING/%s'

        # EM/SET_NICK_NAME/[ClientID]
        EM_SET_NICK_NAME = 'EM/SET_NICK_NAME/%s'

        # EM/SET_DESCRIPTION/[ClientID]
        EM_SET_DESCRIPTION = 'EM/SET_DESCRIPTION/%s'

        # EM/REQUEST_MATTER_SCAN/[ClientID]
        EM_REQUEST_MATTER_SCAN = 'EM/REQUEST_MATTER_SCAN/%s'

        # EM/OPEN_WINDOW_MATTER/[ClientID]
        EM_OPEN_WINDOW_MATTER = 'EM/OPEN_WINDOW_MATTER/%s'

        # EM/CANCEL_OPEN_WINDOW_MATTER/[ClientID]
        EM_CANCEL_OPEN_WINDOW_MATTER = 'EM/CANCEL_OPEN_WINDOW_MATTER/%s'

        #### Scenario Manage
        # EM/VERIFY_SCENARIO/[ClientID]
        EM_VERIFY_SCENARIO = 'EM/VERIFY_SCENARIO/%s'

        # EM/ADD_SCENARIO/[ClientID]
        EM_ADD_SCENARIO = 'EM/ADD_SCENARIO/%s'

        # EM/RUN_SCENARIO/[ClientID]
        EM_RUN_SCENARIO = 'EM/RUN_SCENARIO/%s'

        # EM/STOP_SCENARIO/[ClientID]
        EM_STOP_SCENARIO = 'EM/STOP_SCENARIO/%s'

        # EM/UPDATE_SCENARIO/[ClientID]
        EM_UPDATE_SCENARIO = 'EM/UPDATE_SCENARIO/%s'

        # EM/DELETE_SCENARIO/[ClientID]
        EM_DELETE_SCENARIO = 'EM/DELETE_SCENARIO/%s'

        #### Service Manage
        # EM/ADD_TAG/[ClientID]
        EM_ADD_TAG = 'EM/ADD_TAG/%s'

        # EM/DELETE_TAG/[ClientID]
        EM_DELETE_TAG = 'EM/DELETE_TAG/%s'

        # EM/SET_ACCESS/[ClientID]
        EM_SET_ACCESS = 'EM/SET_ACCESS/%s'

        # EM/SET_OPENED/[ClientID]
        EM_SET_OPENED = 'EM/SET_OPENED/%s'

        # EM/GET_TREE/[ClientID]
        EM_GET_TREE = 'EM/GET_TREE/%s'

        # EM/EXECUTE/[ClientID]
        EM_EXECUTE = 'EM/EXECUTE/%s'

        #### Sync Info
        # EM/REFRESH/[ClientID]
        EM_REFRESH = 'EM/REFRESH/%s'

        # EM/GET_THING/[ClientID]
        EM_GET_THING = 'EM/GET_THING/%s'

        # EM/GET_SERVICE/[ClientID]
        EM_GET_SERVICE = 'EM/GET_SERVICE/%s'

        # EM/GET_SCENARIO/[ClientID]
        EM_GET_SCENARIO = 'EM/GET_SCENARIO/%s'

        # EM/GET_MEMBER/[ClientID]
        EM_GET_MEMBER = 'EM/GET_MEMBER/%s'

        # EM/GET_THING_LIST/[ClientID]
        EM_GET_THING_LIST = 'EM/GET_THING_LIST/%s'

        # EM/GET_SERVICE_LIST/[ClientID]
        EM_GET_SERVICE_LIST = 'EM/GET_SERVICE_LIST/%s'

        # EM/GET_SCENARIO_LIST/[ClientID]
        EM_GET_SCENARIO_LIST = 'EM/GET_SCENARIO_LIST/%s'

        # EM/GET_MEMBER_LIST/[ClientID]
        EM_GET_MEMBER_LIST = 'EM/GET_MEMBER_LIST/%s'

        #### Hub Reset
        # EM/RESET_HUB/[ClientID]
        EM_RESET_HUB = 'EM/RESET_HUB/%s'

        # ==================
        #   __  __  ______
        #  |  \/  ||  ____|
        #  | \  / || |__
        #  | |\/| ||  __|
        #  | |  | || |____
        #  |_|  |_||______|
        # ==================

        #### Hub Connect
        # ME/RESULT/REQUEST_CONNECTION/[ClientID]
        ME_RESULT_REQUEST_CONNECTION = 'ME/RESULT/REQUEST_CONNECTION/%s'

        # ME/OWNER_BUTTON_CLICKED/[ClientID]
        ME_OWNER_BUTTON_CLICKED = 'ME/OWNER_BUTTON_CLICKED/%s'

        # ME/RESULT/CONNECT_AS_OWNER/[ClientID]
        ME_RESULT_CONNECT_AS_OWNER = 'ME/RESULT/CONNECT_AS_OWNER/%s'

        #### Member Manage
        # ME/RESULT/SET_MEMBER_LEVEL/[ClientID]
        ME_RESULT_SET_MEMBER_LEVEL = 'ME/RESULT/SET_MEMBER_LEVEL/%s'

        # ME/RESULT/SET_MEMBER_STATE/[ClientID]
        ME_RESULT_SET_MEMBER_STATE = 'ME/RESULT/SET_MEMBER_STATE/%s'

        # ME/RESULT/DELETE_MEMBER/[ClientID]
        ME_RESULT_DELETE_MEMBER = 'ME/RESULT/DELETE_MEMBER/%s'

        #### Device Manage
        # ME/RESULT/REGISTER_THING/[ClientID]
        ME_RESULT_REGISTER_THING = 'ME/RESULT/REGISTER_THING/%s'

        # ME/RESULT/UNREGISTER/[ClientID]
        ME_RESULT_UNREGISTER_THING = 'ME/RESULT/UNREGISTER/%s'

        # ME/RESULT/SET_NICK_NAME/[ClientID]
        ME_RESULT_SET_NICK_NAME = 'ME/RESULT/SET_NICK_NAME/%s'

        # ME/RESULT/SET_DESCRIPTION/[ClientID]
        ME_RESULT_SET_DESCRIPTION = 'ME/RESULT/SET_DESCRIPTION/%s'

        # ME/RESULT/REQUEST_MATTER_SCAN/[ClientID]
        ME_RESULT_REQUEST_MATTER_SCAN = 'ME/RESULT/REQUEST_MATTER_SCAN/%s'

        # ME/RESULT/OPEN_WINDOW_MATTER/[ClientID]
        ME_RESULT_OPEN_WINDOW_MATTER = 'ME/RESULT/OPEN_WINDOW_MATTER/%s'

        # ME/RESULT/CANCEL_OPEN_WINDOW_MATTER/[ClientID]
        ME_RESULT_CANCEL_OPEN_WINDOW_MATTER = 'ME/RESULT/CANCEL_OPEN_WINDOW_MATTER/%s'

        #### Scenario Manage
        # ME/RESULT/VERIFY_SCENARIO/[ClientID]
        ME_RESULT_VERIFY_SCENARIO = 'ME/RESULT/VERIFY_SCENARIO/%s'

        # ME/RESULT/RUN_SCENARIO/[ClientID]
        ME_RESULT_RUN_SCENARIO = 'ME/RESULT/RUN_SCENARIO/%s'

        # ME/RESULT/STOP_SCENARIO/[ClientID]
        ME_RESULT_STOP_SCENARIO = 'ME/RESULT/STOP_SCENARIO/%s'

        # ME/RESULT/SCHEDULE_SCENARIO/[ClientID]
        ME_RESULT_SCHEDULE_SCENARIO = 'ME/RESULT/SCHEDULE_SCENARIO/%s'

        # ME/RESULT/SCHEDULE_SCENARIO/[ClientID]
        ME_RESULT_ADD_SCENARIO = ME_RESULT_SCHEDULE_SCENARIO

        # ME/RESULT/SCHEDULE_SCENARIO/[ClientID]
        ME_RESULT_UPDATE_SCENARIO = ME_RESULT_SCHEDULE_SCENARIO

        # ME/RESULT/DELETE_SCENARIO/[ClientID]
        ME_RESULT_DELETE_SCENARIO = 'ME/RESULT/DELETE_SCENARIO/%s'

        #### Service Manage
        # ME/RESULT/ADD_TAG/[ClientID]
        ME_RESULT_ADD_TAG = 'ME/RESULT/ADD_TAG/%s'

        # ME/RESULT/DELETE_TAG/[ClientID]
        ME_RESULT_DELETE_TAG = 'ME/RESULT/DELETE_TAG/%s'

        # ME/RESULT/SET_ACCESS/[ClientID]
        ME_RESULT_SET_ACCESS = 'ME/RESULT/SET_ACCESS/%s'

        # ME/RESULT/SET_OPENED/[ClientID]
        ME_RESULT_SET_OPENED = 'ME/RESULT/SET_OPENED/%s'

        # ME/RESULT/GET_TREE/[ClientID]
        ME_RESULT_GET_TREE = 'ME/RESULT/GET_TREE/%s'

        # ME/RESULT/EXECUTE/[ClientID]
        ME_RESULT_EXECUTE = 'ME/RESULT/EXECUTE/%s'

        #### Sync Info
        # ME/RESULT/THING/[ClientID]
        ME_RESULT_THING = 'ME/RESULT/THING/%s'

        # ME/RESULT/SERVICE/[ClientID]
        ME_RESULT_SERVICE = 'ME/RESULT/SERVICE/%s'

        # ME/RESULT/SCENARIO/[ClientID]
        ME_RESULT_SCENARIO = 'ME/RESULT/SCENARIO/%s'

        # ME/RESULT/GET_MEMBER/[ClientID]
        ME_RESULT_MEMBER = 'ME/RESULT/GET_MEMBER/%s'

        # ME/RESULT/THING_LIST/[ClientID]
        ME_RESULT_THING_LIST = 'ME/RESULT/THING_LIST/%s'

        # ME/RESULT/SERVICE_LIST/[ClientID]
        ME_RESULT_SERVICE_LIST = 'ME/RESULT/SERVICE_LIST/%s'

        # ME/RESULT/SCENARIO_LIST/[ClientID]
        ME_RESULT_SCENARIO_LIST = 'ME/RESULT/SCENARIO_LIST/%s'

        # ME/RESULT/GET_MEMBER_LIST/[ClientID]
        ME_RESULT_MEMBER_LIST = 'ME/RESULT/GET_MEMBER_LIST/%s'

        #### Notify
        # ME/NOTIFY_MESSAGE/[ClientID]
        ME_NOTIFY_MESSAGE = 'ME/NOTIFY_MESSAGE/%s'

        # ME/NOTIFY_CHANGE/[ClientID]
        ME_NOTIFY_CHANGE = 'ME/NOTIFY_CHANGE/%s'

        #### Hub Reset
        # ME/RESULT/RESET_HUB/[ClientID]
        ME_RESULT_RESET_HUB = 'ME/RESULT/RESET_HUB/%s'

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class SN(Enum):
        # TM/SN/REGISTER/VALUE/[Thing ID]
        TM_SN_REGISTER_VALUE = "TM/SN/REGISTER/VALUE/%s"

        # TM/SN/REGISTER/VALUEDESC/[Thing ID]
        TM_SN_REGISTER_VALUEDESC = "TM/SN/REGISTER/VALUEDESC/%s"

        # TM/SN/REGISTER/VALUETAG/[Thing ID]
        TM_SN_REGISTER_VALUETAG = "TM/SN/REGISTER/VALUETAG/%s"

        # TM/SN/REGISTER/FUNCTION/[Thing ID]
        TM_SN_REGISTER_FUNCTION = "TM/SN/REGISTER/FUNCTION/%s"

        # TM/SN/REGISTER/FUNCTIONDESC/[Thing ID]
        TM_SN_REGISTER_FUNCTIONDESC = "TM/SN/REGISTER/FUNCTIONDESC/%s"

        # TM/SN/REGISTER/FUNCTIONTAG/[Thing ID]
        TM_SN_REGISTER_FUNCTIONTAG = "TM/SN/REGISTER/FUNCTIONTAG/%s"

        # TM/SN/REGISTER/ARGUMENT/[Thing ID]
        TM_SN_REGISTER_ARGUMENT = "TM/SN/REGISTER/ARGUMENT/%s"

        # TM/SN/REGISTER/ALIVECYCLE/[Thing ID]
        TM_SN_REGISTER_ALIVECYCLE = "TM/SN/REGISTER/ALIVECYCLE/%s"

        # TM/SN/REGISTER/FINISH/[Thing ID]
        TM_SN_REGISTER_FINISH = "TM/SN/REGISTER/FINISH/%s"

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    @classmethod
    def get(cls, topic: str) -> 'MXProtocolType':
        # MT
        if 'MT/RESULT/REGISTER/' in topic:
            return cls.Base.MT_RESULT_REGISTER
        elif 'MT/RESULT/UNREGISTER/' in topic:
            return cls.Base.MT_RESULT_UNREGISTER
        elif 'MT/EXECUTE/' in topic:
            return cls.Base.MT_EXECUTE
        elif 'MT/RESULT/BINARY_VALUE/' in topic:
            return cls.Base.MT_RESULT_BINARY_VALUE
        # TM
        elif 'TM/RESULT/EXECUTE/' in topic:
            return cls.Base.TM_RESULT_EXECUTE
        elif 'TM/REGISTER/' in topic:
            return cls.Base.TM_REGISTER
        elif 'TM/UNREGISTER/' in topic:
            return cls.Base.TM_UNREGISTER
        elif 'TM/ALIVE/' in topic:
            return cls.Base.TM_ALIVE
        elif len(topic.split('/')) == 2:
            return cls.Base.TM_VALUE_PUBLISH
        # MS
        elif 'MS/SCHEDULE/' in topic:
            return cls.Super.MS_SCHEDULE
        elif 'MS/EXECUTE/' in topic:
            return cls.Super.MS_EXECUTE
        elif 'MS/RESULT/SCHEDULE/' in topic:
            return cls.Super.MS_RESULT_SCHEDULE
        elif 'MS/RESULT/EXECUTE/' in topic:
            return cls.Super.MS_RESULT_EXECUTE
        elif 'MS/RESULT/SERVICE_LIST/' in topic:
            return cls.Super.MS_RESULT_SERVICE_LIST
        # SM
        elif 'SM/SCHEDULE/' in topic:
            return cls.Super.SM_SCHEDULE
        elif 'SM/EXECUTE/' in topic:
            return cls.Super.SM_EXECUTE
        elif 'SM/RESULT/SCHEDULE/' in topic:
            return cls.Super.SM_RESULT_SCHEDULE
        elif 'SM/RESULT/EXECUTE/' in topic:
            return cls.Super.SM_RESULT_EXECUTE
        elif 'SM/AVAILABILITY/' in topic:
            return cls.Super.SM_AVAILABILITY
        elif 'SM/REFRESH/' in topic:
            return cls.Super.SM_REFRESH
        # PC
        elif 'PC/SCHEDULE/' in topic:
            return cls.Super.PC_SCHEDULE
        elif 'PC/EXECUTE/' in topic:
            return cls.Super.PC_EXECUTE
        elif 'PC/RESULT/SCHEDULE/' in topic:
            return cls.Super.PC_RESULT_SCHEDULE
        elif 'PC/RESULT/EXECUTE/' in topic:
            return cls.Super.PC_RESULT_EXECUTE
        elif 'PC/SERVICE_LIST/' in topic:
            return cls.Super.PC_SERVICE_LIST
        elif 'PC/TRAVERSE/' in topic:
            return cls.Super.PC_TRAVERSE
        # CP
        elif 'CP/SCHEDULE/' in topic:
            return cls.Super.CP_SCHEDULE
        elif 'CP/EXECUTE/' in topic:
            return cls.Super.CP_EXECUTE
        elif 'CP/RESULT/SCHEDULE/' in topic:
            return cls.Super.CP_RESULT_SCHEDULE
        elif 'CP/RESULT/EXECUTE/' in topic:
            return cls.Super.CP_RESULT_EXECUTE
        elif 'CP/SERVICE_LIST/' in topic:
            return cls.Super.CP_SERVICE_LIST
        # EM
        if 'EM/REQUEST_CONNECTION/' in topic:
            return cls.WebClient.EM_REQUEST_CONNECTION
        elif 'EM/CONNECT_AS_OWNER/' in topic:
            return cls.WebClient.EM_CONNECT_AS_OWNER
        elif 'EM/SET_MEMBER_LEVEL/' in topic:
            return cls.WebClient.EM_SET_MEMBER_LEVEL
        elif 'EM/SET_MEMBER_STATE/' in topic:
            return cls.WebClient.EM_SET_MEMBER_STATE
        elif 'EM/DELETE_MEMBER/' in topic:
            return cls.WebClient.EM_DELETE_MEMBER
        elif 'EM/REGISTER_THING/' in topic:
            return cls.WebClient.EM_REGISTER_THING
        elif 'EM/UNREGISTER_THING/' in topic:
            return cls.WebClient.EM_UNREGISTER_THING
        elif 'EM/SET_NICK_NAME/' in topic:
            return cls.WebClient.EM_SET_NICK_NAME
        elif 'EM/SET_DESCRIPTION/' in topic:
            return cls.WebClient.EM_SET_DESCRIPTION
        elif 'EM/REQUEST_MATTER_SCAN/' in topic:
            return cls.WebClient.EM_REQUEST_MATTER_SCAN
        elif 'EM/OPEN_WINDOW_MATTER/' in topic:
            return cls.WebClient.EM_OPEN_WINDOW_MATTER
        elif 'EM/CANCEL_OPEN_WINDOW_MATTER/' in topic:
            return cls.WebClient.EM_CANCEL_OPEN_WINDOW_MATTER
        elif 'EM/EXECUTE/' in topic:
            return cls.WebClient.EM_EXECUTE
        elif 'EM/SET_ACCESS/' in topic:
            return cls.WebClient.EM_SET_ACCESS
        elif 'EM/SET_OPENED/' in topic:
            return cls.WebClient.EM_SET_OPENED
        elif 'EM/GET_THING/' in topic:
            return cls.WebClient.EM_GET_THING
        elif 'EM/GET_SERVICE/' in topic:
            return cls.WebClient.EM_GET_SERVICE
        elif 'EM/GET_SCENARIO/' in topic:
            return cls.WebClient.EM_GET_SCENARIO
        elif 'EM/GET_MEMBER/' in topic:
            return cls.WebClient.EM_GET_MEMBER
        elif 'EM/GET_THING_LIST/' in topic:
            return cls.WebClient.EM_GET_THING_LIST
        elif 'EM/GET_SERVICE_LIST/' in topic:
            return cls.WebClient.EM_GET_SERVICE_LIST
        elif 'EM/GET_SCENARIO_LIST/' in topic:
            return cls.WebClient.EM_GET_SCENARIO_LIST
        elif 'EM/GET_MEMBER_LIST/' in topic:
            return cls.WebClient.EM_GET_MEMBER_LIST
        elif 'EM/RESET_HUB/' in topic:
            return cls.WebClient.EM_RESET_HUB
        # ME
        elif 'ME/RESULT/REQUEST_CONNECTION/' in topic:
            return cls.WebClient.ME_RESULT_REQUEST_CONNECTION
        elif 'ME/OWNER_BUTTON_CLICKED/' in topic:
            return cls.WebClient.ME_OWNER_BUTTON_CLICKED
        elif 'ME/RESULT/CONNECT_AS_OWNER/' in topic:
            return cls.WebClient.ME_RESULT_CONNECT_AS_OWNER
        elif 'ME/RESULT/SET_MEMBER_LEVEL/' in topic:
            return cls.WebClient.ME_RESULT_SET_MEMBER_LEVEL
        elif 'ME/RESULT/SET_MEMBER_STATE/' in topic:
            return cls.WebClient.ME_RESULT_SET_MEMBER_STATE
        elif 'ME/RESULT/DELETE_MEMBER/' in topic:
            return cls.WebClient.ME_RESULT_DELETE_MEMBER
        elif 'ME/RESULT/REGISTER_THING/' in topic:
            return cls.WebClient.ME_RESULT_REGISTER_THING
        elif 'ME/RESULT/UNREGISTER_THING/' in topic:
            return cls.WebClient.ME_RESULT_UNREGISTER_THING
        elif 'ME/RESULT/SET_NICK_NAME/' in topic:
            return cls.WebClient.ME_RESULT_SET_NICK_NAME
        elif 'ME/RESULT/SET_DESCRIPTION/' in topic:
            return cls.WebClient.ME_RESULT_SET_DESCRIPTION
        elif 'ME/RESULT/REQUEST_MATTER_SCAN/' in topic:
            return cls.WebClient.ME_RESULT_REQUEST_MATTER_SCAN
        elif 'ME/RESULT/OPEN_WINDOW_MATTER/' in topic:
            return cls.WebClient.ME_RESULT_OPEN_WINDOW_MATTER
        elif 'ME/RESULT/CANCEL_OPEN_WINDOW_MATTER/' in topic:
            return cls.WebClient.ME_RESULT_CANCEL_OPEN_WINDOW_MATTER
        elif 'ME/RESULT/EXECUTE/' in topic:
            return cls.WebClient.ME_RESULT_EXECUTE
        elif 'ME/RESULT/SET_ACCESS/' in topic:
            return cls.WebClient.ME_RESULT_SET_ACCESS
        elif 'ME/RESULT/SET_OPENED/' in topic:
            return cls.WebClient.ME_RESULT_SET_OPENED
        elif 'ME/RESULT/THING/' in topic:
            return cls.WebClient.ME_RESULT_THING
        elif 'ME/RESULT/SERVICE/' in topic:
            return cls.WebClient.ME_RESULT_SERVICE
        elif 'ME/RESULT/SCENARIO/' in topic:
            return cls.WebClient.ME_RESULT_SCENARIO
        elif 'ME/RESULT/MEMBER/' in topic:
            return cls.WebClient.ME_RESULT_MEMBER
        elif 'ME/RESULT/THING_LIST/' in topic:
            return cls.WebClient.ME_RESULT_THING_LIST
        elif 'ME/RESULT/SERVICE_LIST/' in topic:
            return cls.WebClient.ME_RESULT_SERVICE_LIST
        elif 'ME/RESULT/SCENARIO_LIST/' in topic:
            return cls.WebClient.ME_RESULT_SCENARIO_LIST
        elif 'ME/RESULT/MEMBER_LIST/' in topic:
            return cls.WebClient.ME_RESULT_MEMBER_LIST
        elif 'ME/NOTIFY_MESSAGE/' in topic:
            return cls.WebClient.ME_NOTIFY_MESSAGE
        elif 'ME/RESULT/RESET_HUB/' in topic:
            return cls.WebClient.ME_RESULT_RESET_HUB
        # TM/SN
        elif 'TM/SN/REGISTER/VALUE/' in topic:
            return cls.SN.TM_SN_REGISTER_VALUE
        elif 'TM/SN/REGISTER/VALUEDESC/' in topic:
            return cls.SN.TM_SN_REGISTER_VALUEDESC
        elif 'TM/SN/REGISTER/VALUETAG/' in topic:
            return cls.SN.TM_SN_REGISTER_VALUETAG
        elif 'TM/SN/REGISTER/FUNCTION/' in topic:
            return cls.SN.TM_SN_REGISTER_FUNCTION
        elif 'TM/SN/REGISTER/FUNCTIONDESC/' in topic:
            return cls.SN.TM_SN_REGISTER_FUNCTIONDESC
        elif 'TM/SN/REGISTER/FUNCTIONTAG/' in topic:
            return cls.SN.TM_SN_REGISTER_FUNCTIONTAG
        elif 'TM/SN/REGISTER/ARGUMENT/' in topic:
            return cls.SN.TM_SN_REGISTER_ARGUMENT
        elif 'TM/SN/REGISTER/ALIVECYCLE/' in topic:
            return cls.SN.TM_SN_REGISTER_ALIVECYCLE
        elif 'TM/SN/REGISTER/FINISH/' in topic:
            return cls.SN.TM_SN_REGISTER_FINISH
        else:
            return None


class MXRangeType(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    UNDEFINED = auto()
    ALL = auto()
    SINGLE = auto()

    @classmethod
    def get(cls, name: str) -> 'MXRangeType':
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class HierarchyType(Enum):
    LOCAL = 0
    PARENT = 1
    CHILD = 2


class MXServiceType(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    UNDEFINED = auto()
    VALUE = auto()
    FUNCTION = auto()

    @classmethod
    def get(cls, name: str) -> 'MXServiceType':
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED
