import requests
url = "http://182.92.154.98:80"

# def download_dataset(dataset_name):
#     '''
#     :param dataset_name: 数据集名字
#     :return:
#     '''
    # return True


def list_datasets():
    return requests.get(url + "/api/list_datasets")


def evaluate(answer_file):
    '''
    :param answer_file: 按照规范格式化的答案文件 json格式
    :return:
    '''
    # 构建文件上传请求
    files = {'file': open(answer_file, 'rb')}
    response = requests.post(url + "/api/eval", files=files)

    # 打印响应内容
    return response.text
