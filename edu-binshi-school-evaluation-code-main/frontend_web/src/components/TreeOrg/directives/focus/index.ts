interface IBinding {
  value: any;
}
const focus = {
  beforeMount(el: HTMLElement, { value }: IBinding): void {
    if (value) {
      el.focus();
    }
  },
};
export default focus;
