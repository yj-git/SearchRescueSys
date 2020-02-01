module.exports = {
    parser: '@typescript-eslint/parser',
    plugins: ['@typescript-eslint'],
    rules: {
        // 禁止使用 var
        'no-var': 'error',
        // 优先使用 interface 而不是 type
        '@typescript-eslint/consistent-type-definitions': ['error', 'interface'],
        //强制使用单引号
        quotes: ['error', 'single'],
        //强制不使用分号结尾
        semi: ['error', 'never']
    }
};
