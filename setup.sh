mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
[theme]\n\
primaryColor='"#ff8700"'\n\
backgroundColor='"#363636"'\n\
secondaryBackgroundColor='"#474747"'\n\
textColor='"#ecf0f1"'\n\
font='"sans serif"'\n\
\n\
" > ~/.streamlit/config.toml
