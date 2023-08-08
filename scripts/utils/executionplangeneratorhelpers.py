import jsonpickle



#ULR USED  '../../tests/resources/inputs/profilegenerator/resourceinstances.json'
def generate_json_with_executionplan(output_dir, plan):
    plan_json_string = jsonpickle.encode(plan)
    with open(output_dir, 'w') as file:
        file.write(plan_json_string)
    print(plan_json_string)
