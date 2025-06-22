require("nvchad.configs.lspconfig").defaults()

local servers = { "html", "cssls", "rust_analyzer", "ruff" }
vim.lsp.enable(servers)

-- read :h vim.lsp.config for changing options of lsp servers 
