<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.pro_name"
        placeholder="请输入内容"
        style="width: 360px;"
        class="filter-item"
      />
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="searchList">检索</el-button>
      <el-button class="filter-item" type="primary" icon="el-icon-refresh" @click="resetQuery">重置</el-button>
    </div>

    <el-table v-loading="listLoading" :data="list">
      <el-table-column label="名称" :show-overflow-tooltip="true" min-width="150px">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="位置" :show-overflow-tooltip="true" min-width="300px">
        <template slot-scope="{row}">
          <span>
            <i class="el-icon-location" />
            {{ row.address }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="经度" :show-overflow-tooltip="true" min-width="100px">
        <template slot-scope="{row}">
          <span>{{ row.lat }}</span>
        </template>
      </el-table-column>
      <el-table-column label="纬度" :show-overflow-tooltip="true" min-width="100px">
        <template slot-scope="{row}">
          <span>{{ row.lng }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        width="210px"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" icon="el-icon-edit" @click="handleUpdate(row)">编辑</el-button>
          <el-button size="mini" type="danger" icon="el-icon-delete" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div style="padding: 10px 0;">
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="listQuery.page"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="20"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
    </div>

    <el-dialog :title="dialogStatus==='create'?'新增项目':'更新项目'" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="temp.name" :disabled="true" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="temp.address" />
        </el-form-item>
        <el-form-item label="经度" prop="lat">
          <el-input v-model="temp.lat" />
        </el-form-item>
        <el-form-item label="纬度" prop="lng">
          <el-input v-model="temp.lng" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getProjectList, updateProject } from "@/api/projects";

export default {
  data() {
    return {
      list: [],
      total: 0,
      listLoading: "",
      dialogFormVisible: false,
      dialogStatus: "",
      listQuery: {
        pro_name: "",
        _page: 1,
        _limit: 20
      },
      temp: {
        name: "",
        address: "",
        lat: "",
        lng: ""
      },
      rules: {
        name: [
          {
            required: true,
            message: "project name is required",
            trigger: "change"
          }
        ],
        address: [
          {
            required: true,
            message: "project addrss is required",
            trigger: "change"
          }
        ],
        lat: [
          {
            required: true,
            message: "project lat is required",
            trigger: "change"
          }
        ],
        lng: [
          {
            required: true,
            message: "project lng is required",
            trigger: "change"
          }
        ]
      }
    };
  },
  mounted() {
    this.fetchList();
  },
  methods: {
    resetQuery() {
      this.listQuery = {
        pro_name: "",
        _page: 1,
        _limit: 20
      };
    },
    searchList() {
      this.listQuery._page = 1
      this.listQuery._limit = 20
      this.fetchList()
    },
    fetchList() {
      this.listLoading = true;
      getProjectList(this.listQuery).then(response => {
        const { data } = response;
        this.list = data.list;
        this.total = data.total;
        this.listLoading = false;
      });
    },
    handleSizeChange(val) {
      this.listQuery._limit = val;
      this.fetchList();
    },
    handleCurrentChange(val) {
      this.listQuery._page = val;
      this.fetchList();
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row); // copy obj
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          const tempData = Object.assign({}, this.temp);
          updateProject(tempData).then(() => {
            for (const v of this.list) {
              if (v.id === this.temp.id) {
                const index = this.list.indexOf(v);
                this.list.splice(index, 1, this.temp);
                break;
              }
            }
            this.dialogFormVisible = false;
            this.$notify({
              title: "Success",
              message: "更新记录成功",
              type: "success",
              duration: 2000
            });
          });
        }
      });
    },
    handleDelete(row) {
      this.$message("暂不支持删除记录");
    }
  }
};
</script>

<style scoped>
.line {
  text-align: center;
}
</style>

