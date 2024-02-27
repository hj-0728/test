import { defineComponent } from 'vue';
const ifScrollable = (can: boolean) => {
  if (can == true) {
    return {
      overflowY: 'scroll',
      overflowX: 'hidden',
      position: 'absolute',
      padding: '10px',
      borderSizing: 'border-box',
      display: 'flex',
      alignContent: 'flex-start',
      paddingBottom: 0,
      flexWrap: 'wrap',
      border: '1px solid #fff',
      left: '0px',
      right: '2px',
      bottom: '6px',
      top: '6px',
    };
  } else {
    return {
      position: 'absolute',
      padding: '10px',
      borderSizing: 'border-box',
      paddingRight: '0px',
      paddingBottom: 0,
      display: 'flex',
      justifyContent: 'flex-start',
      flexDirection: 'column',
      flexWrap: 'wrap',
      border: '1px solid #fff',
      left: '0px',
      right: '0px',
      bottom: '0px',
      top: '0px',
    };
  }
};
const xboxProps = {
  scrollable: Boolean,
  style: Object as PropType<any>,
};
export default defineComponent({
  name: 'XBox',
  props: xboxProps,
  setup(props: any, { slots }) {
    return () => (
      <div
        style={{
          ...props.style,
          boxSizing: 'border-box',
          background: '#fff',

          ...ifScrollable(props.scrollable),
        }}
      >
        {slots.default && slots.default()}
      </div>
    );
  },
});
