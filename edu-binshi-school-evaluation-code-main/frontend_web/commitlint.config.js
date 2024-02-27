module.exports = {
  ignores: [(commit) => commit.includes('')],
  extends: ['@commitlint/config-conventional'],
  rules: {},
};
