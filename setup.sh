mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
[theme]\n\
primaryColor="#FDBF00"\n\
backgroundColor="#ffffff"\n\
secondaryBackgroundColor="#f1f2f6"\n\
textColor="#2f3542"\n\
\n\
" > ~/.streamlit/config.toml
