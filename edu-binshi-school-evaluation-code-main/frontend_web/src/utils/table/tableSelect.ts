let that: any = null;
export const initThat = (_that) => {
  that = _that;
};
export const exitTableSelect = () => {
  that.selectedRowKeys = [];
  that.selectedRows = [];
  that.currentSelectIdList = [];
};

export const changPage = () => {
  that.currentSelectIdList = [];
  for (const data of that.tableData) {
    const idx = that.selectedRowKeys.indexOf(data.id);
    if (idx > -1) {
      that.currentSelectIdList.push(data.id);
    }
  }
};

export const onCheckboxClick = (record) => {
  if (record !== null) {
    const idx = that.currentSelectIdList.indexOf(record.id);
    if (idx > -1) {
      that.currentSelectIdList.splice(idx, 1);
    } else {
      that.currentSelectIdList.push(record.id);
    }
    const idx2 = that.selectedRowKeys.indexOf(record.id);
    if (idx2 > -1) {
      that.selectedRowKeys.splice(idx2, 1);
      that.selectedRows.splice(idx2, 1);
    } else {
      that.selectedRowKeys.push(record.id);
      that.selectedRows.push(record);
    }
  } else {
    if (
      that.currentSelectIdList.length < that.tableData.length ||
      that.currentSelectIdList.length === 0
    ) {
      that.currentSelectIdList = [];
      for (const data of that.tableData) {
        const idx = that.currentSelectIdList.indexOf(data.id);
        if (idx < 0) {
          that.currentSelectIdList.push(data.id);
        }
        const idx2 = that.selectedRowKeys.indexOf(data.id);
        if (idx2 < 0) {
          that.selectedRowKeys.push(data.id);
          that.selectedRows.push(data);
        }
      }
    } else {
      that.currentSelectIdList = [];
      for (const data of that.tableData) {
        const idx = that.selectedRowKeys.indexOf(data.id);
        if (idx > -1) {
          that.selectedRowKeys.splice(idx, 1);
          that.selectedRows.splice(idx, 1);
        }
      }
    }
  }
};
