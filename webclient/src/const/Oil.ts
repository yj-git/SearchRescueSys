
const optionsFactors: { value: string, label: string, key: number }[] = [
    {
        value: "thickness",
        label: "油膜厚度",
        key: 0
    },
    {
        value: "mass",
        label: "油膜质量",
        key: 1
    }
]

const optionsShowTypes: { value: string, label: string, key: number }[] = [{
    value: "scatter",
    label: "散点",
    key: 0
},
{
    value: "heatmap",
    label: "热图",
    key: 1
}]

export {
    optionsFactors, optionsShowTypes
}