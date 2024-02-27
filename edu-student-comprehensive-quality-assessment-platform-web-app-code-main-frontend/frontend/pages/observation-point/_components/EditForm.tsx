import {
    Avatar,
    LoadingOverlay,
    SimpleGrid,
    Indicator,
    Button,
    Group,
    Modal,
    Grid,
    Image,
    Input,
    Badge,
    Chip,
    UnstyledButton,
    ScrollArea,
} from '@mantine/core';
import React, { useEffect, useState } from 'react';
import {
    apiDeleteObservationPoint,
    apiGetObservationPointInfo,
    apiGetObservationPointSystemIcon,
    apiSaveObservationPoint,
} from '@/api/ObservationPointApi';
import {
    ObservationPointSystemIcon,
    ObservationPoint, SaveObservationPoint,
} from '@/model/ObservationPoint.model';
import { apiGetSceneList } from '@/api/SceneApi';
import { Scene } from '@/model/Scene.model';
import { useForm } from '@mantine/form';
import openConfirmModal from '@/components/BasicConfirmModal';
import { showErrorNotification, showSuccessNotification } from '@/components/BasicNotifications';
import { IconCheck, IconTrash, IconX } from '@tabler/icons-react';
import classes from './EditForm.module.css';

const ObservationPointIcon: React.FC<{ category: string, onSelectIcon: any, selectedIconId: string | null }> = (
    { category, onSelectIcon, selectedIconId }
) => {
    const [loading, setLoading] = useState(true);
    const [observationPointIcon, setObservationPointIcon] = useState<ObservationPointSystemIcon[] | null>(null);
    const [selectedIcon, setSelectedIcon] = useState<string | null>(null);

    const setSelectIcon = (data: ObservationPointSystemIcon) => {
        // 处理子组件传递的数据
        onSelectIcon(data);
        setSelectedIcon(data.id);
    };
    const observationPointSystemIconList = () => {
        apiGetObservationPointSystemIcon(category).then((res) => {
            if (res.code === 200) {
                setObservationPointIcon(res.data);
                if (!selectedIconId || selectedIconId === '') {
                    setSelectIcon(res.data[0]);
                }
            }
        }).finally(() => {
            setLoading(false);
        });
    };
    useEffect(() => {
        if (selectedIconId && selectedIconId !== '') {
            setSelectedIcon(selectedIconId);
        }
        observationPointSystemIconList();
    }, []); // 空数组表示只在组件挂载时运行

    return (
        <>
            <div style={{ textAlign: 'center', marginBottom: '10px' }}>
                <Badge
                  size="xl"
                  variant="gradient"
                  gradient={{ from: 'blue', to: 'cyan', deg: 90 }}
                >
                  系统图标
                </Badge>
            </div>
            <ScrollArea className={classes.selectScroll}>
                <SimpleGrid className={classes.selectIcon} cols={8} spacing="sm" verticalSpacing="md">
                    {observationPointIcon ? (
                        observationPointIcon.map((item: ObservationPointSystemIcon) => (
                          <Indicator
                            disabled={item.id !== selectedIcon}
                            key={item.id}
                            inline
                            label="√"
                            size={25}
                            offset={8}
                            withBorder
                          >
                            <Avatar
                              className={item.id !== selectedIcon ? classes.addSelectPointIcon : classes.addSelectedPointIcon}
                              src={item.fileUrl}
                              radius="xl"
                              onClick={() => { setSelectIcon(item); }}
                            />
                          </Indicator>
                    ))
                  ) : (
                      <LoadingOverlay visible={loading} zIndex={1000} />
                  )}
                </SimpleGrid>
            </ScrollArea>
        </>

    );
};

