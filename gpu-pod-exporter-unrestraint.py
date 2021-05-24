#! -*- coding: utf-8 -*-

import subprocess
import prometheus_client
from prometheus_client import Counter, Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask

app = Flask(__name__)
# REGISTRY = CollectorRegistry(auto_describe=False)


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


@app.route('/metrics')
def res_value():
    """
    gauge_name,
    gauge_describe,
    labels_name
    """
    # 自定义参数，供测试
    pod_gpu_list = [
        {'node': 'ti', 'namespace': 'default', 'pod_name': 'test', 'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61',
         'gpu_model': '4080ti'},
        {'node': 'ti2', 'namespace': 'default', 'pod_name': 'test2',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '4080ti'},
        {'node': 'ti2', 'namespace': 'default', 'pod_name': 'test2',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '4080ti'},
        {'node': 'ti2', 'namespace': 'default', 'pod_name': 'test2',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '4080ti'},
        {'node': 'ti2', 'namespace': 'default', 'pod_name': 'test2',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
        {'node': 'ti2', 'namespace': 'default', 'pod_name': 'test4',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
        {'node': 'ti2', 'namespace': 'default', 'pod_name': 'test2',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
        {'node': 'ti2', 'namespace': 'default3', 'pod_name': 'test2',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
        {'node': 'ti2', 'namespace': 'default', 'pod_name': 'test2',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
        {'node': 'ti7', 'namespace': 'default', 'pod_name': 'test2',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2080ti'},
        {'node': 'ti2', 'namespace': 'default', 'pod_name': 'test2',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61', 'gpu_model': '2040ti'},
        {'node': 'ti', 'namespace': 'default', 'pod_name': 'test3',
         'gpu_id': 'GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb91', 'gpu_model': '2080ti'}]
    # 即时重k8s获取最新的pod和gpu信息
    #pod_gpu_list = get_pod_gpu()

    # 注册 or 重新注册
    REGISTRY = CollectorRegistry(auto_describe=False)

    for inx in range(len(pod_gpu_list)):
        pod_gpu_map_info_name = 'POD_GPU_MAP_INFO_' + str(inx)
        pod_gpu_map_info_name = Gauge(pod_gpu_map_info_name,
                                      'pod gpu map info - please use labels value to match pod and gpu',
                                      ['node', 'namespace', 'pod_name', 'gpu_id', 'gpu_model'],
                                      registry=REGISTRY)
        pod_gpu_dict = pod_gpu_list[inx]
        node = pod_gpu_dict.get('node')
        namespace = pod_gpu_dict.get('namespace')
        pod_name = pod_gpu_dict.get('pod_name')
        gpu_id = pod_gpu_dict.get('gpu_id')
        gpu_model = pod_gpu_dict.get('gpu_model')
        pod_gpu_map_info_name.labels(node=node, namespace=namespace, pod_name=pod_name,
                                     gpu_id=gpu_id, gpu_model=gpu_model)

    return Response(prometheus_client.generate_latest(REGISTRY),
                    mimetype="text/plain")


@app.route('/')
def index():
    return "Pod GPU map metrics!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=9401)
