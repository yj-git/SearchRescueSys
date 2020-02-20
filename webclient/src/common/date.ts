import moment from 'moment'
/**
 * 获取总共包含的自然日的数量
 *
 * @param {Date} start
 * @param {Date} end
 * @returns {number}
 */
function getDaysNum(start: Date, end: Date): number {
    /* 
        大体思路：遍历并add hours ,将当前的day放入一个数组中
        每次循环时再次判断这个date是否存在于当前的list中
    */
    const diff = end.getTime() - start.getTime()
    const diffHours = diff / (60 * 1000 * 60)
    const days: Array<number> = []
    let tempDate = moment(start)
    for (let index = 0; index < diffHours; index++) {
        // 若不存在则插入days list中
        if (days.indexOf(tempDate.date()) === -1) {
            days.push(tempDate.date())
        }
        tempDate = tempDate.add(1, 'h')
        //    start.getUTCDate()
    }
    return days.length
    //    for()
}

function formatDate(now: Date) {
    return moment(now).format('YYYY-MM-DD HH')
}

export { getDaysNum, formatDate }
