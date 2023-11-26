from open_eval.dataset import Dataset
from open_eval.dimension import Dimension


def is_valid_name(name):
    # 使用 vars() 获取类的命名空间字典
    class_dict = vars(Dataset)
    # 遍历类的类变量
    for var_name, var_value in class_dict.items():
        if name == var_value:
            return True
    return False


def is_valid_dimension(dimension):
    # 使用 vars() 获取类的命名空间字典
    class_dict = vars(Dimension)
    # 遍历类的类变量
    for var_name, var_value in class_dict.items():
        if dimension == var_value:
            return True
    return False

