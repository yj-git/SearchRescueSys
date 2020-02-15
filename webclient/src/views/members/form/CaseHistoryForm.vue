<template>
    <div id="my-history-form">
        <div class="title">历史作业统计</div>
        <ul>
            <li v-for="temp in caseDailyList" :key="temp.id">
                <span>{{ moment(temp.current).format('L') }}</span>
                <span>
                    <b>{{ temp.nums }}</b>
                    <small>cases</small>
                </span>
            </li>
            <!-- <li>
                <span>2019-11-04</span>
                <span>
                    <b>3</b>
                    <small>cases</small>
                </span>
            </li>
            <li>
                <span>2019-11-06</span>
                <span>
                    <b>9</b>
                    <small>cases</small>
                </span>
            </li>
            <li>
                <span>2019-11-08</span>
                <span>
                    <b>6</b>
                    <small>cases</small>
                </span>
            </li> -->
        </ul>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import { CaseDailyDetail } from '@/middle_model/case'
import moment from 'moment'
@Component({})
export default class CaseHistoryForm extends Vue {
    @Prop()
    caseDailyList: Array<CaseDailyDetail>
    mounted() {}
    get computedTest() {
        return null
    }
}
</script>
<style scoped lang="less">
@import '../../../styles/base';
#my-history-form {
    background: #0be2cc !important;
    height: 100%;
    @formmoreshadow();
    margin-left: 1em;
    width: 300px;
    .title {
        color: white;
        font-size: 1em;
        height: 3em;
        background: rgba(0, 0, 0, 0.12);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 400;
    }
    ul {
        padding: 0;
        li {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            list-style-type: none;
            //   justify-content: space-around;
            color: white;
            font-weight: 400;
            font-size: 1.25em;
            flex-direction: row;
            margin: 1em;
        }
    }
}
</style>
