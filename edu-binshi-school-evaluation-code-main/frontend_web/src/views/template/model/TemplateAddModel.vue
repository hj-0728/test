<template>
  <BasicModal
    v-bind="$attrs"
    :canFullscreen="false"
    :draggable="false"
    :keyboard="false"
    :maskClosable="false"
    :loading="loading"
    @register="register"
    title="Modal Title"
    @visible-change="handleVisibleChange"
    width="60%"
  >
    <template #title>
      <span class="inline-flex-center">
        <Icon icon="ion:settings-outline" :size="16" style="margin-right: 5px" /> Modal Title
      </span>
    </template>
    <div class="pt-3px pr-3px">
      <BasicFormFromAnt ref="basicFormFromAnt" />
    </div>
    <template #footer>
      <Button key="back" @click="close">{{ t('sys.model.close') }}</Button>
      <Button key="submit" type="primary" :loading="loading" @click="submitForm">{{
        t('sys.model.submit')
      }}</Button>
    </template>
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, ref, nextTick } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Icon } from '/@/components/Icon';
  import { Button } from '/@/components/Button';
  import BasicFormFromAnt from '../form/BasicFormFromAnt.vue';
  import { useI18n } from '/@/hooks/web/useI18n';
  export default defineComponent({
    components: { BasicModal, BasicFormFromAnt, Icon, Button },
    props: {
      userData: { type: Object },
    },
    setup(props) {
      const [register, { closeModal }] = useModalInner((data) => {
        data && onDataReceive(data);
      });

      function onDataReceive(data) {
        console.log('Data Received', data);
      }

      function handleVisibleChange(v) {
        v && props.userData && nextTick(() => onDataReceive(props.userData));
      }

      const loading = ref(false);
      const { t } = useI18n();
      const basicFormFromAnt = ref();
      return { register, handleVisibleChange, loading, t, basicFormFromAnt, closeModal };
    },
    methods: {
      submitForm() {
        this.basicFormFromAnt.onSubmit();
      },
      close() {
        this.closeModal();
      },
    },
  });
</script>
