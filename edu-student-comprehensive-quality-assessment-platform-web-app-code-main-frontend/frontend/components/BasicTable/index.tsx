import React, { ReactElement, useEffect, useState } from 'react';
import { Center, Grid, Input, Pagination, Table } from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';
import { Column, TableData } from './BasicTable.model';

import classes from './BasicTable.module.css';

interface TableProps {
  table?: TableData
  columns: Column[];
  cusComponent?: (dataIndex: string, rowData: any) => React.ReactNode;
  toolbar?: React.ReactNode;
  onPageChange?: (page: number) => void;
  onSearch?: (searchText: string) => void;
}

function empty(colSpan: number) {
  return (
    <tr>
      <td colSpan={colSpan}>
        <Center h={50} w="80vw">
          <div>暂无数据</div>
        </Center>
      </td>
    </tr>
  );
}

const BasicTable: React.FC<TableProps> = ({
                                       table,
                                       columns,
                                       cusComponent,
                                       toolbar,
                                       onPageChange,
                                       onSearch,
                                     }): ReactElement<any, any> | null => {
  if (!table || !table.data) {
    return null;
  }

  const [page, setPage] = useState<number>(0);

  useEffect(() => {
    setPage(Math.ceil(table.totalCount / table.pageSize));
  }, [table]);

  // 处理页码变化
  const handlePageChange = (curPage: number) => {
    if (onPageChange) {
      onPageChange(curPage - 1);
    }
  };

  const handleSearch = (value: string) => {
    if (onSearch) {
      onSearch(value);
    }
  };

  const rows = table.data.map((element) => {
    const tds = columns.map((col) => {
      let cusComp;
      if (cusComponent) {
        cusComp = cusComponent(col.dataIndex, element);
      }
      return cusComp ? (
        <Table.Td key={col.dataIndex}>{cusComp}</Table.Td>
      ) : (
        <Table.Td key={col.dataIndex}>{element[col.dataIndex]}</Table.Td>
      );
    });
    return (
      <Table.Tr key={element.name}>
        {tds}
      </Table.Tr>
    );
  });

  return (
    <>
      <Grid style={{ marginBottom: '10px' }}>
        <Grid.Col span={3}>
          <Input
            leftSection={<IconSearch />}
            placeholder="输入关键字搜索"
            className={classes.searchInput}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleSearch(e.target.value)}
            // onKeyDown={(event) => {
            //       if (event.key === 'Enter') {
            //           handleSearch(event.target.value);
            //       }
            //   }}
          />
        </Grid.Col>
        <Grid.Col span={9} className={classes.toolbar}>
          {toolbar}
        </Grid.Col>
      </Grid>

      <Table withTableBorder highlightOnHover withColumnBorders striped stickyHeader>
        <Table.Thead>
          <Table.Tr>{
            columns.map((col) => (
              <Table.Th key={col.dataIndex}>{col.title}</Table.Th>
            ))
          }
          </Table.Tr>
        </Table.Thead>
          <Table.Tbody>
            {rows && rows.length > 0 ? (
              rows
            ) : (
              empty(columns.length)
            )}
          </Table.Tbody>
      </Table>

      {
        page > 0 && (
          <div>
            <Pagination
              total={page}
              value={table.pageIndex + 1}
              onChange={handlePageChange}
              className={classes.pagination}
            />
          </div>
        )
      }

    </>
  );
};

export default BasicTable;
