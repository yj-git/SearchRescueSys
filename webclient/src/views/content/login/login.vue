<template>
    <div id="my-form">
        <div class="my-container">
            <div class="login-box">
                <div class="login-form-my">
                    <form>
                        <div>
                            <span class="login-title-my">溢油搜救系统</span>
                            <div class="login-wrap-my">
                                <!-- <span>用户名</span> -->
                                <label for="exampleInputName2">用户名</label>
                                <input
                                    type="text"
                                    v-model="userName"
                                    class="form-control"
                                    placeholder="用户名"
                                />
                            </div>
                            <div class="login-wrap-my">
                                <!-- <span>用户名</span> -->
                                <label for="exampleInputName2">密码</label>
                                <input
                                    type="password"
                                    v-model="parseWord"
                                    class="form-control"
                                    placeholder="密码"
                                />
                            </div>
                            <div class="login-wrap-my">
                                <div class="login-form-btn">
                                    <div class="login-btn-div"></div>
                                    <!-- <button class="login-btn" @click="login">登录</button> -->
                                    <input
                                        class="login-btn"
                                        id="jsLoginBtn"
                                        type="button"
                                        @click="login"
                                        value="登录"
                                    />
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
@Component({})
export default class Login extends Vue {
    userName = ''
    pwd = '123'
    // sdfsdf: string = 123
    mounted() {}
    login() {}
    get computedTest() {
        return null
    }
}
</script>
<style scoped>
#my-form {
    position: relative;
    height: 100%;
    background: linear-gradient(45deg, #588fe9 25%, #16a085 50%);
    /* height: 100%; */
    /* min-height: 100%; */
}

/* body {
            background-color: #ECEFF1;
            color: #37474F;
            font-family: 'Raleway', sans-serif;
            font-weight: 300;
            font-size: 16px;
        } */
.my-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-wrap: wrap;

    /* 主轴上的对其方式 */
    justify-content: center;
    /* 交叉轴上的对其方式 */
    align-items: center;
}

.login-box {
    width: 500px;
    height: 500px;
    background: #fff;
    border-radius: 10px;
    /* width: 400px; */
    overflow: hidden;

    padding-left: 55px;
    padding-right: 55px;
    padding-top: 65px;
    padding-bottom: 45px;
}

.login-form-my {
    width: 100%;
}

.login-title-my {
    display: block;
    font-family: Poppins-Bold;
    font-size: 39px;
    color: #333333;
    line-height: 1.2;
    text-align: center;
}

.login-wrap-my {
    width: 100%;
    margin-top: 10px;
    margin-bottom: 20px;
}

.login-wrap-my > input {
    font-family: Poppins-Medium;
    font-size: 16px;
    color: #333333;
    line-height: 1.2;
    /* display: block; */
    width: 100%;
    height: 55px;
    background: transparent;
    padding: 0 7px 0 43px;

    outline: none;
    border: none;
}

.login-form-btn {
    width: 100%;
    display: block;
    position: relative;
    z-index: 1;
    border-radius: 25px;
    overflow: hidden;
    margin: 0 auto;
}

.login-btn-div {
    position: absolute;
    z-index: -1;
    width: 300%;
    height: 100%;
    /* background: #a64bf4; */
    /* background: -webkit-linear-gradient(right, #00dbde, #fc00ff, #00dbde, #fc00ff);
			background: -o-linear-gradient(right, #00dbde, #fc00ff, #00dbde, #fc00ff);
			background: -moz-linear-gradient(right, #00dbde, #fc00ff, #00dbde, #fc00ff); */
    /* background: linear-gradient(right, #00dbde, #fc00ff, #00dbde, #fc00ff); */
    background: linear-gradient(45deg, #588fe9 25%, #16a085 50%);
    top: 0;
    left: -100%;
    /* -webkit-transition: all 0.4s;
			-o-transition: all 0.4s;
			-moz-transition: all 0.4s; */
    transition: all 0.4s;
}

.login-btn-div:hover {
    background: linear-gradient(45deg, #161fa0 50%, rgb(168, 88, 233) 25%);
}

.login-btn {
    font-family: Poppins-Medium;
    font-size: 16px;
    color: #fff;
    line-height: 1.2;
    text-transform: uppercase;
    /* display: -webkit-box;
			display: -webkit-flex;
			display: -moz-box;
			display: -ms-flexbox; */
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 20px;
    width: 100%;
    height: 50px;

    border: none;
    background: transparent;
}
</style>
