mkdir -p ~/.streamlit/

echo "\
[theme]
primaryColor = "#fdbf00"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#ededed"
textColor= "#2e2e2e"
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
