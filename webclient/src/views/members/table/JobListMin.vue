<template>
    <div id="job-list" class="card bg-info">
        <div class="card-header card-my-header text-white">case列表</div>
        <div class="card-body card-my-body">
            <ul class="list-group">
                <li
                    class="list-group-item list-my-group-item"
                    v-for="(item, index) in tableData"
                    :key="index"
                    @click="onClick(item)"
                >
                    {{ item.date }}|{{ item.name }}
                </li>
            </ul>
        </div>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
@Component({
    filters: {
        getStatusLevel(val: number) {}
    }
})
export default class JobListUser extends Vue {
    tableData: {
        id: string
        date: string
        name: string
        state: string
        tag: string
        area: string
        percent: number
    }[] = [
        {
            id: '001',
            date: '2016-05-02',
            name: 'case_a',
            state: '作业中',
            tag: 'doing',
            area: 'ind',
            percent: 56
        },
        {
            id: '001',
            date: '2016-05-04',
            name: 'case_b',
            state: '排队中',
            tag: 'wait',
            area: 'scs',
            percent: 0
        },
        {
            id: '001',
            date: '2016-05-01',
            name: 'case_c',
            state: '已结束',
            tag: 'finish',
            area: 'bhs',
            percent: 100
        },
        {
            id: '001',
            date: '2016-05-03',
            name: 'case_d',
            state: '作业中',
            tag: 'doing',
            area: 'ecs',
            percent: 42
        }
    ]
    mounted() {}
    getStatusLevel(val: number): string {
        let level = ''
        if (val < 50) {
            level = 'exception'
        } else if (val < 80) {
            level = 'warning'
        } else if (val >= 80) {
            level = 'success'
        }
        return level
    }

    // 是否为缩小版
    @Prop({ default: false })
    isMin!: boolean

    onClick(item: {
        id: string
        date: string
        name: string
        state: string
        tag: string
        area: string
        percent: number
    }): void {
        // 获取到选定的item的id传给后台即可
        console.log(item.id)
        // 根据指定的case的id以及user id获取模型信息
        // 加载指定模型的平均轨迹
    }

    get computedTest() {
        return null
    }
    get columnWidth() {
        return this.isMin ? 120 : 180
    }

    get rowStyle(): string {
        let style = ''
        if (this.isMin) {
            style = 'background-color:#329d96;color: #fff;font-weight: 500;'
        }
        return style
    }
}
</script>
<style scoped>
.bg-info {
    background-color: transparent !important;
}
#data_list {
    margin-top: 5px;
    background: rgba(73, 115, 165, 0.701);
    padding-right: 8px;
    border-radius: 5px;
}
li {
    list-style: none;
    text-align: left;
}

.list-my-group-item {
    color: rgb(4, 4, 4);
    font-size: 85%;
    background: rgba(184, 206, 200, 0.557);
    padding-top: 5px;
    padding-bottom: 5px;
    font-weight: 400;
    text-shadow: 2px 2px 8px rgb(33, 32, 32);
}

.list-my-group-item:hover {
    color: rgb(255, 255, 255);
    font-size: 85%;
    background: rgba(111, 238, 204, 0.557);
    padding-top: 5px;
    padding-bottom: 5px;
    font-weight: 600;
}
.form-group .control-label {
    color: #ffffff;
    font-family: 'Lato', Helvetica, Arial, sans-serif;
}

#job-list {
    margin-top: 5px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
    /* 0.5s动画过渡的时间 */
}
.fade-enter,
.fade-leave-to {
    opacity: 0;
}

/* #condition .card-my-header {
    background: linear-gradient(to right, #1a6865 30%, rgba(4, 107, 114, 0.639));
    font-size: 90%;
    text-shadow: 2px 2px 8px rgb(33, 32, 32);
  } */

/* 自动以的card-body样式 */
#my_condition .card-my-body {
    /* background: linear-gradient(to right, #248e8a 30%, rgba(4, 107, 114, 0.639)); */
    padding-left: 24px;
}

/* 对于多条件搜索的card的一些样式 */
.card-my-header {
    background: linear-gradient(to right, #1a6865 30%, rgba(4, 107, 114, 0.639));
    font-size: 90%;
    text-shadow: 2px 2px 8px rgb(33, 32, 32);
    width: 100%;
}
/* 自动以的card-body样式 */
.card-my-body {
    background: linear-gradient(to right, #248e8a 30%, rgba(4, 107, 114, 0.639));
    padding: 8px 8px 8px 8px;
    width: 100%;
}
.btn-my {
    background: #2988d2;
}
</style>
