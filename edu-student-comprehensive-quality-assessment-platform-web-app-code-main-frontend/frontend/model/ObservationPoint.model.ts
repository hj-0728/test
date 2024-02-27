export interface ObservationPoint {
  id: string
  version?: number
  name: string
  category: string
  categoryName: string
  fileId: string
  fileUrl: string
  pointScore: number
  sceneIdList: string[] | null
}

export interface ObservationPointList {
  commendObsPointList: ObservationPoint[]
  toBeImprovedObsPointList: ObservationPoint[]
}

export interface DeleteObservationPoint {
  id: string
}

export interface ObservationPointSystemIcon {
  id: string
  fileUrl: string
}

export interface SaveObservationPoint {
  id?: string | null
  version?: number
  name: string
  category: string
  fileId: string
  pointScore: number
  sceneIdList: string[] | null
}