const ObservationPointScene: React.FC<{ onSetSelectScene: any, selectedSceneIds: string[] | null }> = (
    { onSetSelectScene, selectedSceneIds }
) => {
    const [loading, setLoading] = useState(true);
    const [observationPointScene, setObservationPointScene] = useState<Scene[] | null>(null);
    const [selectedScene, setSelectedScene] = useState<string[]>([]);
    const observationPointSceneList = () => {
        apiGetSceneList().then((res) => {
            if (res.code === 200) {
                setObservationPointScene(res.data);
            }
        }).finally(() => {
            setLoading(false);
        });
    };
    useEffect(() => {
        observationPointSceneList();
        setSelectedScene(selectedSceneIds || []);
    }, []); // 空数组表示只在组件挂载时运行

    const setSelectedSceneData = (data: string[]) => {
        // 处理子组件传递的数据
        setSelectedScene(data);
        onSetSelectScene(data);
    };

    return (
        <>
            <div style={{ textAlign: 'center', marginBottom: '10px' }}>
                <Badge
                  size="xl"
                  variant="gradient"
                  gradient={{ from: 'blue', to: 'cyan', deg: 90 }}
                >
                  场景
                </Badge>
            </div>
            <ScrollArea className={classes.selectScroll}>
                <div style={{ marginTop: '30px' }}>
                    <Chip.Group multiple value={selectedScene} onChange={setSelectedSceneData}>
                        <Group justify="center">
                        {
                            observationPointScene ? (observationPointScene.map((item: Scene) => (
                            <Chip
                              icon={false}
                              key={item.id}
                              value={item.id}
                            >{item.name}
                            </Chip>
                        ))
                          ) : (
                              <LoadingOverlay visible={loading} zIndex={1000} />
                          )
                        }
                        </Group>
                    </Chip.Group>
                </div>
            </ScrollArea>
        </>

    );
};

