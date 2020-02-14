enum ProductType {
    oil = 0,
    rescue = 1
}

interface Common {
    productType: ProductType
}

const state: Common = {
    productType: ProductType.oil
}

export default {
    state: state
}
