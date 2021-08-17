// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));
var myChart1 = echarts.init(document.getElementById('main1'));

// 指定图表的配置项和数据
var option = {
    tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        data: [1, 2, 3, 4, 5],
        axisTick: {
            alignWithLabel: true
        },
        name: '前七日阅读量变化',
        nameLocation: 'middle',
        nameTextStyle: {
            lineHeight: 35
        }
    },
    yAxis: {
        type: 'value',
        splitLine: {    //网格线
            lineStyle: {
                type: 'dashed'    //设置网格线类型 dotted：虚线   solid:实线
            },
            show: true //隐藏或显示
        },
        axisLabel: {
            show: false//刻度标签
        }
    },
    series: [{
        data: [1, 2, 3, 4],
        type: 'line',
        name: '阅读量',
        itemStyle: {normal: {label: {show: true}}}
    }]
};

// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
myChart1.setOption(option);