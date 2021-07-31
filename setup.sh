mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
[theme]
primaryColor="#FDBF00"\n\
backgroundColor="#ffffff"\n\
secondaryBackgroundColor="#f1f2f6"\n\
textColor="#2f3542"\n\
\n\
" > ~/.streamlit/config.toml
