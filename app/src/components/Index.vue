<template>
  <div>
    {{token}}
  </div>
</template>

<script>
import Cookies from 'js-cookie'
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'Index',
  data () {
    return {
      token: ''
    }
  },
  created () {
    this.token = Cookies.get('_xsrf')
    axios.post('/account/login', qs.stringify({
      name: '1',
      passwd: '1',
      _xsrf: this.token
    })).then((res) => {
      console.log(res)
    }).catch((err) => {
      console.log(err)
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
