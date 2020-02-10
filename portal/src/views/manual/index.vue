<template>
  <div class="app-container">
    <el-card
      class="box-card"
      style="margin-bottom: 20px;"
      v-for="(item, index) in manual"
      :key="item['title']"
    >
      <div slot="header" class="clearfix">
        <strong>{{index + ". " + item.title }}</strong>
      </div>
      <div class="text item">{{ item.content }}</div>
    </el-card>
  </div>
</template>

<script>
import { getOptions } from "@/api/options";
export default {
  data() {
    return {
      manual: ""
    };
  },
  mounted() {
    this.fetchManual();
  },
  methods: {
    fetchManual() {
      getOptions({ opt_key: "manual" }).then(response => {
        const { data } = response;
        this.manual = JSON.parse(data);
      });
    }
  }
};
</script>


<style scoped>
body {
  font-family: "Microsoft YaHei";
}
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both;
}

/* .box-card {
  width: 480px;
} */
</style>