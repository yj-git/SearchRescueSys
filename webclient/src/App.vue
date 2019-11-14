<template>
  <div id="app">
    <Header></Header>
    <Center></Center>
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/> -->
    <Footer></Footer>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import HelloWorld from "./components/HelloWorld.vue";
import Header from "@/views/header/header.vue";
import Footer from "@/views/footer/footer.vue";
import Center from "@/views/center/center.vue";
@Component({
  components: {
    HelloWorld,
    Header,
    Footer,
    Center
  }
})
export default class App extends Vue {}
</script>

<style lang="scss">
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #dbe347;
  background: #87a2bd;
  display: flex;
  height: 100vh;
  min-height: 100vh;
  flex-direction: column;
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
