<template>
  <!--  添加用户-->
  <FormItem name="people">
    <template #label>
      <span v-if="state === 'add'">选择关联人员</span>
      <span v-if="state === 'edit'">关联人员</span>
    </template>
    <Input v-if="state === 'add'" v-model:value="people" @click="selectPeople" readonly />
    <span v-if="state === 'edit'">{{ people }}</span>
  </FormItem>
  <SelectPeopleList ref="select" @register="register" @selected-people="selectedPeople" />
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { Input, Form } from 'ant-design-vue';
  import SelectPeopleList from './SelectPeopleList.vue';
  import { useModal } from '/@/components/Modal';
  export default defineComponent({
    components: {
      SelectPeopleList,
      Input,
      FormItem: Form.Item,
    },
    props: {
      selectedPeopleId: {
        type: String,
        default: null,
      },
      peopleName: {
        type: String,
        default: null,
      },
      state: {
        type: String,
        required: true,
      },
    },
    emits: ['getSelectedPeopleId', 'validatePeople'],
    setup(props) {
      const [register, { openModal }] = useModal();
      const people = ref(props.peopleName);
      const peopleId = ref(props.selectedPeopleId);
      const category = ref(props.state);

      return {
        register,
        openModal,
        people,
        peopleId,
        category,
      };
    },
    unmounted() {
      this.selectPeople();
    },
    methods: {
      selectPeople() {
        if (this.state == 'add') {
          this.openModal(true, this.peopleId);
        }
      },
      selectedPeople(data) {
        this.people = data.name;
        this.peopleId = data.id;
        this.$emit('getSelectedPeopleId', this.peopleId);
        console.log('data', this.peopleId);
      },
      validatePeople() {
        this.$emit('validatePeople');
      },
    },
  });
</script>
