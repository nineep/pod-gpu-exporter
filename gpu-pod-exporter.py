#! -*- coding: utf-8 -*-

import os
import subprocess
import prometheus_client
from prometheus_client.core import CollectorRegistry, InfoMetricFamily
from flask import Response, Flask, render_template

project_path = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(project_path, 'templates')

test_data = [
    {'node': 'node01', 'namespace': 'default', 'pod_name': 'test',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '4080ti'},
    {'node': 'node01', 'namespace': 'default', 'pod_name': 'test2',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '4080ti'},
    {'node': 'node03', 'namespace': 'default3', 'pod_name': 'test2',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '4080ti'},
    {'node': 'node01', 'namespace': 'default2', 'pod_name': 'test2',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '4080ti'},
    {'node': 'node03', 'namespace': 'default', 'pod_name': 'test2',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
    {'node': 'node03', 'namespace': 'default3', 'pod_name': 'test4',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
    {'node': 'node01', 'namespace': 'default', 'pod_name': 'test2',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
    {'node': 'node02', 'namespace': 'default3', 'pod_name': 'test2',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
    {'node': 'node01', 'namespace': 'default2', 'pod_name': 'test2',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
    {'node': 'node03', 'namespace': 'default', 'pod_name': 'test2',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
    {'node': 'node02', 'namespace': 'default2', 'pod_name': 'test2',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2040ti'},
    {'node': 'node02', 'namespace': 'default', 'pod_name': 'test3',
     'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb91', 'gpu_model': '2080ti'}]

app = Flask(__name__, template_folder=templates_path)


class CustomCollector(object):
    """
    metrics_label_dict_list: 列表中多个字典元素 [{'k1':1}, {'k2':2} ...]
    """
    def __init__(self, metric_name, metric_describe, metric_label_list, metric_label_dict_list):
        self.metric_name = metric_name
        self.metric_describe = metric_describe
        self.metric_label_list = metric_label_list
        self.metric_label_dict_list = metric_label_dict_list

    def collect(self):
        c = InfoMetricFamily(self.metric_name, self.metric_describe)
        for metric_label_dict in self.metric_label_dict_list:
            c.add_metric(self.metric_label_list, metric_label_dict)

        yield c


def get_pod_gpu():
    """
    :return: pod gpu list, elements are dict
    """
    cmd = "kubectl-gpu-info -all|grep -v + | grep -v NODE | awk -F '|' '{print $2,$3,$4,$6,$7}'"
    labels = ['node', 'namespace', 'pod_name', 'gpu_id', 'gpu_model']
    cmd_res = subprocess.getstatusoutput(cmd)

    if cmd_res[0] == 0:
        pod_gpu_list_info = []
        # 命令执行成功， cmd res 为 cmd_res[1], 每项由\n分割
        res_list = cmd_res[1].split('\n')
        for value_ls in res_list:
            new_ls = value_ls.strip().split()
            d = dict(zip(labels, new_ls))
            pod_gpu_list_info.append(d)
        return pod_gpu_list_info
    else:
        print('命令执行失败！, 请确认 kubectl-gpu-info 可执行！')


@app.route('/')
def index():
    return 'Pod GPU map metrics ! Jump to "/metrics" and "/mrtrics/nodes" to get specific metrics'
    # render_template('index.html')


@app.route('/metrics')
def all_pod_gpu_map():
    # 自定义参数，供测试用
    #pod_gpu_list = test_data
    # 即时从k8s控制平面获取最新的pod和gpu信息
    pod_gpu_list = get_pod_gpu()

    # 定义metrics
    metric_name = 'pod_and_gpu_map'
    metric_describe = 'Provide a mapping relationship between pod and gpu'
    metric_label_list = ['node', 'namespace', 'pod_name', 'gpu_id', 'gpu_model']
    metric_label_dict_list = pod_gpu_list

    # 注册 or 重新注册
    REGISTRY = CollectorRegistry(auto_describe=False)
    REGISTRY.register(CustomCollector(metric_name, metric_describe,
                                      metric_label_list, metric_label_dict_list))

    # 生成最近的注册数据结果
    res = prometheus_client.generate_latest(REGISTRY)

    return Response(res, mimetype="text/plain")


@app.route('/metrics/nodes')
def node_gpu_pod_map():
    # 自定义参数，供测试用
    #pod_gpu_list = test_data
    # 即时从k8s控制平面获取最新的pod和gpu信息
    pod_gpu_list = get_pod_gpu()

    # 处理命令行传来的数据，转换为 [
    # {'node1': [{labels}, {labels}...]},
    # {'node2': [{labels}, {labels}]},
    # {'node3': [{labels}]},
    # ...]
    node_label_ls = []
    node_name_ls = []
    for d in pod_gpu_list:
        node_name = d.get('node')

        # 如果遍历到的node已经存在，更新已有node字典的value, value类型list
        if node_name in node_name_ls:
            for joined_dict in node_label_ls:
                if node_name in joined_dict:
                    joined_dict[node_name].append(d)
        # 如果遍历到新的node，那么形成一个字典，加入到外层list
        else:
            node_name_ls.append(node_name)
            new_dict = {node_name: [d]}
            node_label_ls.append(new_dict)
    # print('node_name_ls:', node_name_ls)
    # print('node_label_ls:', node_label_ls)

    # 定义固定的metrics
    metric_describe = "Provide every node's pod and gpu mapping relationship"
    metric_label_list = ['node', 'namespace', 'pod_name', 'gpu_id', 'gpu_model']

    # 注册 or 重新注册
    REGISTRY = CollectorRegistry(auto_describe=False)

    # 动态获取,并赋值metrics。循环注册metrics
    for node_dict in node_label_ls:
        for k, v in node_dict.items():
            # print('k', k)
            # print('v', v)
            metric_name = k
            metric_label_dict_list = v
            REGISTRY.register(CustomCollector(metric_name, metric_describe,
                                              metric_label_list, metric_label_dict_list))

    # 生成最近的注册数据结果
    res = prometheus_client.generate_latest(REGISTRY)

    return Response(res, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=9401)
