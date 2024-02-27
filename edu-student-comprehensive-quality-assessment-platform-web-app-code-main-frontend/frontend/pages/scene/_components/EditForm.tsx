import {
  Box,
  Button,
  Group,
  TextInput,
  MultiSelect,
  SegmentedControl,
  Center,
  rem,
  Grid,
  Avatar,
  Indicator,
  Modal,
  ScrollArea,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { IconCheck, IconMoodEmpty, IconMoodCheck, IconTrash, IconX } from '@tabler/icons-react';
import React, {
  ForwardedRef,
  forwardRef,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from 'react';
import { showErrorNotification, showSuccessNotification } from '@/components/BasicNotifications';
import openConfirmModal from '@/components/BasicConfirmModal';
import {
  apiDeleteScene,
  apiGetSceneInfo,
  apiGetTerminalCategoryList,
  apiSaveScene,
} from '@/api/SceneApi';
import { SceneEditModal, TerminalCategory } from '@/model/Scene.model';
import { apiGetObservationPointList } from '@/api/ObservationPointApi';
import styles from './EditForm.module.css';

interface ObservationPointListHandles {
  setObservationPointCategory: (category: string) => void;
  observationPointIdList: string[];
}

function ObservationPointList(props, ref: ForwardedRef<ObservationPointListHandles>): JSX.Element {
  const [observationPointCategory, setObservationPointCategory] = useState('COMMEND');
  const [commendObsPointList] = useState<any[]>(props.commendObsPointList);
  const [toBeImprovedObsPointList] = useState<any[]>(
    props.toBeImprovedObsPointList
  );
  const [observationPointIdList, setObservationPointIdList] = useState<string[]>(
    props.initialObservationPointIdList
  );
  const [commendNum, setCommendNum] = useState(
    commendObsPointList.filter(
      (obsPoint) =>
        obsPoint.category === 'COMMEND' && observationPointIdList.find((id) => id === obsPoint.id)
    ).length
  );
  const [toBeImprovedNum, setToBeImprovedNum] = useState(
    toBeImprovedObsPointList.filter(
      (obsPoint) =>
        obsPoint.category === 'TO_BE_IMPROVED' &&
        observationPointIdList.find((id) => id === obsPoint.id)
    ).length
  );

  useImperativeHandle(ref, () => ({
    setObservationPointCategory,
    observationPointIdList,
  }));

  const selectObservationPoint = (observationPointId: string, observationCategory: string) => {
    if (observationPointIdList.includes(observationPointId)) {
      setObservationPointIdList(observationPointIdList.filter((id) => id !== observationPointId));
      if (observationCategory === 'TO_BE_IMPROVED') {
        setToBeImprovedNum(toBeImprovedNum - 1);
      } else if (observationCategory === 'COMMEND') {
        setCommendNum(commendNum - 1);
      }
    } else {
      setObservationPointIdList([...observationPointIdList, observationPointId]);
      if (observationCategory === 'TO_BE_IMPROVED') {
        setToBeImprovedNum(toBeImprovedNum + 1);
      } else if (observationCategory === 'COMMEND') {
        setCommendNum(commendNum + 1);
      }
    }
  };

  return (
    <>
      <div style={{ fontSize: '14px', margin: '16px 0 0 5px' }}>选择观测点</div>
      <div style={{ textAlign: 'center' }}>
        <SegmentedControl
          style={{ marginTop: '10px' }}
          color="var(--mantine-color-blue-filled)"
          value={observationPointCategory}
          onChange={setObservationPointCategory}
          styles={{
            indicator: {
              height: '80%',
            },
          }}
          data={[
            {
              value: 'COMMEND',
              label: (
                <Center style={{ gap: 10 }}>
                  <IconMoodCheck style={{ width: rem(18), height: rem(18) }} />
                  <span>表扬类型({commendNum})</span>
                </Center>
              ),
            },
            {
              value: 'TO_BE_IMPROVED',
              label: (
                <Center style={{ gap: 10 }}>
                  <IconMoodEmpty style={{ width: rem(18), height: rem(18) }} />
                  <span>待改进类型({toBeImprovedNum})</span>
                </Center>
              ),
            },
          ]}
        />
      </div>
      <ScrollArea className={styles.showObservationPointScroll}>
        {observationPointCategory === 'COMMEND' && (
          <Grid
            style={{
              marginTop: '10px',
            }}
            styles={{
              inner: { width: '100%', margin: '0 auto' },
            }}
          >
            {commendObsPointList.map((observationPoint) => (
                <Grid.Col
                  span={2}
                  key={observationPoint.id}
                  onClick={() => {
                    selectObservationPoint(observationPoint.id, observationPoint.category);
                  }}
                >
                  <div
                    className={`${styles.obsPointItem} ${
                      observationPointIdList.includes(observationPoint.id) ? styles.active : ''
                    }`}
                  >
                    <Indicator
                      inline
                      size={20}
                      offset={7}
                      label={`${observationPoint.pointScore}`}
                      withBorder
                    >
                      <Avatar src={observationPoint.fileUrl} radius={60} size={60} />
                    </Indicator>

                    {observationPoint.name}
                  </div>
                </Grid.Col>
              ))}
          </Grid>
        )}
        {observationPointCategory === 'TO_BE_IMPROVED' && (
          <Grid
            style={{
              marginTop: '10px',
            }}
            styles={{
              inner: { width: '100%', margin: '0 auto' },
            }}
          >
            {toBeImprovedObsPointList.map((observationPoint) => (
                <Grid.Col
                  span={2}
                  key={observationPoint.id}
                  onClick={() => {
                    selectObservationPoint(observationPoint.id, observationPoint.category);
                  }}
                >
                  <div
                    className={`${styles.obsPointItem} ${
                      observationPointIdList.includes(observationPoint.id) ? styles.active : ''
                    }`}
                  >
                    <Indicator
                      inline
                      size={20}
                      offset={7}
                      label={`${observationPoint.pointScore}`}
                      color="red"
                      withBorder
                    >
                      <Avatar src={observationPoint.fileUrl} radius={60} size={60} />
                    </Indicator>

                    {observationPoint.name}
                  </div>
                </Grid.Col>
              ))}
          </Grid>
        )}
      </ScrollArea>
    </>
  );
}

const ForwardedObservationPointList = forwardRef(ObservationPointList);

interface SceneEditFormProps {
  open: boolean;
  onClose: () => void;
  sceneId?: string | undefined;
}

const EditForm = ({ open, sceneId, onClose }: SceneEditFormProps) => {
  const form = useForm<SceneEditModal>({
    initialValues: {
      id: '',
      name: '',
      code: '',
      version: 1,
      terminalCategoryList: [],
      observationPointIdList: [],
    },

    validate: {
      name: (value) => (value?.trim() ? null : '场景名称不能为空'),
      terminalCategoryList: (value) => (value && value.length > 0 ? null : '适用终端不能为空'),
    },
  });

  const onLoadSceneInfo = () => {
    apiGetSceneInfo(sceneId).then((res) => {
      if (res.code === 200) {
        const { id, version, name, code, terminalCategoryList, observationPointIdList } =
          res.data as SceneEditModal;
        form.setValues({ id, version, name, code, terminalCategoryList, observationPointIdList });
      } else {
        showErrorNotification(res.error!.message);
      }
    });
  };

  const [terminalCategoryList, setTerminalCategoryList] = useState<TerminalCategory[]>([]);
  const onloadTerminalCategoryList = () => {
    apiGetTerminalCategoryList().then((res) => {
      if (res.code === 200) {
        setTerminalCategoryList(res.data);
      } else {
        showErrorNotification(res.error!.message);
      }
    });
  };

  const [commendObsPointList, setCommendObsPointList] = useState<any[]>([]);
  const [toBeImprovedObsPointList, setToBeImprovedObsPointList] = useState<any[]>([]);
  const onLoadObservationPointList = () => {
    apiGetObservationPointList().then((res) => {
      if (res.code === 200) {
        const { commendObsPointList, toBeImprovedObsPointList } = res.data as {
          commendObsPointList: any[];
          toBeImprovedObsPointList: any[];
        };
        setCommendObsPointList(commendObsPointList);
        setToBeImprovedObsPointList(toBeImprovedObsPointList);
      } else {
        showErrorNotification(res.error!.message);
      }
    });
  };

  useEffect(() => {
    if (open && sceneId) {
      onLoadSceneInfo();
    }
    onloadTerminalCategoryList();
    onLoadObservationPointList();
  }, [open]);

  const observationPointListRef = useRef<ObservationPointListHandles | null>(null);

  const onCloseModal = () => {
    form.reset();
    observationPointListRef.current?.setObservationPointCategory('COMMEND');
    onClose();
  };

  const handleAccept = () => {
    form.values.observationPointIdList = observationPointListRef.current?.observationPointIdList;

    const scene = form.values;
    apiSaveScene(scene).then((res) => {
      if (res.code === 200) {
        showSuccessNotification('保存成功');
        onCloseModal();
      } else {
        showErrorNotification(res.error!.message);
      }
    });
  };

  const onSaveScene = () => {
    openConfirmModal({
      message: '确定要提交吗？',
      onConfirm: () => handleAccept(),
    });
  };

  const onDeleteScene = (sceneId: string) => {
    openConfirmModal({
      message: '确定要删除此场景吗？',
      onConfirm: () => {
        apiDeleteScene({ sceneId }).then((res) => {
          if (res.code === 200) {
            showSuccessNotification('删除成功');
            onCloseModal();
          } else {
            showErrorNotification(res.error!.message);
          }
        });
      },
    });
  };

  const formBody = (
    <form onSubmit={form.onSubmit(() => onSaveScene())}>
      <Box maw={800} mx="left" m={5}>
        <TextInput
          withAsterisk
          label="场景名称"
          placeholder="请输入场景名称"
          {...form.getInputProps('name')}
        />

        <MultiSelect
          mt="md"
          label="适用终端"
          placeholder="请选择适用终端"
          data={terminalCategoryList}
          withAsterisk
          {...form.getInputProps('terminalCategoryList')}
          comboboxProps={{ transitionProps: { transition: 'pop', duration: 200 } }}
        />
      </Box>
      {(form.values.observationPointIdList!.length || !sceneId) && (
        <ForwardedObservationPointList
          ref={observationPointListRef}
          commendObsPointList={commendObsPointList}
          toBeImprovedObsPointList={toBeImprovedObsPointList}
          initialObservationPointIdList={form.values.observationPointIdList}
        />
      )}
      <div className={styles.bottomBtn}>
        <Group justify={sceneId ? 'space-between' : 'right'} mt="md">
          {sceneId && (
            <Button
              leftSection={<IconTrash />}
              color="red"
              onClick={() => {
                onDeleteScene(sceneId);
              }}
            >
              删除此项
            </Button>
          )}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Button
              leftSection={<IconX size={14} />}
              variant="default"
              onClick={onCloseModal}
              style={{ marginRight: '10px' }}
            >
              取消
            </Button>
            <Button leftSection={<IconCheck />} type="submit">
              保存
            </Button>
          </div>
        </Group>
      </div>
    </form>
  );

  return (
    <>
      <Modal
        size="75%"
        opened={open}
        onClose={onCloseModal}
        title={sceneId ? '编辑场景' : '创建场景'}
      >
        {formBody}
      </Modal>
    </>
  );
};

export default EditForm;
