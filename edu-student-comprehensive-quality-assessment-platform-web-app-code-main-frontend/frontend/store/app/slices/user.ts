import { StateCreator } from 'zustand';
import { UserInfo } from 'MyApp';
import { NavbarMenu } from '@/model/Menu.model';

export interface UserSlice {
  accessToken: string;
  refreshToken: string;
  userInfo: UserInfo | null;
  navbarMenu: NavbarMenu[];
  logout: () => void;
  updateNavbarMenuOpened: (menuId: string) => void;
}

export const createUserSlice: StateCreator<UserSlice> = (set) => ({
  accessToken: '',
  refreshToken: '',
  userInfo: null,
  navbarMenu: [],
  logout: () => {
    set({ accessToken: '', refreshToken: '', userInfo: null, navbarMenu: [] });
  },
  updateNavbarMenuOpened: (menuId: string) => {
    set((state) => ({
      navbarMenu: state.navbarMenu.map((item: NavbarMenu) =>
        item.id === menuId ? { ...item, opened: !item.opened } : item
      ),
    }));
  },
});
