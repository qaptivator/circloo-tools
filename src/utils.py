import re

def get_cli_args(inputs):
    res = []
    for input_data in inputs:
        prompt = input_data.get('prompt')
        if prompt:
            default = input_data.get('default')
            input_res = input(prompt)
            if default and not input_res:
                res.append(default)
            elif not default and not input_res:
                raise Exception('This argument is required!')
            elif input_res:
                res.append(input_res)
    return res

def string_to_tuple(str):
    parts = str.split(',')
    return (parts[0].strip(), parts[1].strip())

def list_safe_get(array, index):
    try:
        return array[index]
    except IndexError:
        return None
    except KeyError:
        return None
    
def get_file_name(full_name):
    dot_index = full_name.rfind('.')
    if dot_index != -1: 
        return full_name[:dot_index]
    else:
        return full_name

def num_from_str(v):
    return ''.join(re.findall(r'\d+', v))

def level_output(level_text, save_as_file, file_name='script_output.txt'):
    if save_as_file == 'y':
      print(f'Saving to {file_name}')
      with open(file_name, 'w') as f:
         f.write(level_text)
    else:
      print(level_text)