const SaveObservationPointModel: React.FC<{ category: string, isOpen: boolean, onClose: any, observationPointId: string | null }> = (
    { category, isOpen, onClose, observationPointId }
) => {
    // const [opened, { open, close }] = useDisclosure(isOpen);
    const [scoreList] = useState<string[]>(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']);
    const [score, setScore] = useState<number>(1);
    const [operateCategory, setOperateCategory] = useState<string>('icon');
    const [title, setTitle] = useState<string>('添加表扬观测点');
    const [selectIcon, setSelectIcon] = useState<ObservationPointSystemIcon | null>(null);
    const [selectedScene, setSelectedScene] = useState<string[]>([]);
    const [observationPointInfo, setObservationPointInfo] = useState<ObservationPoint | null>(null);

    const form = useForm<SaveObservationPoint>({
        initialValues: {
            id: null,
            version: 1,
            name: '',
            category: '',
            fileId: '',
            pointScore: 1,
            sceneIdList: [],
        },

        validate: {
            name: (value) => (value.trim() ? null : '名称不能为空'),
        },
    });

    const setSelectIconData = (data: ObservationPointSystemIcon) => {
        // 处理子组件传递的数据
        setSelectIcon(data);
        form.values.fileId = data.id;
    };

    const getObservationPointInfo = () => {
        if (observationPointId === null) {
            return;
        }
        apiGetObservationPointInfo(observationPointId).then((res) => {
            if (res.code === 200) {
                setSelectIconData({
                    id: res.data.fileId,
                    fileUrl: res.data.fileUrl,
                });
                const data = res.data as ObservationPoint;
                setObservationPointInfo(data);
                setScore(data.pointScore);
                setSelectedScene(data.sceneIdList || []);
                form.setValues({
                    id: data.id,
                    version: data.version,
                    name: data.name,
                    category: data.category,
                    fileId: data.fileId,
                    pointScore: data.pointScore,
                    sceneIdList: data.sceneIdList || [],
                });
            }
        });
    };

    const initData = () => {
        form.reset();
        setOperateCategory('icon');
        setObservationPointInfo(null);
        setScore(1);
        setSelectIcon(null);
        setSelectedScene([]);
    };

    const setModelTitle = () => {
        const categoryName = category === 'COMMEND' ? '表扬' : '待改进';
        if (observationPointId) {
            setTitle(`编辑${categoryName}观测点`);
        } else {
            setTitle(`添加${categoryName}观测点`);
        }
    };

    useEffect(() => {
        initData();
        setModelTitle();
        if (isOpen) {
            getObservationPointInfo();
        }
    }, [isOpen]); // 空数组表示只在组件挂载时运行

    const setScoreData = (data: string) => {
        setScore(Number(data));
        form.values.pointScore = Number(data);
    };

    const setSelectSceneData = (data: string[]) => {
        setSelectedScene(data);
    };

    const onCloseModal = () => {
        initData();
        onClose();
    };

    const saveObservationPointInfo = () => {
        form.values.category = category;
        form.values.sceneIdList = selectedScene;
        apiSaveObservationPoint(form.values).then((res) => {
            if (res.code === 200) {
                showSuccessNotification('保存成功');
                onCloseModal();
            } else {
                showErrorNotification(res.error!.message);
            }
        });
    };

    const deleteObservationPointInfo = () => {
        if (!observationPointId) {
            return;
        }
        apiDeleteObservationPoint({ id: observationPointId }).then((res) => {
            if (res.code === 200) {
                showSuccessNotification('删除成功');
                onCloseModal();
            } else {
                showErrorNotification(res.error!.message);
            }
        });
    };

    const onSaveObservationPoint = () => {
        openConfirmModal({
          message: '确定要提交吗？',
          onConfirm: () => saveObservationPointInfo(),
        });
    };

    const onDeleteObservationPoint = () => {
        openConfirmModal({
          message: '确定要删除吗？',
          onConfirm: () => deleteObservationPointInfo(),
        });
    };

    return (
        <>
            <Modal
              size="75%"
              opened={isOpen}
              onClose={onCloseModal}
              title={title}
              centered
              zIndex={210}
            >
                { !observationPointId || observationPointInfo ? (
                    <form onSubmit={form.onSubmit(() => onSaveObservationPoint())}>
                        <Grid align="stretch">
                            <Grid.Col span={4} style={{ textAlign: 'center' }} className={classes.addPointsInfo}>
                                <div className={classes.addPointIconDiv}>
                                    <Image
                                      onClick={() => {
                                            setOperateCategory('icon');
                                        }}
                                      className={classes.addPointIcon}
                                      src={selectIcon?.fileUrl}
                                    />
                                </div>
                                <Group className={classes.addPointName}>
                                    <div>
                                        <span style={{ color: 'red', padding: '0 3px' }}>*</span>名称：
                                    </div>
                                    <Input placeholder="不超过十个字" {...form.getInputProps('name')} />
                                </Group>
                                <Group className={classes.addPointName}>
                                    <div>
                                        <span style={{ color: 'red', padding: '0 3px' }}>*</span>分值：
                                    </div>
                                    <div style={{ width: '218px' }}>
                                        <Chip.Group
                                          multiple={false}
                                          value={score.toString()}
                                          onChange={setScoreData}
                                        >
                                            <Group justify="center">
                                                {scoreList.map((item: string) => (
                                                    <Chip
                                                      icon={false}
                                                      key={item}
                                                      value={item}
                                                    >{item}
                                                    </Chip>
                                                ))}
                                            </Group>
                                        </Chip.Group>
                                    </div>
                                </Group>
                                <Group className={classes.addPointName}>
                                    <div>
                                        <span style={{ padding: '0 3px', visibility: 'hidden' }}>*</span>场景：
                                    </div>
                                    <UnstyledButton
                                      style={{ color: '#228be6', padding: '0 3px' }}
                                      onClick={() => {
                                            setOperateCategory('scene');
                                        }}
                                    >点击添加场景
                                    </UnstyledButton>
                                </Group>
                            </Grid.Col>
                            <Grid.Col span={8}>
                                <div style={{ minHeight: '430px' }}>
                                    {operateCategory === 'icon' ? (
                                        ((observationPointId && form.values.fileId) || !observationPointId) &&
                                        <ObservationPointIcon
                                          onSelectIcon={setSelectIconData}
                                          category={category}
                                          selectedIconId={selectIcon?.id || null}
                                        />
                                    ) : (
                                        <ObservationPointScene
                                          onSetSelectScene={setSelectSceneData}
                                          selectedSceneIds={selectedScene}
                                        />
                                    )}
                                </div>
                            </Grid.Col>
                        </Grid>
                        <div className={classes.modalBottom}>
                            { observationPointId && (
                                <Button
                                  style={{ float: 'left', margin: '10px 30px 0 0' }}
                                  variant="filled"
                                  color="red"
                                  onClick={onDeleteObservationPoint}
                                  leftSection={<IconTrash />}
                                >
                                    删除此项
                                </Button>
                            )}
                            <Button
                              style={{ float: 'right', margin: '10px 0 0 0' }}
                              variant="filled"
                              type="submit"
                              leftSection={<IconCheck />}
                            >
                                保存
                            </Button>
                            <Button
                              style={{ float: 'right', margin: '10px 10px 0 0' }}
                              onClick={onCloseModal}
                              variant="default"
                              leftSection={<IconX size={14} />}
                            >
                                取消
                            </Button>
                        </div>
                    </form>
                ) : (<div style={{ minHeight: '490px' }}><LoadingOverlay zIndex={1000} /></div>) }

            </Modal>
        </>
    );
};

export default SaveObservationPointModel;
