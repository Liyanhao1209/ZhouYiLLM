<template>
  <div class="home">
    <img alt="ZhouYi logo" src="../assets/bagua.png">
    <HelloWorld msg="欢迎使用周易在线"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>
