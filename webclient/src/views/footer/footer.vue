<template>
  <div>
    <div id="footer">footer</div>
  </div>
</template>
<script lang="ts"
>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class footer extends Vue {
  mydata: any = null;
  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped>
#footer {
  display: flex;
  flex-direction: column;
  flex: 1;
  background: #2f8da5;
}
</style>