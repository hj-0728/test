import { NextPage } from 'next';
import {
    Blockquote,
    Card,
    Avatar,
    LoadingOverlay,
    SimpleGrid,
    Text,
    Indicator,
    Button,
    Group,
    Title,
    ScrollArea,
} from '@mantine/core';
import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import {
    apiGetObservationPointList,
} from '@/api/ObservationPointApi';
import {
    ObservationPointList,
    ObservationPoint,
} from '@/model/ObservationPoint.model';
import { IconBrandCodesandbox, IconEdit, IconPlus } from '@tabler/icons-react';
import AdminLayout from '../../layouts/adminLayout';
import classes from './ObservationPoint.module.css';
import SaveObservationPointModel from './_components/EditForm';

// 定义上下文类型
interface MyContextType {
  isUpdateData: boolean;
  setIsUpdateData: React.Dispatch<React.SetStateAction<boolean>>;
}

// 创建上下文
const MyContext = createContext<MyContextType | undefined>(undefined);

// 提供一个包裹组件，用于在整个应用中共享上下文
export const MyContextProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isUpdateData, setIsUpdateData] = useState<boolean>(true);

  return (
    <MyContext.Provider value={{ isUpdateData, setIsUpdateData }}>
      {children}
    </MyContext.Provider>
  );
};

// 自定义 Hook，用于在组件中获取上下文值
export const useMyContext = (): MyContextType => {
  const context = useContext(MyContext);
  if (!context) {
    throw new Error('useMyContext must be used within a MyContextProvider');
  }
  return context;
};

const ObservationPoint: React.FC<
    { dataList: ObservationPoint[], name: string, category: string }
> = ({ dataList, name, category }) => {
    const [open, setOpen] = useState(false);
    const { setIsUpdateData } = useMyContext();
    const [observationPointId, setObservationPointId] = useState<string | null>(null);

    const onCloseAddForm = () => {
        setOpen(false);
        setIsUpdateData(true);
    };

    const onEditObservationPoint = (id: string | null) => {
        setOpen(true);
        setObservationPointId(id);
    };
    return (
        <>
            <Group>
                <Blockquote color="blue" style={{ width: 100, padding: 10 }}>
                    {name}
                </Blockquote>
            </Group>
            <SimpleGrid
              cols={{ base: 1, sm: 5, lg: 7, xl: 8 }}
              spacing="sm"
              verticalSpacing="md"
              style={{ padding: 22 }}
            >
                {dataList.map((item: ObservationPoint) => (
                    <Card
                      key={item.id}
                      shadow="sm"
                      padding="lg"
                      radius="md"
                      withBorder
                      className={classes.observationPointCard}
                    >
                        <Card.Section>
                            <div className={classes.pointIcon}>
                                <Indicator
                                  color={item.pointScore > 0 ? 'blue' : 'red'}
                                  inline
                                  label={item.pointScore}
                                  size={25}
                                  offset={8}
                                  withBorder
                                  style={{ width: '100%' }}
                                >
                                    <Avatar
                                      className={classes.pointImg}
                                      src={item.fileUrl}
                                      radius="xl"
                                    />
                                </Indicator>
                            </div>
                            <Text fw={500} className={classes.pointText}>{item.name}</Text>
                            <div className={classes.overlay}>
                                <Button
                                  variant="outline"
                                  leftSection={<IconEdit size={14} />}
                                  onClick={() => onEditObservationPoint(item.id)}
                                >
                                    编辑
                                </Button>
                            </div>
                        </Card.Section>
                    </Card>
                ))}
            </SimpleGrid>
            <SaveObservationPointModel
              category={category}
              isOpen={open}
              onClose={onCloseAddForm}
              observationPointId={observationPointId}
            />
        </>
    );
};

const ObservationPointCategoryList = () => {
    const [loading, setLoading] = useState(true);
    const [observationPointData, setObservationPointData] = useState<ObservationPointList | null>(null);
    const { isUpdateData, setIsUpdateData } = useMyContext();
    const observationPointList = () => {
        apiGetObservationPointList().then((res) => {
            if (res.code === 200) {
                setObservationPointData(res.data);
            }
        }).finally(() => {
            setLoading(false);
        });
    };
    useEffect(() => {
        if (isUpdateData) {
            observationPointList();
            setIsUpdateData(false);
        }
    }, [isUpdateData]); // 空数组表示只在组件挂载时运行

    return (
        <ScrollArea className={classes.showObservationPoint}>
            {observationPointData ? (
                <>
                    <ObservationPoint
                      dataList={observationPointData.commendObsPointList}
                      name="表扬"
                      category="COMMEND"
                    />
                    <ObservationPoint
                      dataList={observationPointData.toBeImprovedObsPointList}
                      name="待改进"
                      category="TO_BE_IMPROVED"
                    />
                </>
            ) : (
                <LoadingOverlay visible={loading} zIndex={1000} />
            )}
        </ScrollArea>
    );
};

function OperationBar(): JSX.Element {
    const { setIsUpdateData } = useMyContext();
    const [open, setOpen] = useState(false);
    const [category, setCategory] = useState<string>('');
    const onCloseAddForm = () => {
        setOpen(false);
        setIsUpdateData(true);
    };
    return (
        <>
            <div
              style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}
            >
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <IconBrandCodesandbox color="var(--mantine-color-blue-filled)" />
                  <Title order={4} style={{ marginLeft: '5px' }}>
                    观测点管理
                  </Title>
                </div>
                <SaveObservationPointModel
                  category={category}
                  isOpen={open}
                  onClose={onCloseAddForm}
                  observationPointId={null}
                />
                <div>
                    <Button
                      style={{ marginRight: '10px' }}
                      color="teal"
                      leftSection={<IconPlus />}
                      onClick={() => {
                        setOpen(true);
                        setCategory('COMMEND');
                      }}
                    >
                        添加表扬观测点
                    </Button>
                    <Button
                      leftSection={<IconPlus />}
                      onClick={() => {
                        setOpen(true);
                        setCategory('TO_BE_IMPROVED');
                      }}
                    >
                        添加待改进观测点
                    </Button>
                </div>
            </div>
        </>
  );
}

const ObservationPointList: NextPage = () => (
    <>
        <AdminLayout>
            <MyContextProvider>
                <Card shadow="sm" padding="lg" radius="md" withBorder>
                    <OperationBar />
                    <ObservationPointCategoryList />
                </Card>
            </MyContextProvider>
        </AdminLayout>
    </>
);
export default ObservationPointList;
