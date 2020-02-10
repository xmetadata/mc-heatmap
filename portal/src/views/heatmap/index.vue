<template>
  <div class="app-container">
    <div class="filter-container" style="padding: 10px 0;">
      <el-cascader
        v-model="listQuery.scope"
        :options="scope"
        placeholder="请选择"
        style="width:180px;"
        @change="fetchData"
      ></el-cascader>
      <el-cascader
        v-model="listQuery.stattype"
        :options="stattype"
        placeholder="请选择"
        style="width:180px;"
        @change="changeSelect"
      ></el-cascader>
      <el-select
        v-model="listQuery.property"
        placeholder="请选择"
        style="width:120px;"
        @change="fetchData"
      >
        <el-option
          v-for="item in property"
          :key="item"
          :label="item"
          :value="item"
        ></el-option>
      </el-select>
      <el-select
        v-model="listQuery.datetype"
        placeholder="请选择"
        style="width:100px;"
        @change="changeQueryDate"
      >
        <el-option
          v-for="item in datetype"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
      <el-date-picker
        v-show="listQuery.datetype === 'year'"
        v-model="datePicker"
        type="year"
        format="yyyy 年"
        @change="fetchData"
      ></el-date-picker>
      <el-date-picker
        v-show="listQuery.datetype === 'monthrange'"
        v-model="datePicker"
        type="monthrange"
        format="yyyy 年 MM 月"
        @change="fetchData"
      ></el-date-picker>
      <el-date-picker
        v-show="listQuery.datetype === 'month'"
        v-model="datePicker"
        type="month"
        format="yyyy 年 MM 月"
        @change="fetchData"
      ></el-date-picker>
      <el-date-picker
        v-show="listQuery.datetype === 'week'"
        v-model="datePicker"
        type="week"
        format="yyyy 年 第 WW 周"
        @change="fetchData"
      ></el-date-picker>
      <el-date-picker
        v-show="listQuery.datetype === 'daterange'"
        v-model="datePicker"
        type="daterange"
        format="yyyy 年 MM 月 dd 日"
        @change="fetchData"
      ></el-date-picker>
      <el-checkbox
        v-model="showExFilter"
        class="filter-item"
        style="margin-left:15px;"
        :disabled="listQuery.stattype[0]==='stock' || listQuery.datetype==='daterange' || listQuery.datetype==='week'?true:false"
        @change="exFilter"
      >按属性过滤</el-checkbox>
    </div>

    <div v-show="showExFilter">
      <el-form label-width="80px" size="small">
        <el-form-item label="自定义：">
          <el-switch v-model="customFilter" @change="exFilter"></el-switch>
        </el-form-item>
        <div v-show="customFilter === false">
          <el-form-item
            v-for="groupItem in radioGroup"
            :label="groupItem.radio_group_label + '：'"
            :key="groupItem.radio_group_label"
          >
            <el-radio-group v-model="radioChecked" @change="setArrange">
              <el-radio
                v-for="radioItem in groupItem.radio_group"
                :label="radioItem.value"
                :key="radioItem.value"
              >{{radioItem.label + ' ' + groupItem.radio_group_unit}}</el-radio>
            </el-radio-group>
          </el-form-item>
        </div>
        <div v-show="customFilter === true">
          <el-form-item label="过滤项：">
            <el-select v-model="listQuery.arrange" placeholder="请选择">
              <el-option
                v-for="item in radioGroup"
                :key="item.radio_group_value"
                :label="item.radio_group_label + '/' + item.radio_group_unit"
                :value="item.radio_group_value"
                :disabled="item.disabled"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="范围段：">
            <el-input v-model="interval_from" placeholder="请输入起始值" style="width: 200px"></el-input>
            <span>-</span>
            <el-input v-model="interval_to" placeholder="请输入结束值" style="width: 200px"></el-input>
            <el-button type="primary" @click="onSubmit">搜 索</el-button>
          </el-form-item>
        </div>
      </el-form>
    </div>

    <baidu-map
      class="bm-view"
      :style="conheight"
      :center="center"
      :zoom="zoom"
      @ready="handler"
      ak="lc6PdvUfQ04MYItn8wz0HIOGbI7twGU8"
      v-loading="loading"
    >
      <bm-navigation anchor="BMAP_ANCHOR_TOP_RIGHT"></bm-navigation>
      <bm-control style="padding: 10px;">
        <button class="bm-button" @click="showMarker">
          <span v-if="markerVision">隐藏项目</span>
          <span v-else>显示项目</span>
        </button>
      </bm-control>
      <bml-heatmap :data="data" :max="max" :radius="20"></bml-heatmap>
      <bml-marker-clusterer :averageCenter="true">
        <bm-marker
          v-for="marker of markers"
          :position="{lng: marker.lng, lat: marker.lat}"
          :key="marker.lng"
        >
          <bm-label
            :content="marker.count + '【' + marker.name + '】' + marker.address"
            :offset="{width: 20, height: -10}"
          />
        </bm-marker>
      </bml-marker-clusterer>
    </baidu-map>
  </div>
