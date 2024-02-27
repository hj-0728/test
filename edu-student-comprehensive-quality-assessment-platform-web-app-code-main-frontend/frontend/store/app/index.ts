import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { UserSlice, createUserSlice } from './slices/user';
import { createSidebarSlice, SidebarConfigSlice } from './slices/sidebar';
import { AppConfigSlice, createAppConfigSlice } from './slices/config';

const useAppState = create<UserSlice & SidebarConfigSlice & AppConfigSlice>()(
  persist(
    (...p) => ({
      ...createUserSlice(...p),
      ...createSidebarSlice(...p),
      ...createAppConfigSlice(...p),
    }),
    {
      name: 'app-state',
      partialize: (state) =>
        Object.fromEntries(Object.entries(state).filter(([key]) => !['config'].includes(key))),
    }
  )
);

export default useAppState;
