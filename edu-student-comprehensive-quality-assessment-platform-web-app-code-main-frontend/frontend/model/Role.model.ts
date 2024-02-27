export interface Role {
  id?: null | string;
  version?: number;
  parentId?: null | string;
  name: string
  code: string
  comments?: string | null
  isActivated: boolean
}

export interface ChangeIsActivated {
  id: string
  version: number
  isActivated: boolean
}
