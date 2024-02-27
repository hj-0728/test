export interface Menu {
  id?: string
  version?: number
  parentId: string | null
  name: string
  path: string
  icon: string
  seq?: number
}

export interface NavbarMenu {
  id: string
  name: string
  path: string
  icon: string
  childList: NavbarMenu[]
  opened: boolean
}

export interface MenuTree {
  id: string
  version: number
  parentId: string | null
  name: string
  childList: MenuTree[]
}

export interface PrimereactMenuTree {
  key: string
  version: number
  label: string
  children: PrimereactMenuTree[]
}

export interface UpdateMenuSort {
  id: string
  version: number
  parentId: string | null
  seq: number
}
