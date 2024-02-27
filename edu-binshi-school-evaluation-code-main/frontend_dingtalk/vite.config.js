import {defineConfig} from 'vite'

import vue from '@vitejs/plugin-vue'
import legacy from '@vitejs/plugin-legacy'


// https://vitejs.dev/config/
export default defineConfig({
    base: '/',
    build: {
        target: ['es2015']
    },
    plugins: [
        vue(),
        legacy({
            targets: ['chrome 53']
        }),
    ]
})
