# pod gpu metrics exporter
采集k8s节点上pod所使用的GPU的对应关系   


## 支持的metrics
#### 访问endpoint: http://127.0.0.1:9401/metrics
    
    # HELP pod_and_gpu_map_info Provide a mapping relationship between pod and gpu
    # TYPE pod_and_gpu_map_info gauge
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti",pod_name="test"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test4"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default3",node="ti2",pod_name="test2"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti7",pod_name="test2"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2040ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    pod_and_gpu_map_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb91",gpu_model="2080ti",namespace="default",node="ti",pod_name="test3"} 1.0


#### 访问endpoint: http://127.0.0.1:9401/metrics/nodes

    # HELP ti_info Provide every node's pod and gpu mapping relationship
    # TYPE ti_info gauge
    ti_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti",pod_name="test"} 1.0
    ti_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti",pod_name="test2"} 1.0
    # HELP ti2_info Provide every node's pod and gpu mapping relationship
    # TYPE ti2_info gauge
    ti2_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    ti2_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    ti2_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    ti2_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test4"} 1.0
    ti2_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    ti2_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default3",node="ti2",pod_name="test2"} 1.0
    ti2_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test2"} 1.0
    # HELP ti7_info Provide every node's pod and gpu mapping relationship
    # TYPE ti7_info gauge
    ti7_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti7",pod_name="test2"} 1.0
    ti7_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2040ti",namespace="default",node="ti7",pod_name="test2"} 1.0
    ti7_info{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb91",gpu_model="2080ti",namespace="default",node="ti7",pod_name="test3"} 1.0



## 遗弃的metrics
#### 访问endpoint：http://127.0.0.1:9401/metrics

    # HELP POD_GPU_MAP_INFO_0 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_0 gauge
    POD_GPU_MAP_INFO_0{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti",pod_name="test"} 0.0
    # HELP POD_GPU_MAP_INFO_1 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_1 gauge
    POD_GPU_MAP_INFO_1{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti2",pod_name="test2"} 0.0
    # HELP POD_GPU_MAP_INFO_2 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_2 gauge
    POD_GPU_MAP_INFO_2{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti2",pod_name="test2"} 0.0
    # HELP POD_GPU_MAP_INFO_3 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_3 gauge
    POD_GPU_MAP_INFO_3{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="4080ti",namespace="default",node="ti2",pod_name="test2"} 0.0
    # HELP POD_GPU_MAP_INFO_4 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_4 gauge
    POD_GPU_MAP_INFO_4{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test2"} 0.0
    # HELP POD_GPU_MAP_INFO_5 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_5 gauge
    POD_GPU_MAP_INFO_5{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test4"} 0.0
    # HELP POD_GPU_MAP_INFO_6 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_6 gauge
    POD_GPU_MAP_INFO_6{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test2"} 0.0
    # HELP POD_GPU_MAP_INFO_7 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_7 gauge
    POD_GPU_MAP_INFO_7{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default3",node="ti2",pod_name="test2"} 0.0
    # HELP POD_GPU_MAP_INFO_8 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_8 gauge
    POD_GPU_MAP_INFO_8{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti2",pod_name="test2"} 0.0
    # HELP POD_GPU_MAP_INFO_9 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_9 gauge
    POD_GPU_MAP_INFO_9{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2080ti",namespace="default",node="ti7",pod_name="test2"} 0.0
    # HELP POD_GPU_MAP_INFO_10 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_10 gauge
    POD_GPU_MAP_INFO_10{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb61",gpu_model="2040ti",namespace="default",node="ti2",pod_name="test2"} 0.0
    # HELP POD_GPU_MAP_INFO_11 pod gpu map info - please use labels value to match pod and gpu
    # TYPE POD_GPU_MAP_INFO_11 gauge
    POD_GPU_MAP_INFO_11{gpu_id="GPU-40f717b2-01dc-1a31-6b17-d487ffe7cb91",gpu_model="2080ti",namespace="default",node="ti",pod_name="test3"} 0.0

*https://github.com/tkestack/gpu-manager 提供metric，IP:5678/metric默认未开启*
*<table class="wrapped confluenceTable"><colgroup><col style="width: 228.0px;" /><col style="width: 210.0px;" /><col style="width: 389.0px;" /><col style="width: 248.0px;" /></colgroup><tbody><tr><th class="confluenceTh">metric name</th><th class="confluenceTh">help</th><th class="confluenceTh">说明</th><th class="confluenceTh" colspan="1">k8s yaml def</th></tr><tr><td class="confluenceTd">container_gpu_memory_total</td><td class="confluenceTd">gpu memory usage in MiB</td><td class="confluenceTd">pod的gpu显存使用量 MiB</td><td class="confluenceTd" colspan="1"><br /></td></tr><tr><td class="confluenceTd">container_request_gpu_memory</td><td class="confluenceTd">request of gpu memory in MiB</td><td class="confluenceTd">pod申请的gpu显存总量 MiB</td><td class="confluenceTd" colspan="1"><pre><code>vcuda-memory: 30</code><br />申请显存 30 *256MiB= 7680M</pre></td></tr><tr><td class="confluenceTd">container_gpu_utilization</td><td class="confluenceTd">gpu utilization</td><td class="confluenceTd"><p>pod的gpu算力使用率：</p><p>每块卡metric值为0-100，每块卡使用率以及所有卡使用率和</p></td><td class="confluenceTd" colspan="1"><br /></td></tr><tr><td class="confluenceTd" colspan="1">container_request_gpu_utilization</td><td class="confluenceTd" colspan="1">request of gpu utilization</td><td class="confluenceTd" colspan="1"><p>pod申请的gpu算力(多少vgpu卡)：</p><p>申请0.5块卡，metric值为0.5；申请2块卡，metric值为2</p></td><td class="confluenceTd" colspan="1"><pre><code>vcuda-core: 200<br /></code>申请卡数 200 /100= 2</pre><p>注意：一个pod申请： 0-100，或者100倍数</p></td></tr></tbody></table>*