</template>

<script>
import { getOptions } from "@/api/options";
import { getDataset } from "@/api/dataset";
import BaiduMap from "vue-baidu-map/components/map/Map.vue";
import {
  BmControl,
  BmLabel,
  BmMarker,
  BmNavigation,
  BmlHeatmap,
  BmlMarkerClusterer
} from "vue-baidu-map";

export default {
  components: {
    BaiduMap,
    BmControl,
    BmLabel,
    BmMarker,
    BmNavigation,
    BmlHeatmap,
    BmlMarkerClusterer
  },
  data() {
    return {
      loading: false,
      conheight: { height: "" },
      showExFilter: false,
      customFilter: false,
      radioGroup: [],
      radioChecked: "",
      interval_from: "",
      interval_to: "",
      arrangeItems: [
        { value: "room", label: "户型" },
        { value: "price", label: "价格" },
        { value: "amount", label: "总价" },
        { value: "area", label: "面积" }
      ],
      listQuery: {
        scope: ["西安市", ""],
        stattype: ["sale", "price"],
        property: "普通住宅",
        datetype: "month",
        statdate: "",
        arrange: "",
        intervals: ""
      },
      datePicker: "",
      datetype: [
        { label: "按年", value: "year" },
        { label: "月段", value: "monthrange" },
        { label: "按月", value: "month" },
        { label: "按周", value: "week" },
        { label: "按日", value: "daterange" }
      ],
      property: [],
      room: [],
      scope: [],
      stattype: [
        {
          value: "sale",
          label: "成交情况",
          children: [
            {
              value: "price",
              label: "成交价格"
            },
            {
              value: "amount",
              label: "成交金额"
            },
            {
              value: "area",
              label: "成交面积"
            },
            {
              value: "number",
              label: "成交套数"
            }
          ]
        },
        {
          value: "supply",
          label: "上市情况",
          children: [
            {
              value: "number",
              label: "上市套数"
            },
            {
              value: "area",
              label: "上市面积"
            }
          ]
        },
        {
          value: "stock",
          label: "可售情况",
          children: [
            {
              value: "number",
              label: "可售套数"
            },
            {
              value: "area",
              label: "可售面积"
            }
          ]
        }
      ],
      center: { lng: 0, lat: 0 },
      zoom: 0,
      max: 0,
      data: [],
      markers: [],
      markerVision: false,
      map: null
    };
  },
  mounted() {
    this.getHeight();
    this.fetchProperty();
    this.fetchScope();
    this.fetchRadioGroup();
    this.changeQueryDate();
  },
  methods: {
    getHeight() {
      this.conheight.height = window.innerHeight - 160 + "px";
    },
    fetchProperty() {
      getOptions({ opt_key: "spiderman_frame" }).then(response => {
        const { data } = response;
        this.property = JSON.parse(data).property;
        let roomOrg = JSON.parse(data).arrange.room;
        for (let i = 0; i < roomOrg.length; i++) {
          this.room.push(roomOrg[i]);
        }
      });
    },
    fetchScope() {
      getOptions({ opt_key: "cities" }).then(response => {
        const { data } = response;
        this.scope = JSON.parse(data);
      });
    },
    fetchRadioGroup() {
      getOptions({ opt_key: "filter_template" }).then(response => {
        const { data } = response;
        this.radioGroup = JSON.parse(data);
      });
    },
    setArrange() {
      this.listQuery.arrange = this.radioChecked.split(".")[0];
      this.listQuery.intervals = this.radioChecked.split(".")[1];
      this.fetchData();
    },
    onSubmit() {
      if (this.listQuery.arrange === null || this.listQuery.arrange === "") {
        this.$message.error("过滤项不能为空");
        return;
      }
      if (this.interval_from === null || this.interval_from === "") {
        this.$message.error("起始值不能为空");
        return;
      }
      if (this.interval_to === null || this.interval_to === "") {
        this.$message.error("结束值不能为空");
        return;
      }
      if (isNaN(this.interval_from) || isNaN(this.interval_to)) {
        this.$message.error("起始/结束值必须为数字类型");
        return;
      }
      if (parseInt(this.interval_from) > parseInt(this.interval_to)) {
        this.$message.error("结束值要大于起始值");
        return;
      }
      this.listQuery.intervals = this.interval_from + ":" + this.interval_to;
      this.fetchData();
    },
    changeSelect() {
      this.showExFilter = false;
      this.exFilter();
      this.fetchData();
    },
    changeQueryDate() {
      this.listQuery.arrange = "";
      this.listQuery.intervals = "";
      this.radioChecked = "";
      this.interval_from = "";
      this.interval_to = "";
      this.showExFilter = false;
      switch (this.listQuery.datetype) {
        case "year":
          this.datePicker = new Date(new Date().getFullYear() - 1, 0, 1);
          break;
        case "monthrange":
          this.datePicker = [
            new Date(new Date().getFullYear(), new Date().getMonth() - 3, 1),
            new Date(new Date().getFullYear(), new Date().getMonth() - 1, 1)
          ];
          break;
        case "month":
          this.datePicker = new Date(
            new Date().getFullYear(),
            new Date().getMonth() - 1,
            1
          );
          break;
        case "week":
          this.datePicker = new Date(
            new Date().getFullYear(),
            new Date().getMonth(),
            new Date().getDate() - (new Date().getDay() || 7) - 13
          );
          break;
        case "daterange":
          this.datePicker = [
            new Date(
              new Date().getFullYear(),
              new Date().getMonth() - 1,
              new Date().getDate() - 14
            ),
            new Date(
              new Date().getFullYear(),
              new Date().getMonth(),
              new Date().getDate() - 14
            )
          ];
          break;
        default:
          break;
      }
      this.fetchData();
    },
    exFilter() {
      this.listQuery.arrange = "";
      this.listQuery.intervals = "";
      this.radioChecked = "";
      this.interval_from = "";
      this.interval_to = "";
      this.fetchData();
    },
    convertToDate(date) {
      var y = date.getFullYear();
      var m = date.getMonth() + 1;
      var d = date.getDate();

      m = m < 10 ? "0" + m : m;
      d = d < 10 ? "0" + d : d;

      return y + "-" + m + "-" + d;
    },
    fetchData() {
      if (this.map !== null) {
        this.map.clearOverlays();
      }
      if (
        this.listQuery.datetype === "monthrange" ||
        this.listQuery.datetype === "daterange"
      ) {
        this.listQuery.statdate = [
          this.convertToDate(this.datePicker[0]),
          this.convertToDate(this.datePicker[1])
        ];
      } else {
        this.listQuery.statdate = this.convertToDate(this.datePicker);
      }
      this.loading = true;
      getDataset(this.listQuery).then(response => {
        const { data } = response;
        if (data === "" || data === null) {
          this.data = [];
          this.max = 0;
        } else {
          this.data = data.data;
          this.max = data.max;
        }
        this.loading = false;
      });
    },
    handler({ BMap, map }) {
      this.map = map;
      this.center.lng = 108.953364;
      this.center.lat = 34.275946;
      this.zoom = 12;
    },
    showMarker() {
      if (this.markerVision) {
        this.markerVision = false;
        this.markers = [];
      } else {
        this.markerVision = true;
        this.markers = this.data;
      }
    }
  }
};
</script>

<style>
.bm-view {
  width: 100%;
  height: 500px;
}
.bm-button {
  background-color: #3f51b5;
  color: rgba(255, 255, 255, 0.87);
  outline: none;
  min-width: 88px;
  min-height: 36px;
  margin: 6px 8px;
  padding: 0 16px;
  display: inline-block;
  position: relative;
  overflow: hidden;
  user-select: none;
  cursor: pointer;
  border: 0;
  border-radius: 2px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-family: inherit;
  font-size: 14px;
  font-style: inherit;
  font-variant: inherit;
  font-weight: 500;
  letter-spacing: inherit;
  line-height: 36px;
  text-align: center;
  text-transform: uppercase;
  text-decoration: none;
  vertical-align: top;
  white-space: nowrap;
}
</style>
