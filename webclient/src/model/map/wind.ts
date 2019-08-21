

class WindModel {
    public name: string
    public baseUrl: string
    public layers: string
    public visible: boolean
    public style: string
    public format: string
    public transparent: boolean

    constructor(name: string, baseUrl: string, layers: string, visible: boolean, style: string, format: string, transparent: boolean) {
        this.name = name
        this.baseUrl = baseUrl
        this.layers = layers
        this.visible = visible
        this.style = style
        this.format = format
        this.transparent = transparent
    }

}

export {
    WindModel
}

