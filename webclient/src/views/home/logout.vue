<template>
    <div></div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
@Component({})
export default class Logout extends Vue {
    mydata: any = null
    mounted() {
        this.$store.dispatch('auth/logout')
        this.$router.push('/login')
    }
    get computedTest() {
        return null
    }
}
</script>
<style scoped></style>
