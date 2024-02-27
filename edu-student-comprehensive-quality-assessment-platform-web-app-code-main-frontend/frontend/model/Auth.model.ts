export interface LoginParams {
    name: string
    password: string
}

export interface Token {
    accessToken: string
    refreshToken: string
}
