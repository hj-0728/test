import { NextPage } from 'next';
import { createContext, useContext, useEffect, useState } from 'react';
import PageWrapperCard from '@/components/Page/WrapperCard';
import {
  IconBrandCodesandbox,
  IconPlus,
  IconMoodEmpty,
  IconTerminal2,
  IconMoodCheck,
  IconEdit,
} from '@tabler/icons-react';
import { Button, Grid, Title, List, ThemeIcon, rem, Badge } from '@mantine/core';
import { apiGetSceneList } from '@/api/SceneApi';
import { Scene } from '@/model/Scene.model';
import Empty from '@/components/Empty';
import styles from './List.module.css';
import EditForm from './_components/EditForm';
import AdminLayout from '../../layouts/adminLayout';

const ReloadContext = createContext<(() => void) | null>(null);

function OperationBar(): JSX.Element {
  const loadSceneList = useContext(ReloadContext);
  const [open, setOpen] = useState(false);
  const onCloseRoleAddForm = () => {
    setOpen(false);
    if (loadSceneList) {
      loadSceneList();
    }
  };
  return (
    <>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <IconBrandCodesandbox color="var(--mantine-color-blue-filled)" />
          <Title order={4} style={{ marginLeft: '5px' }}>
            我的场景
          </Title>
        </div>
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
      </div>
    </>
  );
}

function SceneList(): JSX.Element {
  const [sceneList, setSceneList] = useState<Scene[] | null>(null);
  const [open, setOpen] = useState(false);
  const [sceneId, setSceneId] = useState<string | undefined>('');
  useEffect(() => {
    loadSceneList();
  }, []);

  const loadSceneList = () => {
    apiGetSceneList().then((res) => {
      if (res.code === 200) {
        setSceneList(res.data as Scene[]);
      } else {
        console.log(res.message);
        setSceneList([]);
      }
    });
  };

  const onCloseRoleEditForm = () => {
    setOpen(false);
    // @ts-ignore
    loadSceneList();
  };
  const onClickEditBtn = (sceneId: string | undefined) => {
    setSceneId(sceneId);
    setOpen(true);
  };

  const sceneCardList = sceneList !== null && sceneList.map((scene) => (
      <Grid.Col span={{ lg: 6, xl: 3 }} key={scene.id}>
        <div className={styles.sceneCard}>
          <div style={{ display: 'flex' }}>
            <span
              style={{
                fontWeight: '600',
                fontSize: '18px',
                textOverflow: 'ellipsis',
                overflow: 'hidden',
                whiteSpace: 'nowrap',
                width: '200px',
                display: 'inline-block',
              }}
            >
              {scene.name}
            </span>
          </div>
          <List
            spacing="xs"
            size="sm"
            style={{ marginTop: '15px', itemWrapper: { alignItems: 'none' } }}
          >
            <List.Item
              icon={
                <ThemeIcon color="var(--mantine-color-blue-filled)" size={20} radius="xl">
                  <IconMoodCheck style={{ width: rem(12), height: rem(12) }} />
                </ThemeIcon>
              }
            >
              表扬观测点：
              {scene.observationPointStatistics.find((obsPoint) => obsPoint.category === 'COMMEND')
                ?.num || 0}
            </List.Item>
            <List.Item
              icon={
                <ThemeIcon color="var(--mantine-color-blue-filled)" size={20} radius="xl">
                  <IconMoodEmpty style={{ width: rem(12), height: rem(12) }} />
                </ThemeIcon>
              }
            >
              待改进观测点：
              {scene.observationPointStatistics.find(
                (obsPoint) => obsPoint.category === 'TO_BE_IMPROVED'
              )?.num || 0}
            </List.Item>
            <List.Item
              styles={{
                itemLabel: { height: '70px' },
                itemWrapper: { alignItems: 'flex-start' },
              }}
              icon={
                <ThemeIcon color="var(--mantine-color-blue-filled)" size={20} radius="xl">
                  <IconTerminal2 style={{ width: rem(12), height: rem(12) }} />
                </ThemeIcon>
              }
            >
              适用终端：
              {scene.terminalCategoryNameList.map((terminalCategoryName) => (
                  <Badge variant="outline" key={terminalCategoryName} style={{ margin: '0 3px 3px 0' }}>
                    {terminalCategoryName}
                  </Badge>
                ))}
            </List.Item>
          </List>
          <div className={styles.overlay}>
            <Button
              variant="outline"
              leftSection={<IconEdit size={14} />}
              onClick={() => onClickEditBtn(scene.id)}
            >
              编辑
            </Button>
          </div>
        </div>
      </Grid.Col>
    ));

  return (
    <ReloadContext.Provider value={loadSceneList}>
      <OperationBar />
      <Grid gutter="md" style={{ height: 'calc(100vh - 190px)', padding: '0 10px', overflowY: 'auto' }}>
        <EditForm open={open} sceneId={sceneId} onClose={onCloseRoleEditForm} />
        {sceneCardList && sceneCardList.length > 0 ? sceneCardList : (sceneList !== null && <Empty />)}
      </Grid>
    </ReloadContext.Provider>
  );
}

const ScenePage: NextPage = () => (
    <AdminLayout>
      <PageWrapperCard>
        <SceneList />
      </PageWrapperCard>
    </AdminLayout>
  );

export default ScenePage;
