import js from "@eslint/js";
import globals from "globals";

export default [
  {
    ignores: ["node_modules/", "dist/", ".git/", "eslint.config.js"],
  },
  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "script",
      globals: {
        ...globals.browser,
        ...globals.es2021,
      },
    },
    rules: {
      ...js.configs.recommended.rules,
      "no-unused-vars": "off",
    },
  },
];
