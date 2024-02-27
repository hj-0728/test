import { StateCreator } from 'zustand';

export interface AppConfigSlice {
  colorScheme: 'dark' | 'light';
  primaryColor: any;
  toggleColorScheme: () => void;
  updatePrimaryColor: (color: string) => void;
}
export const createAppConfigSlice: StateCreator<AppConfigSlice> = (set) => ({
  colorScheme: 'light',
  primaryColor: 'grape',
  toggleColorScheme: () =>
    set((state) => ({
      colorScheme: state.colorScheme === 'dark' ? 'light' : 'dark',
    })),
  updatePrimaryColor: (color: any) => {
    set(() => ({
      primaryColor: color,
    }));
  },
});
