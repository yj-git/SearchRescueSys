/*
    所有的和 geo相关的类
*/

/**
 *  coverage 的 概述信息 中间类
 *
 * @class CoverageDetailMidModel
 */
class CoverageDetailMidModel {
    public fileSize: string
    public fileName: string
    public dimessions: string[]
    public variables: string[]
    public forecastStart: Date
    public forecastEnd: Date
    public(
        size: string,
        fileName: string,
        dimessions: string[],
        variables: string[],
        start: Date,
        end: Date
    ) {
        this.fileName = fileName
        this.fileSize = size
        this.dimessions = dimessions
        this.variables = variables
        this.forecastStart = start
        this.forecastEnd = end
    }
}

export { CoverageDetailMidModel }
