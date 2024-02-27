module.exports = {
  extends: [
    'mantine',
    'plugin:@next/next/recommended',
    'plugin:jest/recommended',
    'plugin:storybook/recommended',
  ],
  plugins: ['testing-library', 'jest'],
  overrides: [
    {
      files: ['**/?(*.)+(spec|test).[jt]s?(x)'],
      extends: ['plugin:testing-library/react'],
    },
  ],
  parserOptions: {
    project: './tsconfig.json',
  },
  settings: {
    'import/resolver': {
      typescript: {}, // 这会让 ESLint 使用 tsconfig.json 中的路径配置
    },
  },
  rules: {
    'react/react-in-jsx-scope': 'off',
    'max-len': ['warn', {code: 120}],
  },
};
