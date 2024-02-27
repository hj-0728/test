import { NextPage } from 'next';
import { Button, LoadingOverlay, Switch } from '@mantine/core';
import React, { createContext, useContext, useEffect, useState } from 'react';
import { IconEdit, IconPlus } from '@tabler/icons-react';
import Index from '@/components/BasicTable';
import { Column, TableData } from '@/components/BasicTable/BasicTable.model';
import { apiChangeIsActivated, apiGetRolePageList } from '@/api/RoleApi';
import { PageFilterParams } from '@/model/Basic.model';
import { showSuccessNotification } from '@/components/BasicNotifications';
import openConfirmModal from '@/components/BasicConfirmModal';
import AdminLayout from '@/layouts/adminLayout';
import PageWrapperCard from '@/components/Page/WrapperCard';
import EditForm from './_components/EditForm';

const ReloadContext = createContext(null);

function AddComponent() {
    const loadRoleList = useContext(ReloadContext);
    const [open, setOpen] = useState(false);
    const onCloseRoleAddForm = () => {
        setOpen(false);
        // @ts-ignore
      loadRoleList();
    };
    return (
        <>
            <EditForm open={open} onClose={onCloseRoleAddForm} />
            <Button
              color="teal"
              leftSection={<IconPlus />}
              onClick={() => {
                    setOpen(true);
                }}
            >
                添加
            </Button>
        </>
    );
}

// @ts-ignore
function OperationComponent({ rowData }) {
    const loadRoleList = useContext(ReloadContext);
    const [open, setOpen] = useState(false);
    const [roleId, setRoleId] = useState(null);
    const onCloseRoleEditForm = () => {
        setOpen(false);
        // @ts-ignore
      loadRoleList();
    };
    const onClickEditBtn = () => {
        setRoleId(rowData.id);
        setOpen(true);
    };
    return (
        <>
            <EditForm open={open} roleId={roleId} onClose={onCloseRoleEditForm} />
            <Button color="cyan" leftSection={<IconEdit />} onClick={onClickEditBtn}>
                编辑
            </Button>
        </>
    );
}

// @ts-ignore
function SwitchComponent({ rowData }) {
    const loadRoleList = useContext(ReloadContext);
    const onChange = () => {
        openConfirmModal({
            message: '确定要禁用吗？',
            onConfirm: () => {
                const { id, isActivated, version } = rowData;
                apiChangeIsActivated({ id, version, isActivated: !isActivated }).then((res) => {
                    if (res.code === 200) {
                        showSuccessNotification('修改成功');
                        // @ts-ignore
                      loadRoleList();
                    } else {
                        showSuccessNotification(res.error!.message);
                    }
                });
            },
        });
    };
    return (
        <>
            <Switch
              onLabel="已启用"
              offLabel="已禁用"
              checked={rowData.isActivated}
              onChange={onChange}
            />
        </>
    );
}

const useTableCusComponent = (dataIndex: string, rowData: any) => {
    // 在这里进行你的条件判断和其他操作
    if (dataIndex === 'operation') {
        return <OperationComponent rowData={rowData} />;
    }
    if (dataIndex === 'isActivated') {
        return <SwitchComponent rowData={rowData} />;
    }
    return null;
};

const columns: Column[] = [
    { title: '名称', dataIndex: 'name' },
    { title: '编码', dataIndex: 'code' },
    { title: '状态', dataIndex: 'isActivated' },
    { title: '描述', dataIndex: 'comments' },
    { title: '操作', dataIndex: 'operation' },
];

const initEmptyTableData: TableData = {
    totalCount: 0,
    pageIndex: 0,
    pageSize: 0,
    data: [],
};

function RoleTable() {
    const [tableData, setTableData] = useState<TableData>(initEmptyTableData);
    const [pageIndex, setPageIndex] = useState<number>(0);
    const [searchText, setSearchText] = useState<string>('');
    const [loading, setLoading] = useState(true);
    const [draw, setDraw] = useState(1);

    const onLoadTableData = () => {
        setDraw(draw + 1);
        const params: PageFilterParams = {
            pageIndex,
            pageSize: 20,
            draw,
            searchText,
        };
        apiGetRolePageList(params).then((res) => {
            if (params.draw === draw) {
                const data: TableData = {
                    totalCount: res.data.filterCount,
                    pageIndex: res.data.pageIndex,
                    pageSize: res.data.pageSize,
                    data: res.data.data,
                };
                setTableData(data);
            }
        }).finally(() => {
            setLoading(false);
        });
    };

    const loadRoleList = () => {
        setLoading(true);
        onLoadTableData();
    };

    useEffect(() => {
        loadRoleList();
    }, [pageIndex, searchText]);

    const onPageChange = (value: number) => {
        setPageIndex(value);
    };

    const onSearch = (value: string) => {
        setSearchText(value);
        setPageIndex(0);
    };

    return (
        <ReloadContext.Provider value={loadRoleList}>
            <>
                <LoadingOverlay visible={loading} zIndex={1000} />
                <Index
                  table={tableData}
                  columns={columns}
                  toolbar={<AddComponent />}
                  onPageChange={onPageChange}
                  onSearch={onSearch}
                  cusComponent={useTableCusComponent}
                />
            </>
        </ReloadContext.Provider>

    );
}

const RoleList: NextPage = () => (
    <>
        <AdminLayout>
            <PageWrapperCard>
                <RoleTable />
            </PageWrapperCard>
        </AdminLayout>
    </>
);
export default RoleList;
