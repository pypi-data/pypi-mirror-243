import json
import re

SCENARIO_VAR_LIST_TYPE = 1
DICT_VAR_LIST_TYPE = 2


class VariableNameError(Exception):
    """Вызывается, когда имя не соответствует ограничениям на имя переменной контекста"""
    pass


class VariableStructureNameError(Exception):
    """Вызывается, когда имя не соответствует ограничениям на имя переменной контекста"""
    pass


def assign_value_to_variable(initial: dict, var_key: str, var_value: str = None, is_assign: bool = False):
    """
    Присвоение значения элементу исходного словаря или дополнение структуры пустым словарем. При is_assign=False
    элементу словаря присваивается значение пустого словаря, если этот элемент отсутствует в словаре.

    Parameters:
        initial (dict):исходный словарь
        var_key (str):имя переменной
        var_value (str):значения переменной
        is_assign (boolean):присваивать значение

    Returns:
        dict|str:строка или пустой словарь
    """
    if type(initial) is not dict:
        initial = dict()

    if is_assign:
        initial[var_key] = var_value
    else:
        if var_key not in initial:
            initial[var_key] = dict()

    return initial[var_key]


def create_var_name(path: list) -> str:
    """
    Создает имя переменной контекста по ее структуре

    :param path: структура переменной в виде упорядоченного списка ее основного имения и свойств

    :return: имя переменной контекста
    """
    if type(path) is list and len(path) > 0:
        name = path.pop(0)
        for p in path:
            name = f'{name}[{p}]'
    else:
        raise VariableStructureNameError("Неверная структура имени переменной контекста")
    return name


pattern = re.compile(r'\[([а-яА-Яa-zA-Z0-9_]+)]')


def parse_var_name(var_name: str) -> tuple:
    """
    Распознает имя переменной и преобразуется ее в набор основного имени и массив имен свойств

    :param var_name:имя переменной

    :return:основное имя и массив имен свойств
    """
    first_part = var_name.split('[', 1)[0]

    try:
        main_name = re.findall(pattern, f'[{first_part}]')[0]

        additional_names = pattern.findall(var_name)

        path = additional_names.copy()
        path.insert(0, main_name)

        if create_var_name(path) == var_name:
            return main_name, additional_names
        else:
            raise VariableNameError
    except IndexError:
        raise VariableNameError


def parse_var_to_list(var, path=None, var_list=None, list_type=SCENARIO_VAR_LIST_TYPE):
    """
    Формирует список переменных в формате сценария

    :param var:переменные в структуре вложенного словаря
    :param path:пусть до значения переменной в структуре переменной var
    :param var_list:начальный список переменных в формате сценария
    :param list_type:тип возвращаемого списка - в формате сценария или в формате словаря
    """
    if path is None: path = []
    if var_list is None:
        if list_type == DICT_VAR_LIST_TYPE:
            var_list = dict()
        else:
            var_list = []
    if type(var) is dict:
        for k in var:
            copied_path = path.copy()
            copied_path.append(k)
            var_list = parse_var_to_list(var[k], copied_path, var_list, list_type)
    else:
        if list_type == DICT_VAR_LIST_TYPE:
            try:
                var_list[create_var_name(path)] = var
            except VariableStructureNameError:
                pass
        else:
            var_list.append({
                "name": create_var_name(path),
                "value": var
            })
    return var_list


class Context:
    variables: dict

    def __init__(self, variables=None, parent_ctx: "Context" = None):
        self.parent = parent_ctx
        if type(variables) is dict:
            self.variables = variables
        else:
            self.variables = dict()

    def set(self, var_name, var_value) -> None:
        """
        Присваивает значение переменной

        :param var_name:имя переменной в формате сценария
        :param var_value:значение переменной
        """
        main, add = parse_var_name(var_name)
        len_add = len(add)

        var = assign_value_to_variable(self.variables, main)

        for c, r in enumerate(add, 1):
            if len_add == c:
                var = assign_value_to_variable(var, r, var_value, True)
            else:
                var = assign_value_to_variable(var, r)

    def get(self, var_name) -> dict:
        main, add = parse_var_name(var_name)
        var = None
        if main in self.variables:
            var = self.variables[main]
            for n in add:
                var = var.get(n)
        if self.parent is not None:
            var = self.parent.get(var_name)
        return var


if __name__ == "__main__":
    pass
    # try:
    #     print(create_var_name(['we', '0']))
    # except VariableStructureNameError as e:
    #     print(e)
    #

    try:
        with open('./parent_context.json', encoding='utf-8') as f:
            parent_context = Context(json.load(f))
    except FileNotFoundError as e:
        print(e)

    try:
        with open('./context.json', encoding='utf-8') as f:
            context = Context(json.load(f), parent_ctx=parent_context)
    except FileNotFoundError as e:
        print(e)

    # v = context.get('Услуги[1]')
    # print(v)

    # print(context.variables)
    # print(context.parent.variables)

    try:
        vars_list = parse_var_to_list(context.variables, list_type=DICT_VAR_LIST_TYPE)
        with open('./variable.json', 'w', encoding='utf-8') as outfile:
            json.dump(vars_list, outfile, ensure_ascii=False, indent=4)

        context_reload = Context()
        for v in vars_list:
            context_reload.set(v.get("name"), v.get("value"))
        with open('./context_reload.json', 'w', encoding='utf-8') as file:
            json.dump(context_reload.variables, file, ensure_ascii=False, indent=4)
    except NameError as e:
        print(e)

