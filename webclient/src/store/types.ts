// 引入了各种可能得状态
export const ACTIVATION_BEGIN = 'ACTIVATION_BEGIN'
export const ACTIVATION_CLEAR = 'ACTIVATION_CLEAR'
export const ACTIVATION_FAILURE = 'ACTIVATION_FAILURE'
export const ACTIVATION_SUCCESS = 'ACTIVATION_SUCCESS'
export const LOGIN_BEGIN = 'LOGIN_BEGIN'
export const LOGIN_CLEAR = 'LOGIN_CLEAR'
export const LOGIN_FAILURE = 'LOGIN_FAILURE'
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS'
export const LOGOUT = 'LOGOUT'
export const PASSWORD_EMAIL_BEGIN = 'PASSWORD_EMAIL_BEGIN'
export const PASSWORD_EMAIL_CLEAR = 'PASSWORD_EMAIL_CLEAR'
export const PASSWORD_EMAIL_FAILURE = 'PASSWORD_EMAIL_FAILURE'
export const PASSWORD_EMAIL_SUCCESS = 'PASSWORD_EMAIL_SUCCESS'
export const PASSWORD_RESET_BEGIN = 'PASSWORD_RESET_BEGIN'
export const PASSWORD_RESET_CLEAR = 'PASSWORD_RESET_CLEAR'
export const PASSWORD_RESET_FAILURE = 'PASSWORD_RESET_FAILURE'
export const PASSWORD_RESET_SUCCESS = 'PASSWORD_RESET_SUCCESS'
export const REGISTRATION_BEGIN = 'REGISTRATION_BEGIN'
export const REGISTRATION_CLEAR = 'REGISTRATION_CLEAR'
export const REGISTRATION_FAILURE = 'REGISTRATION_FAILURE'
export const REGISTRATION_SUCCESS = 'REGISTRATION_SUCCESS'
// export const SET_TOKEN = 'SET_TOKEN'
// TODO:[-] 20-02-07 jwt返回的token的key为 'token'
export const SET_TOKEN = 'token'
// 移除jwt的token,在localStorage中保存的token
export const REMOVE_TOKEN = 'REMOVE_TOKEN'
// 产品的种类(主要是oil还是rescue)
export const SET_PRODUCT_TYPE = 'SET_PRODUCT_TYPE'
export const GET_PRODUCT_TYPE = 'GET_PRODUCT_TYPE'

// case 相关
export const SET_CASE_CODE = 'SET_CASE_CODE'
export const GET_CASE_CODE = 'GET_CASE_CODE'

// map 相关
export const SET_MAP_NOW = 'SET_MAP_NOW'
export const GET_MAP_NOW = 'GET_MAP_NOW'
