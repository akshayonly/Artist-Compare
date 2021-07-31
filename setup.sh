mkdir -p ~/.streamlit/

echo "\
[theme]\n\
primaryColor = "#fdbf00"\n\
backgroundColor = "#ffffff"\n\
secondaryBackgroundColor = "#ededed"\n\
textColor= "#2e2e2e"\n\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
