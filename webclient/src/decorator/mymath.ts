/**
 * 角度转换装饰器
 *
 * @param {Object} target
 * @param {string} propertyName
 * @param {PropertyDescriptor} propertyDescriptor
 * @returns {PropertyDecorator}
 */
// function dirConvertDec(
//     target:Object,
//     propertyName:string,
//     propertyDescriptor:PropertyDescriptor
// ):PropertyDecorator{
//     const method=propertyDescriptor.value;
//     propertyDescriptor.value=function(...args:any[]){
//         const res=method.apply(this,args);
//         // 将角度进行转换
//         /*
//             若角度为负数，说明在第三或第四象限，res=360+val
//         */
//        let resConvert=res;
//        if(res<0){
//             resConvert=360+res
//        }
//        return resConvert;        
//     }
//     return propertyDescriptor
// }

// export {dirConvertDec}