import moment from "moment"
/**
 * 时间轴上的时间 model
 *
 * @class DateModel
 */
class DateModel {
    public value: number
    // public label: String
    public date: Date
    public children: Array<DateModel>
    public constructor(value: number, date: Date, children: Array<DateModel> = []) {
        this.value = value
        this.date = date
        this.children = children
    }
    /**
     * 返回当前时间对应的str
     *
     * @memberof DateModel
     */
    public dateStr() {
        var dateStr = this.date.toLocaleDateString()
        return dateStr
    }

    public datetimeStr() {
        var dtStr = moment(this.date).format("DD HH:mm")
        return dtStr
    }
}

export {
    DateModel
}