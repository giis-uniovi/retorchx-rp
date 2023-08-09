from scripts.model import capacitytypes
from scripts.model.capacity import Capacity
from scripts.model.executionplan import ExecutionPlan
from scripts.model.resourceinstance import ResourceInstance
from scripts.model.tjob import Tjob
from scripts.utils.executionplangeneratorhelpers import generate_json_with_executionplan

cap_database_memory = Capacity(name=capacitytypes.memory_name, quantity=0.29296875)
cap_database_processor = Capacity(name=capacitytypes.processor_name, quantity=0.2)
cap_database_storage = Capacity(name=capacitytypes.storage_name, quantity=0.58)
database = ResourceInstance(name="database", capacities={cap_database_memory, cap_database_processor,
                                                         cap_database_storage})

cap_openvidu_memory = Capacity(name=capacitytypes.memory_name, quantity=8)
cap_openvidu_processor = Capacity(name=capacitytypes.processor_name, quantity=2)
cap_openvidu_storage = Capacity(name=capacitytypes.storage_name, quantity=0.88)
openvidu = ResourceInstance(name="openvidu", capacities={cap_openvidu_memory, cap_openvidu_processor,
                                                         cap_openvidu_storage})

cap_webserver_memory = Capacity(name=capacitytypes.memory_name, quantity=1.46484375)
cap_webserver_processor = Capacity(name=capacitytypes.processor_name, quantity=0.5)
cap_webserver_storage = Capacity(name=capacitytypes.storage_name, quantity=0.92)
webserver = ResourceInstance(name="webserver", capacities={cap_webserver_memory, cap_webserver_processor,
                                                           cap_webserver_storage})

cap_mock_openvidu_memory = Capacity(name=capacitytypes.memory_name, quantity=0.048828125)
cap_mock_openvidu_processor = Capacity(name=capacitytypes.processor_name, quantity=0.25)
cap_mock_openvidu_storage = Capacity(name=capacitytypes.storage_name, quantity=0.31)
mock_openvidu = ResourceInstance(name="mockopenvidu", capacities={cap_mock_openvidu_memory, cap_mock_openvidu_processor,
                                                                  cap_mock_openvidu_storage})

cap_browser_memory = Capacity(name=capacitytypes.memory_name, quantity=1)
cap_browser_processor = Capacity(name=capacitytypes.processor_name, quantity=0.5)
cap_browser_storage = Capacity(name=capacitytypes.storage_name, quantity=1.16)
cap_browser_slots = Capacity(name=capacitytypes.slots_name, quantity=1)
browser = ResourceInstance(name="browser", capacities={cap_browser_memory, cap_browser_processor, cap_browser_storage,
                                                       cap_browser_slots})

cap_executor_memory = Capacity(name=capacitytypes.memory_name, quantity=0.146484375)
cap_executor_processor = Capacity(name=capacitytypes.processor_name, quantity=0.25)
cap_executor_storage = Capacity(name=capacitytypes.storage_name, quantity=0.49)
executor = ResourceInstance(name="executor", capacities={cap_executor_memory, cap_executor_processor,
                                                         cap_executor_storage})

tjob_c = Tjob(name="tjobc", resourceinstances={webserver, database, mock_openvidu, executor, browser})
tjob_d = Tjob(name="tjobd", resourceinstances={webserver, database, mock_openvidu, executor, browser})
tjob_e = Tjob(name="tjobe", resourceinstances={webserver, database, openvidu, executor, browser, browser})
tjob_f = Tjob(name="tjobf", resourceinstances={webserver, database, mock_openvidu, executor, browser})
tjob_g = Tjob(name="tjobg", resourceinstances={webserver, database, mock_openvidu, executor, browser})
tjob_h = Tjob(name="tjobh", resourceinstances={webserver, database, mock_openvidu, executor, browser})
tjob_i = Tjob(name="tjobi", resourceinstances={webserver, database, mock_openvidu, executor, browser})
tjob_j = Tjob(name="tjobj", resourceinstances={webserver, database, mock_openvidu, executor, browser})
tjob_k = Tjob(name="tjobk", resourceinstances={webserver, database, mock_openvidu, executor, browser})
tjob_m = Tjob(name="tjobm", resourceinstances={webserver, database, openvidu, executor, browser, browser})
tjob_n = Tjob(name="tjobn", resourceinstances={webserver, database, mock_openvidu, executor, browser})
tjob_l = Tjob(name="tjobl", resourceinstances={webserver, database, mock_openvidu, executor, browser})

plan = ExecutionPlan(name="OriginalScheduling",
                     tjobs={tjob_c, tjob_d, tjob_e, tjob_f, tjob_g, tjob_h, tjob_i, tjob_j, tjob_k, tjob_m, tjob_n,
                            tjob_l})
generate_json_with_executionplan(plan=plan,
                                 output_dir='../tests/resources/inputs/profilegenerator/resourceinstances.json')
