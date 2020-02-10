<template>
  <div class="app-container">
    <el-card class="box-card" style="font-size: 14px;">
      <el-row>
        <el-col :span="8">
          <div>
            <label>概要统计/月：</label>
            <span>{{ resumeStatdateMonth }}</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div>
            <label>概要统计/日：</label>
            <span>{{ resumeStatdateDay }}</span>
          </div>
        </el-col>
      </el-row>
      <br />
      <el-row>
        <el-col :span="8">
          <div>
            <label>按价格统计：</label>
            <span>{{ arrangePriceStatdate }}</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div>
            <label>按总价统计：</label>
            <span>{{ arrangeAmountStatdate }}</span>
          </div>
        </el-col>
      </el-row>
      <br />
      <el-row>
        <el-col :span="8">
          <div>
            <label>按面积统计：</label>
            <span>{{ arrangeAreaStatdate }}</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div>
            <label>按房型统计：</label>
            <span>{{ arrangeRoomStatdate }}</span>
          </div>
        </el-col>
      </el-row>
    </el-card>
    <el-card class="box-card" style="font-size: 14px; margin-top: 20px;">
      <el-row>
        <el-col :span="24">
          <div v-if="spidermanFrame !== '' && spidermanFrame !== null">
            <label>数据采集规则：</label>
            <p>城市列表：{{spidermanFrame.city}}</p>
            <p>统计类型：{{spidermanFrame.stattype}}</p>
            <p>物业类型：{{spidermanFrame.property}}</p>
            <p>房型：{{spidermanFrame.arrange.room}}</p>
            <p>面积：{{spidermanFrame.arrange.area}}</p>
            <p>单价：{{spidermanFrame.arrange.price}}</p>
            <p>总价：{{spidermanFrame.arrange.amount}}</p>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { getOptions } from "@/api/options";
export default {
  data() {
    return {
      spidermanFrame: "",
      resumeStatdateMonth: "",
      resumeStatdateDay: "",
      arrangeRoomStatdate: "",
      arrangeAreaStatdate: "",
      arrangeAmountStatdate: "",
      arrangePriceStatdate: ""
    };
  },
  mounted() {
    this.fetchspidermanFrame();
    this.fetchOptions();
  },
  methods: {
    fetchspidermanFrame() {
      getOptions({ opt_key: "spiderman_frame" }).then(response => {
        const { data } = response;
        this.spidermanFrame = JSON.parse(data);
      });
    },
    fetchOptions() {
      getOptions({ opt_key: "resume_statdate_month" }).then(response => {
        const { data } = response;
        this.resumeStatdateMonth = data;
      });
      getOptions({ opt_key: "resume_statdate_day" }).then(response => {
        const { data } = response;
        this.resumeStatdateDay = data;
      });
      getOptions({ opt_key: "arrange_room_statdate" }).then(response => {
        const { data } = response;
        this.arrangeRoomStatdate = data;
      });
      getOptions({ opt_key: "arrange_area_statdate" }).then(response => {
        const { data } = response;
        this.arrangeAreaStatdate = data;
      });
      getOptions({ opt_key: "arrange_amount_statdate" }).then(response => {
        const { data } = response;
        this.arrangeAmountStatdate = data;
      });
      getOptions({ opt_key: "arrange_price_statdate" }).then(response => {
        const { data } = response;
        this.arrangePriceStatdate = data;
      });
    }
  }
};
</script>

<style scoped>
.line {
  text-align: center;
}
</style>
